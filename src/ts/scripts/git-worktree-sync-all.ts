#!/usr/bin/env npx tsx

/**
 * Sync All Worktrees - Boomerang Script
 * 
 * Ported and generalized from Spideryarn Reading's sync-worktrees-all.ts
 * Original was hardcoded for specific worktree naming and npm dependencies
 * 
 * Changes from original:
 * - Removed Spideryarn-specific references and hardcoded paths
 * - Made package manager configurable (npm, yarn, pnpm)
 * - Made branch pattern configurable (not hardcoded to worktree1-6)
 * - Made dependency command configurable (not just npm ci)
 * - Generalized to work with any Git worktree setup
 * - Made script paths configurable for the sync script location
 * 
 * This wrapper script automates the two-step sync process across all worktrees:
 * 1. From main: Collects changes from all worktree branches
 * 2. From each worktree: Pulls latest main changes
 * 
 * Run this from your main worktree to sync everything in one command.
 * The script will "boomerang" - go out to each worktree and come back.
 */

import { Cli, Command, Option, UsageError } from 'clipanion';
import { execSync } from 'child_process';
import { existsSync } from 'fs';
import { resolve, basename } from 'path';

class GitWorktreeSyncAllCommand extends Command {
  static paths = [
    ['git-worktree-sync-all'],
    ['sync-all-worktrees'],
    Command.Default,
  ];

  static usage = Command.Usage({
    description: 'Sync all worktrees with main branch in both directions',
    details: `
      This "boomerang" script automates the two-step sync process across all worktrees:
      
      1. From main: Collects changes from all worktree branches
      2. From each worktree: Pulls latest main changes
      
      The script must be run from your main worktree. It will visit each worktree
      to complete the sync process, then return to main.
      
      With --ignore-dirty, the script will skip any worktrees that have uncommitted
      changes, preventing potential merge conflicts or lost work.
      
      By default, dependency install is run in each worktree after successful Git sync
      to ensure dependencies are up to date. Configure with --deps-command or disable
      with --run-deps=false for faster execution.
    `,
    examples: [
      ['Sync all worktrees', 'git-worktree-sync-all'],
      ['Skip worktrees with uncommitted changes', 'git-worktree-sync-all --ignore-dirty'],
      ['Sync without running dependency install', 'git-worktree-sync-all --run-deps=false'],
      ['Use yarn instead of npm', 'git-worktree-sync-all --deps-command "yarn install"'],
      ['Custom worktree pattern', 'git-worktree-sync-all --pattern "feature-*"'],
    ],
  });

  ignoreDirty = Option.Boolean('--ignore-dirty', false, {
    description: 'Skip worktrees with uncommitted changes',
  });

  runDeps = Option.Boolean('--run-deps', true, {
    description: 'Run dependency install in each worktree after successful Git sync (default: true)',
  });

  depsCommand = Option.String('--deps-command', 'npm ci', {
    description: 'Command to run for dependency installation (default: npm ci)',
  });

  pattern = Option.String('--pattern', 'worktree*', {
    description: 'Pattern to match worktree branches (default: worktree*)',
  });

  mainBranch = Option.String('--main', 'main', {
    description: 'Name of the main branch (default: main)',
  });

  syncScript = Option.String('--sync-script', './git-worktree-sync.ts', {
    description: 'Path to the sync script relative to each worktree (default: ./git-worktree-sync.ts)',
  });

  verbose = Option.Boolean('-v,--verbose', false, {
    description: 'Show verbose output',
  });

  // ANSI color codes for output
  private colors = {
    reset: '\x1b[0m',
    bright: '\x1b[1m',
    green: '\x1b[32m',
    yellow: '\x1b[33m',
    red: '\x1b[31m',
    cyan: '\x1b[36m',
  };

  private log(message: string, color: string = this.colors.reset) {
    this.context.stdout.write(`${color}${message}${this.colors.reset}\n`);
  }

