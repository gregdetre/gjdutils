#!/usr/bin/env npx tsx

/**
 * Sequential DateTime Prefix Generator
 * 
 * Ported from Spideryarn Reading project to gjdutils as a generic utility.
 * Originally from: scripts/generate-sequential-datetime-prefix.ts
 * 
 * Generates sequential datetime prefixes in configurable format (default: yyMMdd[x]_)
 * for organizing files chronologically with letter-based sequence indicators.
 * 
 * This utility scans a directory for existing files matching the date pattern
 * and returns the next available letter in the sequence (a-z).
 * 
 * Example usage:
 *   sequential-datetime-prefix planning/
 *   sequential-datetime-prefix docs/conversations/ --format "yyyy-MM-dd"
 *   sequential-datetime-prefix . --verbose
 * 
 * Note: This file should be made executable with: chmod +x sequential-datetime-prefix.ts
 */

import { Cli, Command, Option, UsageError } from 'clipanion';
import { readdir } from 'fs/promises';
import { resolve } from 'path';

class SequentialDatetimePrefixCommand extends Command {
  static paths = [Command.Default];
  
  static usage = Command.Usage({
    description: 'Generate sequential datetime prefix for file organisation',
    details: `
      Generates a datetime prefix with sequential letter suffix for organising files chronologically.
      Scans the specified folder for existing files and returns the next letter in sequence.
      
      The default format is yyMMdd[x]_ where [x] is a sequential letter (a-z).
      You can customise the date format using the --format option.
      
      This tool is useful for:
      - Planning documents
      - Conversation transcripts
      - Any chronologically organised files
    `,
    examples: [
      ['Generate prefix for current directory', 'sequential-datetime-prefix .'],
      ['Planning folder with default format', 'sequential-datetime-prefix planning/'],
      ['Custom date format', 'sequential-datetime-prefix docs/ --format "yyyy-MM-dd"'],
      ['Verbose output', 'sequential-datetime-prefix . --verbose'],
    ],
  });

  folderPath = Option.String({ required: true });
  verbose = Option.Boolean('-v,--verbose', false, {
    description: 'Show detailed scanning information',
  });
  format = Option.String('--format', 'yyMMdd', {
    description: 'Date format pattern (default: yyMMdd)',
  });

  async execute(): Promise<number> {
    try {
      const targetFolder = resolve(this.folderPath);
      const datePrefix = this.getCurrentDatePrefix();
      
      if (this.verbose) {
        this.context.stdout.write(`Scanning ${targetFolder} for ${datePrefix}*\n`);
        this.context.stdout.write(`Using date format: ${this.format}\n`);
      }

      const files = await readdir(targetFolder).catch(err => {
        if (err.code === 'ENOENT') {
          throw new UsageError(`Folder not found: ${targetFolder}`);
        }
        throw err;
      });

      const pattern = new RegExp(`^${this.escapeRegExp(datePrefix)}([a-z])_`);
      const usedLetters = new Set(
        files
          .map(file => file.match(pattern)?.[1])
          .filter(Boolean)
      );

      if (this.verbose && usedLetters.size > 0) {
        this.context.stdout.write(`Found existing prefixes: ${Array.from(usedLetters).sort().join(', ')}\n`);
      }

      const nextLetter = 'abcdefghijklmnopqrstuvwxyz'
        .split('')
        .find(letter => !usedLetters.has(letter)) || 'a';

      const result = `${datePrefix}${nextLetter}_`;
      this.context.stdout.write(`${result}\n`);
      
      if (this.verbose) {
        this.context.stdout.write(`\nNext available prefix: ${result}\n`);
      }
      
      return 0;
    } catch (error) {
      if (error instanceof UsageError) throw error;
      throw new UsageError(`Error: ${error instanceof Error ? error.message : String(error)}`);
    }
  }

  private getCurrentDatePrefix(): string {
    const now = new Date();
    
    // Map common format patterns to implementation
    switch (this.format) {
      case 'yyMMdd':
        return this.formatYYMMDD(now);
      case 'yyyyMMdd':
        return this.formatYYYYMMDD(now);
      case 'yyyy-MM-dd':
        return this.formatYYYYDashMMDashDD(now);
      case 'yy-MM-dd':
        return this.formatYYDashMMDashDD(now);
      default:
        // For custom formats, fall back to the provided format as-is
        // In a more complete implementation, this could use a date formatting library
        this.context.stderr.write(`Warning: Custom format '${this.format}' used as-is. Consider using standard formats.\n`);
        return this.format;
    }
  }

  private formatYYMMDD(date: Date): string {
    const year = date.getFullYear().toString().slice(-2);
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}${month}${day}`;
  }

  private formatYYYYMMDD(date: Date): string {
    const year = date.getFullYear().toString();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}${month}${day}`;
  }

  private formatYYYYDashMMDashDD(date: Date): string {
    const year = date.getFullYear().toString();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  private formatYYDashMMDashDD(date: Date): string {
    const year = date.getFullYear().toString().slice(-2);
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  private escapeRegExp(string: string): string {
    return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }
}

const cli = new Cli({
  binaryName: 'sequential-datetime-prefix',
  binaryLabel: 'Sequential DateTime Prefix Generator',
  binaryVersion: '1.0.0',
});

cli.register(SequentialDatetimePrefixCommand);
cli.runExit(process.argv.slice(2));