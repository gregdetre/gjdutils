#!/usr/bin/env npx tsx

/**
 * Count Lines - Count lines of source code with configurable exclusions
 * 
 * Ported and generalized from Spideryarn Reading's count_lines.sh
 * Original was a bash script specific to that project's structure
 * 
 * Changes from original:
 * - Converted from bash to TypeScript for cross-platform compatibility
 * - Removed project-specific exclusions (gjdutils, Spideryarn paths)
 * - Made all exclusion patterns configurable via command line options
 * - Added support for custom file and directory patterns
 * - Kept --by-file and --exclude-tests functionality
 * - Uses cloc as external dependency (must be installed separately)
 * 
 * Prerequisites:
 * - Install cloc: brew install cloc (macOS) or sudo apt-get install cloc (Ubuntu)
 * - Or download from: https://github.com/AlDanial/cloc
 */

import { Cli, Command, Option, UsageError } from 'clipanion';
import { execSync, execFileSync } from 'child_process';
import { writeFileSync, unlinkSync } from 'fs';
import { tmpdir } from 'os';
import { join } from 'path';

class CountLinesCommand extends Command {
  static paths = [['count-lines'], Command.Default];
  
  static usage = Command.Usage({
    description: 'Count lines of source code with configurable exclusions',
    details: `
      This tool counts lines of code in your project using cloc, with smart defaults
      for excluding generated files, dependencies, and build artifacts.
      
      The tool automatically excludes common directories like node_modules, .git,
      build artifacts, and generated files. You can customize exclusions and
      get detailed breakdowns by file.
      
      Requires cloc to be installed: https://github.com/AlDanial/cloc
    `,
    examples: [
      ['Count all source code', 'count-lines'],
      ['Count with file-by-file breakdown', 'count-lines --by-file'],
      ['Count excluding tests', 'count-lines --exclude-tests'],
      ['Count with custom exclusions', 'count-lines --exclude-dirs build,dist --exclude-files "*.generated.ts"'],
      ['Count only specific file types', 'count-lines --include-files "*.ts,*.js"'],
    ],
  });

  byFile = Option.Boolean('--by-file', false, {
    description: 'Show breakdown by individual files',
  });

  excludeTests = Option.Boolean('--exclude-tests', false, {
    description: 'Exclude test files from the count',
  });

  excludeDirs = Option.String('--exclude-dirs', {
    description: 'Additional directories to exclude (comma-separated)',
  });

  excludeFiles = Option.String('--exclude-files', {
    description: 'File patterns to exclude (comma-separated)',
  });

  includeFiles = Option.String('--include-files', {
    description: 'Only include files matching these patterns (comma-separated)',
  });

  verbose = Option.Boolean('-v,--verbose', false, {
    description: 'Show verbose output including cloc command',
  });

  async execute(): Promise<number> {
    try {
      // Check if cloc is installed
      this.checkClocInstalled();

      // Build cloc command
      const clocArgs = this.buildClocCommand();

      if (this.verbose) {
        this.context.stdout.write(`Running: cloc ${clocArgs.map(arg => {
          // Show how args will be quoted in shell
          if (arg.includes(' ') || arg.includes('|') || arg.includes('$')) {
            return `'${arg}'`;
          }
          return arg;
        }).join(' ')}\n\n`);
      }

      // Execute cloc command using execFileSync to avoid shell interpretation
      const result = execFileSync('cloc', clocArgs, { encoding: 'utf8' });

      // If excluding tests, also show test-only count
      if (this.excludeTests) {
        this.showTestSummary();
      }

      this.context.stdout.write(result);

      return 0;

    } catch (error) {
      if (error instanceof UsageError) {
        throw error;
      }

      this.context.stderr.write(`❌ Error counting lines: ${error.message}\n`);
      this.context.stderr.write('\n🔧 Recovery options:\n');
      this.context.stderr.write('   • Install cloc: brew install cloc (macOS) or apt-get install cloc (Linux)\n');
      this.context.stderr.write('   • Check that you\'re in a valid project directory\n');
      this.context.stderr.write('   • Try with --verbose to see the cloc command being run\n');

      return 1;
    }
  }

  private checkClocInstalled(): void {
    try {
      execSync('which cloc', { stdio: 'pipe' });
    } catch {
      throw new UsageError(
        'cloc not found. Please install it:\n' +
        '  • macOS: brew install cloc\n' +
        '  • Ubuntu/Debian: sudo apt-get install cloc\n' +
        '  • Or download from: https://github.com/AlDanial/cloc'
      );
    }
  }

