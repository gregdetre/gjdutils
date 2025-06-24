#!/usr/bin/env npx tsx

/**
 * Parse LLM Output - Extract and format LLM responses from various output formats
 * 
 * Ported and generalized from Spideryarn Reading's parse-critique-output.ts
 * Original was specific to OpenAI o3 critique output; this version supports multiple formats
 * 
 * Changes from original:
 * - Renamed from parse-critique to parse-llm-output for broader applicability
 * - Added support for multiple LLM output formats (OpenAI, Anthropic, raw JSON)
 * - Made output extraction more flexible with configurable strategies
 * - Added format auto-detection capability
 * - Removed project-specific references
 */

import { Cli, Command, Option, UsageError } from 'clipanion';
import { readFileSync } from 'fs';

interface ParseStrategy {
  name: string;
  canParse: (input: string) => boolean;
  extract: (input: string) => string | null;
}

class ParseLLMOutputCommand extends Command {
  static paths = [['parse-llm-output'], Command.Default];
  
  static usage = Command.Usage({
    description: 'Parse LLM output from various formats and extract the main response',
    details: `
      This script parses output from different LLM APIs and tools, extracting
      the main response content and formatting it for readable display.
      
      Supported formats:
      - OpenAI API responses (including o3 model outputs)
      - Anthropic API responses
      - JSON Lines format
      - Raw JSON format
      
      The script automatically detects the format and extracts the appropriate content.
    `,
    examples: [
      ['Parse from file', 'parse-llm-output output.json'],
      ['Parse from stdin', 'cat output.json | parse-llm-output'],
      ['Force specific format', 'parse-llm-output --format openai output.json'],
      ['Extract specific field', 'parse-llm-output --field choices[0].message.content output.json'],
    ],
  });

  inputFile = Option.String({
    description: 'Input file containing the LLM output (or stdin if not provided)',
    required: false,
  });

  format = Option.String('--format', {
    description: 'Force specific format parsing (auto-detects if not specified)',
    required: false,
  });

  field = Option.String('--field', {
    description: 'Specific field path to extract (e.g., "choices[0].message.content")',
    required: false,
  });

  verbose = Option.Boolean('-v,--verbose', false, {
    description: 'Show verbose parsing information',
  });

  async execute(): Promise<number> {
    try {
      let input: string;
      
      if (this.inputFile) {
        // Read from file
        try {
          input = readFileSync(this.inputFile, 'utf8');
        } catch (error) {
          throw new UsageError(`Could not read file: ${this.inputFile}`);
        }
      } else {
        // Read from stdin
        input = '';
        process.stdin.setEncoding('utf8');
        
        for await (const chunk of process.stdin) {
          input += chunk;
        }
        
        if (!input.trim()) {
          throw new UsageError('No input provided. Use a file argument or pipe input to stdin.');
        }
      }

      const content = this.extractContent(input);
      
      if (!content) {
        this.context.stderr.write('❌ No content found in the input\n');
        if (this.verbose) {
          this.context.stderr.write('Input preview:\n');
          this.context.stderr.write(input.substring(0, 500) + '...\n');
        }
        return 1;
      }

      // Output the formatted content
      this.context.stdout.write(content + '\n');
      return 0;

    } catch (error) {
      if (error instanceof UsageError) {
        throw error;
      }
      
      this.context.stderr.write(`❌ Error parsing output: ${error.message}\n`);
      return 1;
    }
  }

  private extractContent(input: string): string | null {
    // If a specific field is requested, try to extract it
    if (this.field) {
      return this.extractFieldPath(input, this.field);
    }

    // Define parsing strategies
    const strategies: ParseStrategy[] = [
      // OpenAI format (including o3)
      {
        name: 'openai',
        canParse: (input) => input.includes('"choices"') || input.includes('"type":"message"'),
        extract: this.extractOpenAIFormat.bind(this),
      },
      // Anthropic format
      {
        name: 'anthropic',
        canParse: (input) => input.includes('"content"') && input.includes('"role":"assistant"'),
        extract: this.extractAnthropicFormat.bind(this),
      },
      // JSON Lines format (generic)
      {
        name: 'jsonlines',
        canParse: (input) => {
          const lines = input.trim().split('\n');
          return lines.length > 1 && lines.every(line => {
            try {
              JSON.parse(line);
              return true;
            } catch {
              return false;
            }
          });
        },
        extract: this.extractJSONLinesFormat.bind(this),
      },
      // Raw JSON format
      {
        name: 'json',
        canParse: (input) => {
          try {
            JSON.parse(input);
            return true;
          } catch {
            return false;
          }
        },
        extract: this.extractRawJSONFormat.bind(this),
      },
    ];

    // If format is specified, use only that strategy
    if (this.format) {
      const strategy = strategies.find(s => s.name === this.format);
      if (!strategy) {
        throw new UsageError(`Unknown format: ${this.format}. Available formats: ${strategies.map(s => s.name).join(', ')}`);
      }
      if (this.verbose) {
        this.context.stderr.write(`Using forced format: ${this.format}\n`);
      }
      return strategy.extract(input);
    }

    // Auto-detect format
    for (const strategy of strategies) {
      if (strategy.canParse(input)) {
        if (this.verbose) {
          this.context.stderr.write(`Detected format: ${strategy.name}\n`);
        }
        const result = strategy.extract(input);
        if (result) {
          return result;
        }
      }
    }

    return null;
  }

