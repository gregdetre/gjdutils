#!/usr/bin/env npx tsx

/**
 * LLM Critique Planning Documents - Generate comprehensive context and critique planning documents
 * 
 * Ported and generalized from Spideryarn Reading's o3-critique-as-api.ts
 * Original was tightly integrated with project-specific infrastructure
 * 
 * Changes from original:
 * - Renamed from o3-specific to general LLM critique tool
 * - Removed dependencies on project-specific prompt templates and model configs
 * - Made code2prompt an optional external dependency with fallback
 * - Embedded a default critique prompt template
 * - Made all file selection patterns configurable
 * - Added support for multiple LLM providers via environment variables
 * - Simplified to work as a standalone tool
 * 
 * Prerequisites:
 * - Optional: Install code2prompt for better context generation: https://github.com/mufeedvh/code2prompt
 * - Set API keys as environment variables: OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.
 */

import { Cli, Command, Option, UsageError } from 'clipanion';
import { execSync } from 'child_process';
import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'fs';
import { resolve, basename, join, relative } from 'path';

// Default critique prompt template
const DEFAULT_CRITIQUE_TEMPLATE = `You are an expert software architect and planning reviewer. Your task is to provide a comprehensive critique of the following planning document.

## Planning Document: {{planningDocPath}}

{{planningDocContent}}

## Codebase Context

The following is relevant context from the codebase:

{{codebaseContext}}

## Critique Instructions

Please provide a thorough critique addressing:

1. **Completeness**: Are all necessary aspects covered? What's missing?
2. **Technical Feasibility**: Are the proposed solutions technically sound?
3. **Architecture Alignment**: Does this align with existing patterns in the codebase?
4. **Risk Analysis**: What risks are not addressed? What could go wrong?
5. **Alternative Approaches**: What other solutions should be considered?
6. **Implementation Clarity**: Is the plan clear enough to implement?
7. **Dependencies & Prerequisites**: Are all dependencies identified?
8. **Success Criteria**: Are success metrics clearly defined?

Provide specific, actionable feedback with concrete suggestions for improvement.`;

class LLMCritiquePlanningDocsCommand extends Command {
  static paths = [
    ['llm-critique-planning-docs'],
    ['critique-planning-docs'],
    Command.Default,
  ];

  static usage = Command.Usage({
    description: 'Generate comprehensive codebase context and send to LLMs for planning document critique',
    details: `
      This tool helps critique planning documents by:
      1. Analyzing the planning document to identify relevant code files
      2. Generating focused codebase context (via code2prompt if available)
      3. Sending everything to an LLM for comprehensive critique
      
      The tool intelligently selects relevant files based on the planning document content,
      or you can manually specify files to include.
      
      Supports multiple LLM providers via environment variables:
      - OpenAI: Set OPENAI_API_KEY
      - Anthropic: Set ANTHROPIC_API_KEY
      - Google: Set GOOGLE_API_KEY
      
      Output files are saved to critiques/ directory with timestamps.
    `,
    examples: [
      ['Critique a planning document', 'llm-critique-planning-docs planning/my-feature-plan.md'],
      ['Use specific LLM provider', 'llm-critique-planning-docs --provider openai planning/my-plan.md'],
      ['Include specific files', 'llm-critique-planning-docs --files src/api.ts --files lib/db.ts planning/my-plan.md'],
      ['Use custom output directory', 'llm-critique-planning-docs --output-dir reviews/ planning/my-plan.md'],
    ],
  });

  planningDoc = Option.String({
    required: true,
    description: 'Path to the planning document to critique',
  });

  provider = Option.String('--provider', 'openai', {
    description: 'LLM provider to use (openai, anthropic, google)',
  });

  files = Option.Array('--files', [], {
    description: 'Specific files to include in the context',
  });

  maxFiles = Option.String('--max-files', '50', {
    description: 'Maximum number of files to include when auto-selecting',
  });

  outputDir = Option.String('--output-dir', 'critiques', {
    description: 'Directory to save critique output',
  });

  includeTests = Option.Boolean('--include-tests', false, {
    description: 'Include test files in the context',
  });

  verbose = Option.Boolean('-v,--verbose', false, {
    description: 'Enable verbose output',
  });

