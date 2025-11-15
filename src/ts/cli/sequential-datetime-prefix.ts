#!/usr/bin/env -S npx -y -p tsx@^4 tsx

/**
 * Sequential DateTime Prefix Generator (zero-dependency CLI)
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
 *   sequential-datetime-prefix docs/planning --also docs/planning/finished --also docs/planning/later
 *   sequential-datetime-prefix docs/planning --format "yyyy-MM-dd" --also docs/planning/finished --also docs/planning/later --verbose
 *
 * Note: Make executable with: chmod +x sequential-datetime-prefix.ts
 */

// from https://github.com/gregdetre/gjdutils/blob/main/src/ts/cli/sequential-datetime-prefix.ts

import { readdir, mkdir } from 'fs/promises';
import { resolve, basename } from 'path';

type ParsedArgs = {
  folderPath?: string;
  verbose: boolean;
  format: string;
  alsoDirs: string[];
};

function parseArgs(argv: string[]): ParsedArgs {
  const parsed: ParsedArgs = { verbose: false, format: 'yyMMdd', alsoDirs: [] };
  let i = 0;
  while (i < argv.length) {
    const token = argv[i];
    if (token === '-v' || token === '--verbose') {
      parsed.verbose = true;
      i += 1;
      continue;
    }
    if (token === '--also' || token.startsWith('--also=')) {
      let value: string | undefined;
      if (token.includes('=')) {
        const [, v] = token.split('=');
        value = v;
      } else {
        value = argv[i + 1];
        if (!value) {
          throw new Error(
            'Missing folder path for --also option.\n' +
            'Usage: --also <folder-path>'
          );
        }
        i += 1; // consume value below via common increment
      }
      parsed.alsoDirs.push(value);
      i += 1;
      continue;
    }
    if (token.startsWith('--format')) {
      const [flag, valueMaybe] = token.split('=');
      if (valueMaybe) {
        parsed.format = valueMaybe;
        i += 1;
        continue;
      }
      const next = argv[i + 1];
      if (!next) {
        throw new Error(
          'Missing format value for --format option.\n' +
          'Available formats: yyMMdd, yyyyMMdd, yyyy-MM-dd, yy-MM-dd\n' +
          'Example: --format "yyyy-MM-dd"'
        );
      }
      parsed.format = next;
      i += 2;
      continue;
    }
    if (token.startsWith('-')) {
      throw new Error(
        `Unknown option: ${token}\n\n` +
        'Valid options:\n' +
        '  --format <pattern>    Date format (default: yyMMdd)\n' +
        '  --also <dir>          Additional directory to scan\n' +
        '  -v, --verbose         Show detailed output\n\n' +
        'Run without arguments to see full usage help.'
      );
    }
    if (!parsed.folderPath) {
      parsed.folderPath = token;
      i += 1;
      continue;
    }
    // Extra positional arguments are ignored
    i += 1;
  }
  return parsed;
}