  private buildClocCommand(): string[] {
    const args: string[] = ['.'];

    // Base exclusions - common directories to ignore
    const baseExcludeDirs = [
      '.git',
      '.next',
      '.cursor',
      '.claude',
      '.swc',
      '.vscode',
      'coverage',
      'node_modules',
      'screenshots',
      'data',
      'dist',
      'build',
      'logs',
      '.vercel',
      'tmp',
      'temp',
    ];

    // Add user-specified exclusions
    if (this.excludeDirs) {
      baseExcludeDirs.push(...this.excludeDirs.split(',').map(d => d.trim()));
    }

    args.push(`--exclude-dir=${baseExcludeDirs.join(',')}`);

    // Base file exclusions
    const baseExcludeExts = [
      'log',
      'png',
      'jpg',
      'jpeg',
      'ico',
      'zip',
      'html',
      'tsbuildinfo',
      'webmanifest',
    ];

    args.push(`--exclude-ext=${baseExcludeExts.join(',')}`);

    // Base file patterns to exclude
    let excludeFilePatterns = [
      '.*\\.md$',
      '_secrets\\.py',
      '\\.env\\..*',
      'npm-debug\\.log.*',
      'yarn-debug\\.log.*',
      'yarn-error\\.log.*',
      '\\.pnpm-debug\\.log.*',
      'package-lock\\.json',
      'yarn\\.lock',
      'pnpm-lock\\.yaml',
      'dev\\.log',
      '.*types.*database\\.ts$',
      'next-env\\.d\\.ts',
    ];

    // Add test exclusions if requested
    if (this.excludeTests) {
      excludeFilePatterns.push(
        '.*\\.test\\.ts$',
        '.*\\.test\\.tsx$',
        '.*\\.test\\.js$',
        '.*\\.test\\.jsx$',
        'jest\\.setup\\.js$',
        '.*\\.spec\\.ts$',
        '.*\\.spec\\.tsx$',
        '.*\\.spec\\.js$',
        '.*\\.spec\\.jsx$'
      );

      const testExcludeDirs = ['__tests__', 'tests', 'test'];
      args.push(`--not-match-d=${testExcludeDirs.join('|')}`);
    }

    // Add user-specified file exclusions
    if (this.excludeFiles) {
      excludeFilePatterns.push(...this.excludeFiles.split(',').map(p => {
        // Escape the pattern for regex if needed
        const trimmed = p.trim();
        // If it's a simple glob pattern like *.md, convert to regex
        if (trimmed.startsWith('*')) {
          return '.*\\' + trimmed.substring(1) + '$';
        }
        return trimmed;
      }));
    }

    args.push(`--not-match-f=${excludeFilePatterns.join('|')}`);

    // Include only specific files if specified
    if (this.includeFiles) {
      const includePatterns = this.includeFiles.split(',').map(p => p.trim()).join('|');
      args.push(`--match-f=${includePatterns}`);
    }

    // Add by-file flag if requested
    if (this.byFile) {
      args.push('--by-file');
    }

    return args;
  }

  private showTestSummary(): void {
    this.context.stdout.write('\n=== SOURCE CODE ONLY (excluding tests) ===\n');

    // Create temp files for separate counts
    const sourceFile = join(tmpdir(), 'cloc_source.txt');
    const testFile = join(tmpdir(), 'cloc_tests.txt');

    try {
      // Count source code (already done above)
      const sourceArgs = this.buildClocCommand();
      const sourceResult = execFileSync('cloc', sourceArgs, { encoding: 'utf8' });
      writeFileSync(sourceFile, sourceResult);

      // Count tests only
      this.context.stdout.write('\n=== TESTS ONLY ===\n');
      const testArgs = [
        '.',
        '--exclude-dir=.git,.next,.cursor,.claude,.swc,.vscode,coverage,node_modules,screenshots,data,dist,build,logs,.vercel,tmp,temp',
        '--match-f=.*\\.(test|spec)\\.(ts|tsx|js|jsx)$|jest\\.setup\\.js$|jest\\.config\\.js$',
      ];

      const testResult = execFileSync('cloc', testArgs, { encoding: 'utf8' });
      writeFileSync(testFile, testResult);
      this.context.stdout.write(testResult);

      // Calculate summary
      this.calculateTestSummary(sourceFile, testFile);

    } catch (error) {
      this.context.stderr.write(`⚠️  Could not generate test summary: ${error.message}\n`);
    } finally {
      // Clean up temp files
      try {
        unlinkSync(sourceFile);
        unlinkSync(testFile);
      } catch {
        // Ignore cleanup errors
      }
    }
  }

  private calculateTestSummary(sourceFile: string, testFile: string): void {
    try {
      const sourceContent = require('fs').readFileSync(sourceFile, 'utf8');
      const testContent = require('fs').readFileSync(testFile, 'utf8');

      const sourceMatch = sourceContent.match(/^SUM:\s+\d+\s+\d+\s+\d+\s+(\d+)$/m);
      const testMatch = testContent.match(/^SUM:\s+\d+\s+\d+\s+\d+\s+(\d+)$/m);

      if (sourceMatch && testMatch) {
        const sourceLines = parseInt(sourceMatch[1]);
        const testLines = parseInt(testMatch[1]);
        const totalLines = sourceLines + testLines;
        const testPercent = ((testLines / totalLines) * 100).toFixed(1);

        this.context.stdout.write('\n=== SUMMARY ===\n');
        this.context.stdout.write(`Source code: ${sourceLines} lines\n`);
        this.context.stdout.write(`Test code: ${testLines} lines\n`);
        this.context.stdout.write(`Total: ${totalLines} lines\n`);
        this.context.stdout.write(`Tests are ${testPercent}% of codebase\n`);
      }
    } catch (error) {
      // Summary calculation failed, but that's not critical
      if (this.verbose) {
        this.context.stderr.write(`Could not calculate summary: ${error.message}\n`);
      }
    }
  }
}

// CLI setup
const cli = new Cli({
  binaryLabel: 'Count Lines Tool',
  binaryName: 'count-lines',
  binaryVersion: '1.0.0',
});

cli.register(CountLinesCommand);
cli.runExit(process.argv.slice(2));