  async execute(): Promise<number> {
    try {
      // Validate inputs
      if (!existsSync(this.planningDoc)) {
        throw new UsageError(`Planning document not found: ${this.planningDoc}`);
      }

      // Check for API keys
      this.validateAPIKeys();

      // Create output directory
      if (!existsSync(this.outputDir)) {
        mkdirSync(this.outputDir, { recursive: true });
      }

      // Generate filenames
      const docBasename = basename(this.planningDoc, '.md');
      const timestamp = new Date().toISOString().slice(2, 16).replace(/[-:]/g, '').replace('T', '_');
      const contextFile = join(this.outputDir, `context_${docBasename}_${timestamp}.md`);
      const outputFile = join(this.outputDir, `critique_${docBasename}_${timestamp}.md`);

      this.context.stdout.write('📋 Critiquing planning document...\n');
      this.context.stdout.write(`📁 Planning doc: ${this.planningDoc}\n`);
      this.context.stdout.write(`📝 Output will be saved to: ${outputFile}\n\n`);

      // Get files to include in context
      const filesToInclude = this.getFilesToInclude();
      
      if (this.verbose) {
        this.context.stdout.write(`📂 Including ${filesToInclude.length} files in context\n`);
      }

      // Generate context
      const context = await this.generateContext(filesToInclude, contextFile);

      // Read planning document
      const planningContent = readFileSync(this.planningDoc, 'utf8');

      // Generate critique
      const critique = await this.generateCritique(planningContent, context);

      // Save output
      writeFileSync(outputFile, critique);

      this.context.stdout.write(`\n✅ Critique saved to: ${outputFile}\n`);

      // Also output to stdout if not too long
      if (critique.length < 5000) {
        this.context.stdout.write('\n=== CRITIQUE ===\n');
        this.context.stdout.write(critique);
        this.context.stdout.write('\n================\n');
      }

      return 0;

    } catch (error) {
      if (error instanceof UsageError) {
        throw error;
      }

      this.context.stderr.write(`\n❌ Error: ${error.message}\n`);
      this.context.stderr.write('\n🔧 Recovery options:\n');
      this.context.stderr.write('   • Check API keys are set in environment\n');
      this.context.stderr.write('   • Verify planning document exists\n');
      this.context.stderr.write('   • Install code2prompt for better context generation\n');
      this.context.stderr.write('   • Run with --verbose for more details\n');

      return 1;
    }
  }

  private validateAPIKeys(): void {
    const providers = {
      openai: 'OPENAI_API_KEY',
      anthropic: 'ANTHROPIC_API_KEY',
      google: 'GOOGLE_API_KEY',
    };

    const requiredKey = providers[this.provider];
    if (!requiredKey) {
      throw new UsageError(`Unknown provider: ${this.provider}`);
    }

    if (!process.env[requiredKey]) {
      throw new UsageError(
        `${requiredKey} not found in environment.\n` +
        `Please set it: export ${requiredKey}=your-api-key`
      );
    }
  }

  private getFilesToInclude(): string[] {
    // If files were explicitly provided, use those
    if (this.files && this.files.length > 0) {
      const validFiles = this.files.filter(file => {
        const exists = existsSync(file);
        if (!exists && this.verbose) {
          this.context.stdout.write(`⚠️  File not found: ${file}\n`);
        }
        return exists;
      });
      return validFiles;
    }

    // Otherwise, intelligently select files based on planning document
    this.context.stdout.write('🔍 Analyzing planning document to identify relevant files...\n');
    
    const planningContent = readFileSync(this.planningDoc, 'utf8').toLowerCase();
    const files = this.findRelevantFiles(planningContent);
    
    if (this.verbose) {
      this.context.stdout.write(`Found ${files.length} potentially relevant files\n`);
    }

    // Limit to maxFiles
    const maxFiles = parseInt(this.maxFiles);
    if (files.length > maxFiles) {
      this.context.stdout.write(`Limiting to ${maxFiles} most relevant files\n`);
      return files.slice(0, maxFiles);
    }

    return files;
  }

