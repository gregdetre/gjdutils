#!/usr/bin/env npx tsx

/**
 * Git Worktree Branch Synchronization Tool
 * 
 * Ported and generalized from Spideryarn Reading's sync-worktrees.ts
 * Original was specific to that project's worktree setup and naming conventions
 * 
 * Changes from original:
 * - Removed Spideryarn branding and specific references
 * - Made branch naming patterns configurable (not hardcoded to worktree1-6)
 * - Kept the excellent autostash functionality
 * - Made main branch name configurable (already was via --main option)
 * - Generalized worktree validation logic to work with any naming pattern
 * - Made worktree pattern configurable via --pattern option
 * - Added support for custom worktree directory naming
 * 
 * This script provides one-direction merge synchronization between the current
 * branch and main branch. Always requires a two-step process for complete sync:
 * 1. From feature branch: merge main → current
 * 2. From main branch: merge specified branch → main
 * 
 * For automated two-way sync across all worktrees, use git-worktree-sync-all.ts
 * 
 * AUTOSTASH SUPPORT:
 * This script uses Git's built-in --autostash functionality to safely handle
 * uncommitted changes during merges. Local changes are automatically stashed
 * before the merge and reapplied afterward.
 */

import { Cli, Command, Option } from 'clipanion';
import { execSync } from 'child_process';

class GitWorktreeSyncCommand extends Command {
  static paths = [
    ['git-worktree-sync'],
    ['sync-branches'],
    Command.Default,
  ];

  static usage = Command.Usage({
    description: 'Sync current branch with main branch using one-direction merge',
    details: `
      This tool synchronizes Git worktree branches with the main branch using
      one-way merges. It supports both directions:
      
      From feature branch: Merges main → current branch
      From main branch: Merges specified branch → main
      
      The tool uses Git's autostash feature to safely handle uncommitted changes,
      automatically stashing them before merge and reapplying afterward.
      
      Supports configurable worktree naming patterns and branch conventions.
    `,
    examples: [
      ['Sync current branch with main', 'git-worktree-sync'],
      ['Sync with custom main branch', 'git-worktree-sync --main develop'],
      ['Sync specific branch with main (from main)', 'git-worktree-sync --branch feature-1'],
      ['Sync all matching worktrees (from main)', 'git-worktree-sync --pattern "wt*"'],
    ],
  });

  mainBranch = Option.String('--main', 'main', {
    description: 'Name of the main branch (default: main)',
  });

  targetBranch = Option.String('--branch', {
    description: 'Specific branch to sync with main (when on main)',
  });

  pattern = Option.String('--pattern', 'worktree*', {
    description: 'Pattern to match worktree branches (default: worktree*)',
  });

  verbose = Option.Boolean('-v,--verbose', false, {
    description: 'Show verbose output',
  });

  async execute(): Promise<number> {
    try {
      // Safety checks
      await this.runSafetyChecks();

      const currentBranch = this.getCurrentBranch();

      if (currentBranch === this.mainBranch && !this.targetBranch) {
        // From main without specific branch: sync all matching worktrees
        await this.syncAllWorktrees();
      } else {
        // Normal single-branch sync
        const { sourceBranch, targetBranch } = this.determineSyncDirection(currentBranch);
        this.log(`🔀 ${sourceBranch} → ${targetBranch}`);

        await this.performOneDirectionMerge(sourceBranch, targetBranch);

        this.log('✅ Synced');
        const timestamp = this.formatTimestamp();
        this.log(`Synced at ${timestamp}`);
        
        // Provide next step guidance
        if (currentBranch === this.mainBranch) {
          this.log(`Next: sync from ${sourceBranch} worktree to pull changes`);
        } else {
          this.log(`Next: sync from main to merge ${currentBranch} → main`);
        }
      }
      
      return 0;

    } catch (error) {
      console.error('\n❌ Sync failed:', error instanceof Error ? error.message : error);
      console.error('\n🔧 Recovery options:');
      console.error('   • If merge conflicts: resolve conflicts, git add <files>, git commit');
      console.error('   • If autostash conflicts: run "git stash show -p" to see changes, then "git stash drop" or resolve manually');
      console.error('   • If worktree issues: check worktree setup with "git worktree list"');
      console.error('   • If persistent issues: git status and git log --oneline -5 for diagnostics\n');
      return 1;
    }
  }