  private extractFieldPath(input: string, fieldPath: string): string | null {
    try {
      const data = JSON.parse(input);
      // Simple field path extraction (supports dot notation and array indices)
      const parts = fieldPath.split(/[.\[\]]/).filter(p => p);
      let current = data;
      
      for (const part of parts) {
        if (current === null || current === undefined) {
          return null;
        }
        current = current[part];
      }
      
      return typeof current === 'string' ? current : JSON.stringify(current, null, 2);
    } catch (error) {
      if (this.verbose) {
        this.context.stderr.write(`Failed to extract field path: ${error.message}\n`);
      }
      return null;
    }
  }

  private extractOpenAIFormat(input: string): string | null {
    // Handle JSON Lines format (like o3 output)
    const lines = input.trim().split('\n');
    
    for (const line of lines) {
      if (!line.trim()) continue;
      
      try {
        const parsed = JSON.parse(line);
        
        // Look for the final message with content
        if (parsed.type === 'message' && 
            parsed.content && 
            Array.isArray(parsed.content) &&
            parsed.content.length > 0) {
          
          const textContent = parsed.content.find((item: any) => item.type === 'output_text');
          if (textContent && textContent.text) {
            return textContent.text;
          }
        }
        
        // Standard OpenAI completion format
        if (parsed.choices && Array.isArray(parsed.choices) && parsed.choices.length > 0) {
          const firstChoice = parsed.choices[0];
          if (firstChoice.message && firstChoice.message.content) {
            return firstChoice.message.content;
          }
          if (firstChoice.text) {
            return firstChoice.text;
          }
        }
      } catch (e) {
        // Not valid JSON, skip this line
        continue;
      }
    }
    
    // Try parsing as single JSON object
    try {
      const parsed = JSON.parse(input);
      if (parsed.choices && Array.isArray(parsed.choices) && parsed.choices.length > 0) {
        const firstChoice = parsed.choices[0];
        if (firstChoice.message && firstChoice.message.content) {
          return firstChoice.message.content;
        }
        if (firstChoice.text) {
          return firstChoice.text;
        }
      }
    } catch {
      // Not valid JSON
    }
    
    return null;
  }

  private extractAnthropicFormat(input: string): string | null {
    try {
      const parsed = JSON.parse(input);
      
      // Anthropic message format
      if (parsed.content) {
        if (typeof parsed.content === 'string') {
          return parsed.content;
        }
        if (Array.isArray(parsed.content)) {
          // Extract text from content blocks
          const textBlocks = parsed.content
            .filter((block: any) => block.type === 'text')
            .map((block: any) => block.text)
            .join('\n\n');
          if (textBlocks) {
            return textBlocks;
          }
        }
      }
      
      // Anthropic completion format
      if (parsed.completion) {
        return parsed.completion;
      }
    } catch {
      // Not valid JSON
    }
    
    return null;
  }

  private extractJSONLinesFormat(input: string): string | null {
    const lines = input.trim().split('\n');
    const messages: string[] = [];
    
    for (const line of lines) {
      if (!line.trim()) continue;
      
      try {
        const parsed = JSON.parse(line);
        
        // Look for any text-like content
        const possibleFields = ['text', 'content', 'message', 'output', 'response'];
        for (const field of possibleFields) {
          if (parsed[field] && typeof parsed[field] === 'string') {
            messages.push(parsed[field]);
            break;
          }
        }
      } catch {
        // Skip invalid JSON lines
      }
    }
    
    return messages.length > 0 ? messages.join('\n\n') : null;
  }

  private extractRawJSONFormat(input: string): string | null {
    try {
      const parsed = JSON.parse(input);
      
      // Common fields to check
      const possibleFields = ['text', 'content', 'message', 'output', 'response', 'result'];
      
      for (const field of possibleFields) {
        if (parsed[field] && typeof parsed[field] === 'string') {
          return parsed[field];
        }
      }
      
      // If it's a simple string
      if (typeof parsed === 'string') {
        return parsed;
      }
      
      // Return formatted JSON if no specific field found
      return JSON.stringify(parsed, null, 2);
    } catch {
      return null;
    }
  }
}

// CLI setup
const cli = new Cli({
  binaryLabel: 'Parse LLM Output',
  binaryName: 'parse-llm-output',
  binaryVersion: '1.0.0',
});

cli.register(ParseLLMOutputCommand);
cli.runExit(process.argv.slice(2));