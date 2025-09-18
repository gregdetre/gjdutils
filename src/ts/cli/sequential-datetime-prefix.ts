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

import { readdir } from 'fs/promises';
import { resolve } from 'path';

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
          throw new Error("Missing value for --also");
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
        throw new Error("Missing value for --format");
      }
      parsed.format = next;
      i += 2;
      continue;
    }
    if (token.startsWith('-')) {
      throw new Error(`Unknown option: ${token}`);
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
      throw new Error(`Folder not found: ${targetFolder}`);
    }
    throw err;
  }

  // Read additional directories and collect their files
  for (const dir of alsoDirs) {
    const abs = resolve(dir);
    try {
      const extra = await readdir(abs);
      files.push(...extra);
    } catch (err: any) {
      if (err && err.code === 'ENOENT') {
        if (verbose) process.stderr.write(`Warning: Also-scan folder not found: ${abs}\n`);
        continue;
      }
      throw err;
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
    .find(letter => !usedLetters.has(letter)) || 'a';

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
      process.stderr.write('Usage: sequential-datetime-prefix <folder> [--format <pattern>] [--also <dir>]... [-v|--verbose]\n');
      process.exitCode = 1;
      return;
    }
    const result = await generatePrefix(folderPath, format, verbose, alsoDirs);
    process.stdout.write(`${result}\n`);
  } catch (err: any) {
    process.stderr.write(`Error: ${err instanceof Error ? err.message : String(err)}\n`);
    process.exitCode = 1;
  }
}

main();