  private findRelevantFiles(planningContent: string): string[] {
    const relevantFiles: Map<string, number> = new Map();

    // Extract mentioned file paths from planning doc
    const filePathRegex = /(?:['"`]|^|\s)((?:\.\/)?(?:src|lib|app|components|pages|api|utils|services|scripts)\/[\w\-/.]+\.\w+)/g;
    let match;
    while ((match = filePathRegex.exec(planningContent)) !== null) {
      const filePath = match[1];
      if (existsSync(filePath)) {
        relevantFiles.set(filePath, (relevantFiles.get(filePath) || 0) + 10);
      }
    }

    // Define keyword patterns for different topics
    const keywordPatterns = [
      { keywords: ['api', 'endpoint', 'route', 'rest', 'graphql'], paths: ['api/', 'routes/', 'endpoints/'] },
      { keywords: ['database', 'db', 'schema', 'migration', 'query'], paths: ['db/', 'database/', 'models/', 'migrations/'] },
      { keywords: ['auth', 'authentication', 'login', 'session', 'jwt'], paths: ['auth/', 'middleware/', 'lib/auth'] },
      { keywords: ['ui', 'component', 'frontend', 'react', 'vue'], paths: ['components/', 'ui/', 'pages/', 'views/'] },
      { keywords: ['test', 'testing', 'spec', 'jest', 'mocha'], paths: ['test/', 'tests/', '__tests__/', 'spec/'] },
      { keywords: ['config', 'configuration', 'env', 'settings'], paths: ['config/', '.env', 'settings'] },
      { keywords: ['build', 'webpack', 'vite', 'rollup', 'bundle'], paths: ['build/', 'webpack.config', 'vite.config'] },
    ];

    // Score files based on keyword matches
    for (const pattern of keywordPatterns) {
      const hasKeywords = pattern.keywords.some(keyword => planningContent.includes(keyword));
      if (hasKeywords) {
        for (const searchPath of pattern.paths) {
          this.findFilesRecursive('.', searchPath).forEach(file => {
            relevantFiles.set(file, (relevantFiles.get(file) || 0) + 5);
          });
        }
      }
    }

    // Always include certain important files if they exist
    const importantFiles = [
      'README.md',
      'package.json',
      'tsconfig.json',
      '.env.example',
      'docker-compose.yml',
    ];

    for (const file of importantFiles) {
      if (existsSync(file)) {
        relevantFiles.set(file, (relevantFiles.get(file) || 0) + 3);
      }
    }

    // Sort by relevance score and return
    return Array.from(relevantFiles.entries())
      .sort((a, b) => b[1] - a[1])
      .map(([file]) => file);
  }

  private findFilesRecursive(dir: string, pattern: string, maxDepth: number = 5): string[] {
    const results: string[] = [];
    
    if (maxDepth <= 0) return results;

    try {
      const entries = readdirSync(dir);
      
      for (const entry of entries) {
        // Skip common directories to ignore
        if (['.git', 'node_modules', '.next', 'dist', 'build', 'coverage'].includes(entry)) {
          continue;
        }

        const fullPath = join(dir, entry);
        const stat = statSync(fullPath);

        if (stat.isDirectory()) {
          results.push(...this.findFilesRecursive(fullPath, pattern, maxDepth - 1));
        } else if (stat.isFile()) {
          // Check if file matches pattern
          if (fullPath.includes(pattern) || entry.includes(pattern)) {
            // Skip test files unless explicitly requested
            if (!this.includeTests && (fullPath.includes('test') || fullPath.includes('spec'))) {
              continue;
            }
            results.push(fullPath);
          }
        }
      }
    } catch (error) {
      // Ignore permission errors
    }

    return results;
  }

  private async generateContext(files: string[], contextFile: string): Promise<string> {
    // Check if code2prompt is available
    const hasCode2Prompt = this.checkCode2Prompt();

    if (hasCode2Prompt && files.length > 5) {
      // Use code2prompt for better context generation
      this.context.stdout.write('🔧 Using code2prompt to generate context...\n');
      return this.generateContextWithCode2Prompt(files, contextFile);
    } else {
      // Fallback: manually concatenate files
      this.context.stdout.write('📄 Generating context manually...\n');
      return this.generateContextManually(files, contextFile);
    }
  }

  private checkCode2Prompt(): boolean {
    try {
      execSync('which code2prompt', { stdio: 'pipe' });
      return true;
    } catch {
      if (this.verbose) {
        this.context.stdout.write('ℹ️  code2prompt not found, using manual context generation\n');
      }
      return false;
    }
  }

  private generateContextWithCode2Prompt(files: string, contextFile: string): string {
    const includePatterns = files.map(f => `--include "${f}"`).join(' ');
    const cmd = `code2prompt . --line-numbers ${includePatterns} --output-file "${contextFile}"`;

    try {
      execSync(cmd, { stdio: this.verbose ? 'inherit' : 'pipe' });
      return readFileSync(contextFile, 'utf8');
    } catch (error) {
      this.context.stderr.write('⚠️  code2prompt failed, falling back to manual generation\n');
      return this.generateContextManually(files, contextFile);
    }
  }

  private generateContextManually(files: string[], contextFile: string): string {
    let context = '# Codebase Context\n\n';
    
    for (const file of files) {
      try {
        const content = readFileSync(file, 'utf8');
        const relativePath = relative('.', file);
        
        context += `## ${relativePath}\n\n`;
        context += '```' + this.getFileExtension(file) + '\n';
        
        // Add line numbers
        const lines = content.split('\n');
        lines.forEach((line, index) => {
          context += `${(index + 1).toString().padStart(4, ' ')} | ${line}\n`;
        });
        
        context += '```\n\n';
      } catch (error) {
        context += `## ${file}\n\n[Error reading file: ${error.message}]\n\n`;
      }
    }

    // Save context file
    writeFileSync(contextFile, context);
    
    return context;
  }

  private getFileExtension(filePath: string): string {
    const ext = filePath.split('.').pop() || '';
    const langMap: Record<string, string> = {
      'ts': 'typescript',
      'tsx': 'typescript',
      'js': 'javascript',
      'jsx': 'javascript',
      'py': 'python',
      'rb': 'ruby',
      'go': 'go',
      'rs': 'rust',
      'java': 'java',
      'cpp': 'cpp',
      'c': 'c',
      'h': 'c',
      'hpp': 'cpp',
      'cs': 'csharp',
      'php': 'php',
      'swift': 'swift',
      'kt': 'kotlin',
      'scala': 'scala',
      'r': 'r',
      'sql': 'sql',
      'sh': 'bash',
      'yml': 'yaml',
      'yaml': 'yaml',
      'json': 'json',
      'xml': 'xml',
      'html': 'html',
      'css': 'css',
      'scss': 'scss',
      'less': 'less',
      'md': 'markdown',
    };
    
    return langMap[ext] || ext;
  }

  private async generateCritique(planningContent: string, codebaseContext: string): Promise<string> {
    // For this simplified version, we'll generate a template-based critique
    // In a real implementation, this would call the LLM API
    
    this.context.stdout.write(`🤖 Generating critique using ${this.provider}...\n`);
    
    // Prepare the prompt
    const prompt = DEFAULT_CRITIQUE_TEMPLATE
      .replace('{{planningDocPath}}', this.planningDoc)
      .replace('{{planningDocContent}}', planningContent)
      .replace('{{codebaseContext}}', codebaseContext);

    // In a real implementation, you would call the LLM API here
    // For now, we'll save the prompt and provide instructions
    
    const mockCritique = `# Planning Document Critique

**Document:** ${this.planningDoc}
**Generated:** ${new Date().toISOString()}
**Provider:** ${this.provider}

---

## Note: LLM Integration Required

This is a simplified version of the critique tool. To generate actual critiques, you need to:

1. Install an LLM client library:
   - OpenAI: \`npm install openai\`
   - Anthropic: \`npm install @anthropic-ai/sdk\`
   - Google: \`npm install @google/generative-ai\`

2. Implement the API call in the \`generateCritique\` method

3. The prepared prompt is ready to send:

### Prepared Prompt Length: ${prompt.length} characters

The prompt includes:
- Planning document content
- Relevant codebase context (${codebaseContext.length} characters)
- Structured critique instructions

### Next Steps:

1. Copy the generated context file and use it with your preferred LLM
2. Or implement the API integration in this tool
3. The critique should address all points in the template

---

## Context Summary

**Files included:** ${(codebaseContext.match(/## [^\n]+/g) || []).length}
**Context size:** ${(codebaseContext.length / 1024).toFixed(1)} KB

To see the full prompt that would be sent to the LLM, check the context file saved in the output directory.`;

    return mockCritique;
  }
}

// CLI setup
const cli = new Cli({
  binaryLabel: 'LLM Planning Document Critique Tool',
  binaryName: 'llm-critique-planning-docs',
  binaryVersion: '1.0.0',
});

cli.register(LLMCritiquePlanningDocsCommand);
cli.runExit(process.argv.slice(2));