  private execInDirectory(directory: string, command: string): { success: boolean; output?: string; error?: string } {
    try {
      const output = execSync(command, {
        cwd: directory,
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      });
      return { success: true, output };
    } catch (error: any) {
      return { 
        success: false, 
        error: error.message || 'Unknown error',
        output: error.stdout?.toString() || ''
      };
    }
  }

  private isWorktreeDirty(worktreePath: string): boolean {
    try {
      const status = execSync('git status --porcelain', {
        cwd: worktreePath,
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      }).trim();
      return status.length > 0;
    } catch {
      // If we can't check status, consider it dirty to be safe
      return true;
    }
  }

  private getMatchingBranches(): string[] {
    try {
      const branches = execSync('git branch --list', { encoding: 'utf8' })
        .split('\n')
        .map(b => b.replace(/^[\*\+]?\s*/, '').trim())
        .filter(b => b.length > 0);
      
      // Convert shell-style pattern to regex
      const regexPattern = this.pattern
        .replace(/\*/g, '.*')
        .replace(/\?/g, '.');
      const regex = new RegExp(`^${regexPattern}$`);
      
      return branches.filter(b => regex.test(b) && b !== this.mainBranch);
    } catch {
      return [];
    }
  }

  async execute(): Promise<number> {
    try {
      this.log('🔄 Git Worktree Sync All - Boomerang Mode', this.colors.bright);
      if (this.ignoreDirty) {
        this.log('   Option: --ignore-dirty (skipping dirty worktrees)', this.colors.yellow);
      }
      if (!this.runDeps) {
        this.log('   Option: --run-deps=false (skipping dependency install)', this.colors.yellow);
      } else {
        this.log(`   Dependencies: ${this.depsCommand}`, this.colors.cyan);
      }
      if (this.verbose) {
        this.log(`   Pattern: ${this.pattern}`, this.colors.cyan);
        this.log(`   Main branch: ${this.mainBranch}`, this.colors.cyan);
      }
      
      // Get current directory (should be main)
      const currentDir = process.cwd();
      const currentBranch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
      
      if (currentBranch !== this.mainBranch) {
        throw new UsageError(
          `This script must be run from the ${this.mainBranch} branch.\n` +
          `Current branch: ${currentBranch}\n` +
          `Please switch to ${this.mainBranch} branch and try again.`
        );
      }
      
      // Get all worktrees
      const worktreeOutput = execSync('git worktree list --porcelain', { encoding: 'utf8' });
      const worktrees = this.parseWorktreeList(worktreeOutput);
      
      // Get matching branches and filter worktrees
      const matchingBranches = this.getMatchingBranches();
      
      if (matchingBranches.length === 0) {
        throw new UsageError(
          `No branches matching pattern '${this.pattern}' found.\n` +
          `Create branches or adjust the pattern with --pattern <pattern>`
        );
      }

      // Filter for matching worktrees and main
      const standardWorktrees = worktrees
        .filter(wt => wt.branch && (matchingBranches.includes(wt.branch) || wt.branch === this.mainBranch))
        .sort((a, b) => {
          // Put main first, then sort others alphabetically
          if (a.branch === this.mainBranch) return -1;
          if (b.branch === this.mainBranch) return 1;
          return a.branch!.localeCompare(b.branch!);
        });
      
      // Track worktrees that are skipped due to non-matching patterns
      const nonMatchingWorktrees = worktrees
        .filter(wt => wt.branch && 
                wt.branch !== this.mainBranch && 
                !matchingBranches.includes(wt.branch))
        .sort((a, b) => a.branch!.localeCompare(b.branch!));
      
      const worktreeOnlyPaths = standardWorktrees.filter(wt => wt.branch !== this.mainBranch);
      
      if (worktreeOnlyPaths.length === 0) {
        throw new UsageError(`No worktrees with matching branches found. Create matching worktree branches first.`);
      }
      
      this.log(`\nFound ${worktreeOnlyPaths.length} matching worktrees:`, this.colors.cyan);
  
      // Check dirty status if needed
      let cleanWorktrees = worktreeOnlyPaths;
      const dirtyWorktrees: typeof worktreeOnlyPaths = [];
      
      if (this.ignoreDirty) {
        cleanWorktrees = [];
        for (const wt of worktreeOnlyPaths) {
          const isDirty = this.isWorktreeDirty(wt.path);
          if (isDirty) {
            dirtyWorktrees.push(wt);
            this.log(`  • ${wt.branch} → ${wt.path} (⚠️  dirty - skipping)`, this.colors.yellow);
          } else {
            cleanWorktrees.push(wt);
            this.log(`  • ${wt.branch} → ${wt.path}`, this.colors.green);
          }
        }
        
        if (cleanWorktrees.length === 0) {
          this.log(`\n⚠️  All matching worktrees are dirty. No branches to sync.`, this.colors.yellow);
          this.log(`   Use without --ignore-dirty to sync anyway.`, this.colors.yellow);
          return 0;
        }
      } else {
        worktreeOnlyPaths.forEach(wt => {
          this.log(`  • ${wt.branch} → ${wt.path}`);
        });
      }

      // Show non-matching worktrees if verbose
      if (this.verbose && nonMatchingWorktrees.length > 0) {
        this.log(`\nNon-matching worktrees (skipped):`, this.colors.yellow);
        nonMatchingWorktrees.forEach(wt => {
          this.log(`  • ${wt.branch} → ${wt.path} (doesn't match pattern)`, this.colors.yellow);
        });
      }
  
      // Step 1: Sync all worktrees to main (from main)
      this.log(`\n📥 Step 1: Collecting changes from matching worktrees...`, this.colors.bright);
      this.log(`   Running from: ${currentDir}\n`);
  
      // Build sync command - use git-worktree-sync if available, otherwise look for the original
      let syncCommand = 'git-worktree-sync';
      if (!this.checkCommandExists(syncCommand)) {
        // Try the original script name
        syncCommand = './scripts/sync-worktrees.ts';
        if (!existsSync(resolve(currentDir, syncCommand))) {
          // Try our script
          syncCommand = this.syncScript;
          if (!existsSync(resolve(currentDir, syncCommand))) {
            throw new UsageError(
              'Sync script not found. Please ensure git-worktree-sync is in PATH or ' +
              `specify the correct path with --sync-script`
            );
          }
        }
      }

      if (this.ignoreDirty && cleanWorktrees.length < worktreeOnlyPaths.length) {
        // Need to sync specific branches only
        for (const wt of cleanWorktrees) {
          this.log(`   Syncing ${wt.branch}...`);
          const branchResult = this.execInDirectory(currentDir, `${syncCommand} --branch ${wt.branch} --main ${this.mainBranch}`);
          if (!branchResult.success) {
            this.log(`\n❌ Failed to sync ${wt.branch} to ${this.mainBranch}:`, this.colors.red);
            this.log(branchResult.error || 'Unknown error', this.colors.red);
            if (branchResult.output) {
              this.log(`\nOutput:`, this.colors.yellow);
              this.context.stdout.write(branchResult.output + '\n');
            }
            this.log(`\n🔧 Fix the issues above and try again.`, this.colors.yellow);
            return 1;
          }
          if (branchResult.output && this.verbose) {
            this.context.stdout.write(branchResult.output + '\n');
          }
        }
      } else {
        // Sync all matching branches
        const step1Result = this.execInDirectory(currentDir, `${syncCommand} --main ${this.mainBranch} --pattern "${this.pattern}"`);
        
        if (!step1Result.success) {
          this.log(`\n❌ Failed to sync worktrees to ${this.mainBranch}:`, this.colors.red);
          this.log(step1Result.error || 'Unknown error', this.colors.red);
          if (step1Result.output) {
            this.log(`\nOutput:`, this.colors.yellow);
            this.context.stdout.write(step1Result.output + '\n');
          }
          this.log(`\n🔧 Fix the issues above and try again.`, this.colors.yellow);
          return 1;
        }
        
        if (step1Result.output && this.verbose) {
          this.context.stdout.write(step1Result.output + '\n');
        }
      }

      // Run dependency install in main after merging worktree changes
      if (this.runDeps) {
        this.log(`\n📦 Running dependencies in ${this.mainBranch}...`, this.colors.cyan);
        const mainDepsResult = this.execInDirectory(currentDir, this.depsCommand);
        
        if (mainDepsResult.success) {
          this.log(`✅ Dependencies completed in ${this.mainBranch}`, this.colors.green);
        } else {
          this.log(`❌ Dependencies failed in ${this.mainBranch}`, this.colors.red);
          if (mainDepsResult.error) {
            this.log(`Error: ${mainDepsResult.error}`, this.colors.red);
          }
          if (mainDepsResult.output && this.verbose) {
            this.log(`Dependency output:`, this.colors.yellow);
            this.context.stdout.write(mainDepsResult.output + '\n');
          }
          this.log(`\n🔧 Fix dependency issues in ${this.mainBranch} and try again.`, this.colors.yellow);
          return 1;
        }
      }
  
      // Step 2: Go to each worktree and pull from main
      this.log(`\n📤 Step 2: Distributing ${this.mainBranch} to all worktrees...`, this.colors.bright);
      
      let allSuccess = true;
      const results: Array<{ branch: string; success: boolean; error?: string; skipped?: boolean; skipReason?: string; path?: string }> = [];
      
      // If ignoring dirty, add skipped results for dirty worktrees
      if (this.ignoreDirty) {
        for (const wt of dirtyWorktrees) {
          results.push({ branch: wt.branch!, success: true, skipped: true });
        }
      }
      
      // Add skipped results for non-matching branch worktrees
      for (const wt of nonMatchingWorktrees) {
        results.push({ 
          branch: wt.branch!, 
          success: true, 
          skipped: true, 
          skipReason: 'non-matching pattern',
          path: wt.path
        });
      }
      
      // Only sync clean worktrees
      const worktreesToSync = this.ignoreDirty ? cleanWorktrees : worktreeOnlyPaths;
      
      for (const worktree of worktreesToSync) {
        this.log(`\n🔀 Syncing ${worktree.branch}...`, this.colors.cyan);
        this.log(`   Going to: ${worktree.path}`);
        
        // Check for sync script in worktree
        const syncScriptPath = resolve(worktree.path, this.syncScript.replace(/^\.\//, ''));
        
        if (!existsSync(syncScriptPath)) {
          this.log(`   ⚠️  Script not found at ${syncScriptPath}`, this.colors.yellow);
          results.push({ branch: worktree.branch!, success: false, error: 'Script not found' });
          allSuccess = false;
          continue;
        }
        
        const result = this.execInDirectory(worktree.path, `${this.syncScript} --main ${this.mainBranch}`);
        
        if (result.success) {
          this.log(`   ✅ Git sync successful`, this.colors.green);
          if (result.output && this.verbose) {
            // Show the output but indent it
            this.context.stdout.write(result.output.split('\n').map(line => '      ' + line).join('\n') + '\n');
          }
          
          // Run dependency install if enabled
          if (this.runDeps) {
            this.log(`   📦 Running dependencies...`, this.colors.cyan);
            const depsResult = this.execInDirectory(worktree.path, this.depsCommand);
            
            if (depsResult.success) {
              this.log(`   ✅ Dependencies completed`, this.colors.green);
              results.push({ branch: worktree.branch!, success: true });
            } else {
              this.log(`   ❌ Dependencies failed`, this.colors.red);
              if (depsResult.error) {
                this.log(`   Error: ${depsResult.error}`, this.colors.red);
              }
              if (depsResult.output && this.verbose) {
                this.log(`   Dependency output:`, this.colors.yellow);
                this.context.stdout.write(depsResult.output.split('\n').map(line => '      ' + line).join('\n') + '\n');
              }
              results.push({ branch: worktree.branch!, success: false, error: `Dependencies failed: ${depsResult.error}` });
              allSuccess = false;
            }
          } else {
            results.push({ branch: worktree.branch!, success: true });
          }
        } else {
          this.log(`   ❌ Git sync failed`, this.colors.red);
          if (result.error) {
            this.log(`   Error: ${result.error}`, this.colors.red);
          }
          if (result.output) {
            this.context.stdout.write(result.output.split('\n').map(line => '      ' + line).join('\n') + '\n');
          }
          this.log(`\n🛑 Stopping immediately due to merge conflict or sync failure.`, this.colors.red);
          this.log(`   Fix the issues in ${worktree.branch} and try again.`, this.colors.yellow);
          return 1;
        }
      }
  
      // Final summary
      this.log(`\n${'='.repeat(50)}`, this.colors.bright);
      this.log(`🏁 Sync Complete - Boomerang Returned!`, this.colors.bright);
      this.log(`${'='.repeat(50)}\n`, this.colors.bright);
      
      const successCount = results.filter(r => r.success).length;
      this.log(`Summary: ${successCount}/${results.length} worktrees synced successfully\n`);
      
      results.forEach(result => {
        let icon, color, suffix;
        if (result.skipped) {
          icon = '⏭️';
          color = this.colors.yellow;
          if (result.skipReason === 'non-matching pattern') {
            const folderName = result.path ? basename(result.path) : 'unknown';
            suffix = ` (skipped - non-matching pattern in ${folderName}/)`;
          } else {
            suffix = ' (skipped - dirty)';
          }
        } else if (result.success) {
          icon = '✅';
          color = this.colors.green;
          suffix = '';
        } else {
          icon = '❌';
          color = this.colors.red;
          suffix = result.error ? ': ' + result.error : '';
        }
        this.log(`  ${icon} ${result.branch}${suffix}`, color);
      });
      
      if (!allSuccess) {
        this.log(`\n⚠️  Some worktrees failed to sync.`, this.colors.yellow);
        this.log(`   Check the errors above and resolve any merge conflicts.`, this.colors.yellow);
        this.log(`   Then run the sync script manually in those worktrees.`, this.colors.yellow);
        return 1;
      } else {
        this.log(`\n🎉 All matching worktrees are now in sync!`, this.colors.green);
        const timestamp = this.formatTimestamp();
        this.log(`   Completed at ${timestamp}`, this.colors.cyan);
        return 0;
      }
    } catch (error) {
      if (error instanceof UsageError) {
        throw error;
      }
      this.log(`\n❌ Unexpected error:`, this.colors.red);
      this.log(error instanceof Error ? error.message : String(error), this.colors.red);
      this.log(`\n🔧 Recovery options:`, this.colors.yellow);
      this.log(`   • Check git status in all worktrees`, this.colors.yellow);
      this.log(`   • Verify worktree structure: git worktree list`, this.colors.yellow);
      this.log(`   • Ensure sync script exists in worktrees`, this.colors.yellow);
      return 1;
    }
  }

  private checkCommandExists(command: string): boolean {
    try {
      execSync(`which ${command}`, { stdio: 'pipe' });
      return true;
    } catch {
      return false;
    }
  }

  private formatTimestamp(): string {
    const date = new Date();
    const formattedDate = `${date.getFullYear()}-${date.toLocaleDateString('en-US', { month: 'short' }).toUpperCase()}-${date.getDate().toString().padStart(2, '0')}`;
    const formattedTime = date.toLocaleTimeString('en-US', { hour12: false });
    return `${formattedDate} ${formattedTime}`;
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
}

// CLI setup
const cli = new Cli({
  binaryLabel: 'Git Worktree Sync All Tool',
  binaryName: 'git-worktree-sync-all',
  binaryVersion: '1.0.0',
});

cli.register(GitWorktreeSyncAllCommand);
cli.runExit(process.argv.slice(2));