  private async runSafetyChecks(): Promise<void> {
    // Check if we're in a git repository
    try {
      this.execGit('rev-parse --git-dir');
    } catch {
      throw new Error('Not in a git repository. Run this script from within a git repository.');
    }

    // Check for uncommitted changes and inform user about autostash
    const status = this.execGit('status --porcelain').trim();
    if (status) {
      this.log('📦 Uncommitted changes detected - using autostash');
    }

    // Check if main branch exists
    const branches = this.execGit('branch --list').split('\n').map(b => b.replace(/^[\*\+]?\s*/, ''));
    
    if (!branches.includes(this.mainBranch)) {
      throw new Error(`Main branch '${this.mainBranch}' does not exist. Create it or specify correct branch with --main <branch>`);
    }

    // Validate worktree structure if doing sync-all
    const currentBranch = this.getCurrentBranch();
    if (currentBranch === this.mainBranch && !this.targetBranch) {
      await this.validateWorktreeStructure();
    }

    // Show ready message if there were warnings
    if (status || this.verbose) {
      this.log('✅ Ready to sync');
    }
  }

  private getCurrentBranch(): string {
    return this.execGit('branch --show-current').trim();
  }

  private async validateWorktreeStructure(): Promise<void> {
    // Get all worktrees
    const worktreeInfo = this.getWorktreeInfo();
    
    // For sync-all operations, ensure we have matching branches to sync
    const matchingBranches = this.getMatchingBranches();
    if (matchingBranches.length === 0) {
      throw new Error(
        `No branches matching pattern '${this.pattern}' found. ` +
        `Create branches or adjust the pattern with --pattern <pattern>`
      );
    }

    if (this.verbose) {
      this.log(`Found ${matchingBranches.length} branches matching pattern '${this.pattern}': ${matchingBranches.join(', ')}`);
    }
  }

  private getWorktreeInfo(): { branches: string[], worktrees: Map<string, string> } {
    // Get all worktrees from git
    const worktreeOutput = this.execGit('worktree list --porcelain');
    const worktrees = this.parseWorktreeList(worktreeOutput);
    
    // Get all branches
    const branches = this.execGit('branch --list').split('\n')
      .map(b => b.replace(/^[\*\+]?\s*/, '').trim())
      .filter(b => b.length > 0);
    
    // Filter for matching branches
    const matchingBranches = this.getMatchingBranches();
    
    // Create a map of branch to worktree path
    const worktreeMap = new Map<string, string>();
    for (const wt of worktrees) {
      if (wt.branch && matchingBranches.includes(wt.branch)) {
        worktreeMap.set(wt.branch, wt.path);
      }
    }
    
    return { branches: matchingBranches, worktrees: worktreeMap };
  }

  private getMatchingBranches(): string[] {
    const branches = this.execGit('branch --list').split('\n')
      .map(b => b.replace(/^[\*\+]?\s*/, '').trim())
      .filter(b => b.length > 0);
    
    // Convert shell-style pattern to regex
    const regexPattern = this.pattern
      .replace(/\*/g, '.*')
      .replace(/\?/g, '.');
    const regex = new RegExp(`^${regexPattern}$`);
    
    return branches.filter(b => regex.test(b) && b !== this.mainBranch);
  }