async function generatePrefix(folderPath: string, format: string, verbose: boolean, alsoDirs: string[]): Promise<string> {
  const targetFolder = resolve(folderPath);
  const datePrefix = getCurrentDatePrefix(format);

  if (verbose) {
    process.stdout.write(`Scanning ${targetFolder} for ${datePrefix}*\n`);
    process.stdout.write(`Using date format: ${format}\n`);
    if (alsoDirs.length > 0) {
      const resolvedAlso = alsoDirs.map(d => resolve(d));
      process.stdout.write(`Also scanning: ${resolvedAlso.join(', ')}\n`);
    }
  }

  let files: string[];
  try {
    files = await readdir(targetFolder);
  } catch (err: any) {
    if (err && err.code === 'ENOENT') {
      // Auto-create the directory
      try {
        await mkdir(targetFolder, { recursive: true });
        if (verbose) {
          process.stdout.write(`Created directory: ${targetFolder}\n`);
        }
        files = []; // Empty directory, no existing files
      } catch (createErr: any) {
        throw new Error(
          `Could not create folder "${basename(targetFolder)}".\n` +
          `Please check that you have permission to create folders in this location:\n` +
          `  ${targetFolder}`
        );
      }
    } else if (err && err.code === 'EACCES') {
      throw new Error(
        `Permission denied: Cannot access folder "${basename(targetFolder)}".\n` +
        `Please check that you have permission to read this folder:\n` +
        `  ${targetFolder}`
      );
    } else {
      throw new Error(
        `Failed to access folder "${basename(targetFolder)}".\n` +
        `Error: ${err.message || String(err)}\n` +
        `Path: ${targetFolder}`
      );
    }
  }

  // Read additional directories and collect their files
  for (const dir of alsoDirs) {
    const abs = resolve(dir);
    try {
      const extra = await readdir(abs);
      files.push(...extra);
    } catch (err: any) {
      if (err && err.code === 'ENOENT') {
        // Auto-create additional directories as well
        try {
          await mkdir(abs, { recursive: true });
          if (verbose) {
            process.stdout.write(`Created additional directory: ${abs}\n`);
          }
          // Empty directory, no files to add
        } catch (createErr: any) {
          if (verbose) {
            process.stderr.write(
              `Warning: Could not create additional folder "${basename(abs)}".\n` +
              `  Path: ${abs}\n`
            );
          }
        }
        continue;
      } else if (err && err.code === 'EACCES') {
        if (verbose) {
          process.stderr.write(
            `Warning: Permission denied for additional folder "${basename(abs)}".\n` +
            `  Path: ${abs}\n`
          );
        }
        continue;
      } else {
        if (verbose) {
          process.stderr.write(
            `Warning: Failed to access additional folder "${basename(abs)}": ${err.message}\n`
          );
        }
        continue;
      }
    }
  }

  const pattern = new RegExp(`^${escapeRegExp(datePrefix)}([a-z])_`);
  const usedLetters = new Set(
    files
      .map(file => file.match(pattern)?.[1])
      .filter(Boolean) as string[]
  );

  if (verbose && usedLetters.size > 0) {
    process.stdout.write(`Found existing prefixes: ${Array.from(usedLetters).sort().join(', ')}\n`);
  }

  const nextLetter = 'abcdefghijklmnopqrstuvwxyz'
    .split('')
    .find(letter => !usedLetters.has(letter));

  if (!nextLetter) {
    throw new Error(
      `No available prefixes for today (${datePrefix}).\n` +
      `All letters a-z have been used. Consider:\n` +
      `  1. Using a different date format with --format\n` +
      `  2. Moving some files to an archive folder\n` +
      `  3. Waiting until tomorrow to create more files`
    );
  }

  const result = `${datePrefix}${nextLetter}_`;
  if (verbose) {
    process.stdout.write(`\nNext available prefix: ${result}\n`);
  }
  return result;
}

function getCurrentDatePrefix(format: string): string {
  const now = new Date();
  switch (format) {
    case 'yyMMdd':
      return formatYYMMDD(now);
    case 'yyyyMMdd':
      return formatYYYYMMDD(now);
    case 'yyyy-MM-dd':
      return formatYYYYDashMMDashDD(now);
    case 'yy-MM-dd':
      return formatYYDashMMDashDD(now);
    default:
      process.stderr.write(`Warning: Custom format '${format}' used as-is. Consider using standard formats.\n`);
      return format;
  }
}

function formatYYMMDD(date: Date): string {
  const year = date.getFullYear().toString().slice(-2);
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${year}${month}${day}`;
}

function formatYYYYMMDD(date: Date): string {
  const year = date.getFullYear().toString();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${year}${month}${day}`;
}

function formatYYYYDashMMDashDD(date: Date): string {
  const year = date.getFullYear().toString();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function formatYYDashMMDashDD(date: Date): string {
  const year = date.getFullYear().toString().slice(-2);
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
}

function escapeRegExp(input: string): string {
  return input.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

async function main(): Promise<void> {
  try {
    const { folderPath, verbose, format, alsoDirs } = parseArgs(process.argv.slice(2));
    if (!folderPath) {
      process.stderr.write(
        '\nSequential DateTime Prefix Generator\n' +
        '====================================\n\n' +
        'Usage:\n' +
        '  sequential-datetime-prefix <folder> [options]\n\n' +
        'Options:\n' +
        '  --format <pattern>    Date format (default: yyMMdd)\n' +
        '                        Available: yyMMdd, yyyyMMdd, yyyy-MM-dd, yy-MM-dd\n' +
        '  --also <dir>          Additional directory to scan for conflicts\n' +
        '  -v, --verbose         Show detailed output\n\n' +
        'Examples:\n' +
        '  sequential-datetime-prefix planning/\n' +
        '  sequential-datetime-prefix docs/conversations/ --format "yyyy-MM-dd"\n' +
        '  sequential-datetime-prefix . --verbose\n' +
        '  sequential-datetime-prefix docs/planning --also docs/planning/archive\n\n' +
        'This tool generates sequential prefixes like "251015a_", "251015b_", etc.\n' +
        'for organizing files chronologically.\n'
      );
      process.exitCode = 1;
      return;
    }
    const result = await generatePrefix(folderPath, format, verbose, alsoDirs);
    process.stdout.write(`${result}\n`);
  } catch (err: any) {
    const errorMessage = err instanceof Error ? err.message : String(err);
    process.stderr.write(`\n❌ Error: ${errorMessage}\n\n`);
    process.exitCode = 1;
  }
}

main();