  private parseWorktreeList(output: string): Array<{ path: string, branch: string | null }> {
    const worktrees: Array<{ path: string, branch: string | null }> = [];
    const lines = output.split('\n');
    
    let currentWorktree: { path?: string, branch?: string | null } = {};
    for (const line of lines) {
      if (line.startsWith('worktree ')) {
        if (currentWorktree.path) {
          worktrees.push({ 
            path: currentWorktree.path, 
            branch: currentWorktree.branch || null 
          });
        }
        currentWorktree = { path: line.substring(9) };
      } else if (line.startsWith('branch refs/heads/')) {
        currentWorktree.branch = line.substring(18);
      } else if (line === 'detached') {
        currentWorktree.branch = null;
      }
    }
    
    // Don't forget the last worktree
    if (currentWorktree.path) {
      worktrees.push({ 
        path: currentWorktree.path, 
        branch: currentWorktree.branch || null 
      });
    }
    
    return worktrees;
  }

  private determineSyncDirection(currentBranch: string): { sourceBranch: string; targetBranch: string } {
    if (currentBranch === this.mainBranch) {
      // From main: need to specify which branch to sync
      if (!this.targetBranch) {
        throw new Error(`When on main branch, specify which branch to sync: --branch <branch-name>`);
      }
      // Verify target branch exists
      const branches = this.execGit('branch --list').split('\n').map(b => b.replace(/^[\*\+]?\s*/, ''));
      if (!branches.includes(this.targetBranch)) {
        throw new Error(`Target branch '${this.targetBranch}' does not exist. Create it: git checkout -b ${this.targetBranch}`);
      }
      return { sourceBranch: this.targetBranch, targetBranch: this.mainBranch };
    } else {
      // From feature branch: sync main → current
      return { sourceBranch: this.mainBranch, targetBranch: currentBranch };
    }
  }

  private async syncAllWorktrees(): Promise<void> {
    this.log('🔄 Syncing all matching branches with main...\n');
    
    // Get all matching branches
    const matchingBranches = this.getMatchingBranches().sort();
    
    if (matchingBranches.length === 0) {
      throw new Error(`No branches matching pattern '${this.pattern}' found to sync`);
    }
    
    this.log(`Found ${matchingBranches.length} matching branches: ${matchingBranches.join(', ')}\n`);
    
    for (const branch of matchingBranches) {
      this.log(`🔀 ${branch} → main`);
      // Will abort if there are conflicts
      await this.performOneDirectionMerge(branch, this.mainBranch);
    }
    
    const timestamp = this.formatTimestamp();
    this.log(`\n✅ Synced all ${matchingBranches.length} branches to main`);
    this.log(`Synced at ${timestamp}`);
    this.log('Next: run this script from each worktree to pull latest main');
  }

  private async performOneDirectionMerge(sourceBranch: string, targetBranch: string): Promise<void> {
    const currentBranch = this.getCurrentBranch();
    
    if (currentBranch === targetBranch) {
      // Use Git's built-in autostash to safely handle uncommitted changes
      this.execGit(`merge --autostash ${sourceBranch}`, {
        errorMessage: `Merge conflicts during ${sourceBranch} → ${targetBranch}.`
      });
    } else {
      throw new Error(`Expected to be on ${targetBranch} branch, but currently on ${currentBranch}`);
    }
  }

  private execGit(command: string, options?: { errorMessage?: string }): string {
    try {
      return execSync(`git ${command}`, { 
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      });
    } catch (error) {
      if (options?.errorMessage) {
        throw new Error(options.errorMessage);
      }
      throw error;
    }
  }

  private formatTimestamp(): string {
    const date = new Date();
    const formattedDate = `${date.getFullYear()}-${date.toLocaleDateString('en-US', { month: 'short' }).toUpperCase()}-${date.getDate().toString().padStart(2, '0')}`;
    const formattedTime = date.toLocaleTimeString('en-US', { hour12: false });
    return `${formattedDate} ${formattedTime}`;
  }

  private log(message: string): void {
    if (this.verbose || !message.includes('Next:')) {
      console.log(message);
    }
  }
}

// CLI setup
const cli = new Cli({
  binaryLabel: 'Git Worktree Sync Tool',
  binaryName: 'git-worktree-sync',
  binaryVersion: '1.0.0',
});

cli.register(GitWorktreeSyncCommand);
cli.runExit(process.argv.slice(2));