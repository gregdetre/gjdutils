#!/usr/bin/env npx tsx

/**
 * LLM Conversation Extractor
 * 
 * Ported and generalised from Spideryarn Reading project to gjdutils.
 * Originally from: scripts/extract-claude-conversation.ts
 * 
 * Extracts conversations from LLM export files (currently supports Claude.ai JSON format)
 * and converts them to structured markdown for documentation and analysis.
 * 
 * This utility is designed to be extensible to support multiple LLM formats in the future,
 * including ChatGPT, Gemini, and other conversational AI platforms.
 * 
 * Features:
 * - Extracts conversation messages and metadata
 * - Identifies and extracts code artifacts/snippets as appendices
 * - Generates structured markdown with proper formatting
 * - Supports batch extraction of multiple conversations
 * - Configurable output format and directory
 * 
 * Example usage:
 *   extract-llm-conversation --uuid abc123 --input conversations.json
 *   extract-llm-conversation --uuid uuid1,uuid2 --input export.json --output docs/
 *   extract-llm-conversation --uuid abc123 --input claude.json --format claude --verbose
 * 
 * Note: This file should be made executable with: chmod +x extract-llm-conversation.ts
 */

import { Cli, Command, Option, UsageError } from 'clipanion';
import { readFile, writeFile, mkdir, readdir } from 'fs/promises';
import { resolve } from 'path';

// Generic LLM conversation interfaces
interface LLMMessage {
  id: string;
  text: string;
  sender: 'human' | 'assistant' | 'system';
  created_at: string;
  updated_at?: string;
  metadata?: Record<string, any>;
}

interface LLMConversation {
  id: string;
  title: string;
  created_at: string;
  updated_at: string;
  messages: LLMMessage[];
  metadata?: Record<string, any>;
}

interface LLMArtifact {
  identifier: string;
  type: string;
  language?: string;
  title: string;
  content: string;
}

interface ConversationExport {
  conversation: LLMConversation;
  artifacts: LLMArtifact[];
  format: string;
}

// Claude-specific interfaces for parsing
interface ClaudeMessage {
  uuid: string;
  text: string;
  content: Array<{
    type: string;
    text?: string;
    thinking?: string;
    summaries?: Array<{ summary: string }>;
    name?: string;
    input?: any;
    content?: any;
    display_content?: any;
  }>;
  sender: 'human' | 'assistant';
  created_at: string;
  updated_at: string;
}

interface ClaudeConversation {
  uuid: string;
  name: string;
  created_at: string;
  updated_at: string;
  chat_messages: ClaudeMessage[];
}

class ExtractLLMConversationCommand extends Command {
  static paths = [['extract-llm-conversation'], Command.Default];
  
  static usage = Command.Usage({
    description: 'Extract LLM conversations from export files to structured markdown',
    details: `
      Extracts specific conversations from LLM export files and converts them
      to structured markdown for documentation and analysis.
      
      Currently supports:
      - Claude.ai JSON export format
      
      Future support planned for:
      - ChatGPT conversation exports
      - Google Gemini exports
      - Other conversational AI platforms
      
      The tool will:
      - Parse the export file based on detected or specified format
      - Extract conversation messages and metadata
      - Identify and extract any code artifacts as appendices
      - Generate structured markdown with proper formatting
      - Support batch extraction of multiple conversations
      
      Output files are automatically named using the yyMMdd[letter]_description format
      and saved to the specified output directory.
    `,
    examples: [
      ['Extract single conversation', 'extract-llm-conversation --id abc123 --input conversations.json'],
      ['Extract multiple conversations', 'extract-llm-conversation --id id1,id2 --input export.json --output docs/'],
      ['Specify format explicitly', 'extract-llm-conversation --id abc123 --input data.json --format claude'],
      ['Extract with verbose output', 'extract-llm-conversation --id abc123 --input export.json --verbose'],
    ],
  });

  // Define options
  inputFile = Option.String('--input', {
    description: 'Path to LLM export file',
    required: true,
  });

  conversationIds = Option.String('--id,--uuid', {
    description: 'Conversation ID(s) to extract (comma-separated for multiple)',
    required: true,
  });

  outputDir = Option.String('--output', 'docs/conversations', {
    description: 'Output directory for generated markdown files',
  });

  format = Option.String('--format', 'auto', {
    description: 'Export format (auto, claude, chatgpt, gemini)',
  });

  verbose = Option.Boolean('-v,--verbose', false, {
    description: 'Enable verbose output',
  });

  includeMetadata = Option.Boolean('--metadata', true, {
    description: 'Include conversation metadata in output',
  });

  async execute(): Promise<number> {
    try {
      // Validate input file exists
      const inputPath = resolve(this.inputFile);
      const outputPath = resolve(this.outputDir);

      if (this.verbose) {
        this.context.stdout.write(`📂 Reading from: ${inputPath}\n`);
        this.context.stdout.write(`📝 Writing to: ${outputPath}\n`);
        this.context.stdout.write(`📋 Format: ${this.format}\n`);
      }

      // Read the export file
      const fileContent = await readFile(inputPath, 'utf-8');
      
      // Detect or use specified format
      const detectedFormat = this.format === 'auto' 
        ? this.detectFormat(fileContent) 
        : this.format;

      if (this.verbose) {
        this.context.stdout.write(`🔍 Using format: ${detectedFormat}\n`);
      }

      // Parse conversations based on format
      const conversations = this.parseExport(fileContent, detectedFormat);

      // Parse IDs
      const targetIds = this.conversationIds.split(',').map(id => id.trim());

      // Ensure output directory exists
      await mkdir(outputPath, { recursive: true });

      let extractedCount = 0;

      for (const id of targetIds) {
        const exported = this.findAndExtractConversation(conversations, id, detectedFormat);
        
        if (!exported) {
          this.context.stderr.write(`⚠️  Conversation with ID ${id} not found\n`);
          continue;
        }

        if (this.verbose) {
          const msgCount = exported.conversation.messages.length;
          this.context.stdout.write(`🔍 Processing: "${exported.conversation.title}" (${msgCount} messages)\n`);
        }

        // Generate markdown
        const markdown = this.generateMarkdown(exported);
        
        // Generate filename
        const filename = await this.generateFilename(exported.conversation.title, outputPath);
        const outputFile = resolve(outputPath, `${filename}.md`);
        
        // Write file
        await writeFile(outputFile, markdown, 'utf-8');
        
        this.context.stdout.write(`✅ Extracted: ${outputFile}\n`);
        extractedCount++;
      }

      if (extractedCount === 0) {
        this.context.stderr.write(`❌ No conversations were extracted\n`);
        return 1;
      }

      this.context.stdout.write(`\n🎉 Successfully extracted ${extractedCount} conversation(s)\n`);
      return 0;

    } catch (error) {
      if (error instanceof Error) {
        this.context.stderr.write(`❌ Error: ${error.message}\n`);
        
        if (this.verbose) {
          this.context.stderr.write(`Stack trace: ${error.stack}\n`);
        }
        
        // Provide recovery suggestions
        this.context.stderr.write('\n🔧 Recovery options:\n');
        this.context.stderr.write('   • Check file permissions and path\n');
        this.context.stderr.write('   • Verify export format is supported\n');
        this.context.stderr.write('   • Ensure conversation IDs exist in the export\n');
        this.context.stderr.write('   • Try with --verbose for detailed error information\n');
        this.context.stderr.write('   • Use --format to specify format explicitly\n');
      }
      return 1;
    }
  }

  private detectFormat(content: string): string {
    try {
      const parsed = JSON.parse(content);
      
      // Claude detection: array of conversations with chat_messages field
      if (Array.isArray(parsed) && parsed.length > 0 && 'chat_messages' in parsed[0]) {
        return 'claude';
      }
      
      // Add more format detection logic here as needed
      // ChatGPT detection: look for specific fields
      // Gemini detection: look for specific structure
      
      return 'unknown';
    } catch {
      return 'unknown';
    }
  }

  private parseExport(content: string, format: string): any[] {
    switch (format) {
      case 'claude':
        return JSON.parse(content) as ClaudeConversation[];
      
      // Add more format parsers here
      case 'chatgpt':
        throw new UsageError('ChatGPT format not yet implemented');
      
      case 'gemini':
        throw new UsageError('Gemini format not yet implemented');
      
      default:
        throw new UsageError(`Unsupported format: ${format}`);
    }
  }

  private findAndExtractConversation(
    conversations: any[], 
    id: string, 
    format: string
  ): ConversationExport | null {
    switch (format) {
      case 'claude':
        return this.extractClaudeConversation(conversations as ClaudeConversation[], id);
      
      // Add more format extractors here
      default:
        return null;
    }
  }

  private extractClaudeConversation(
    conversations: ClaudeConversation[], 
    id: string
  ): ConversationExport | null {
    const conversation = conversations.find(conv => conv.uuid === id);
    
    if (!conversation) {
      return null;
    }

    // Convert Claude format to generic format
    const genericConversation: LLMConversation = {
      id: conversation.uuid,
      title: conversation.name,
      created_at: conversation.created_at,
      updated_at: conversation.updated_at,
      messages: conversation.chat_messages.map(msg => ({
        id: msg.uuid,
        text: this.extractClaudeMessageText(msg),
        sender: msg.sender,
        created_at: msg.created_at,
        updated_at: msg.updated_at,
        metadata: { content: msg.content },
      })),
    };

    // Extract artifacts
    const artifacts = this.extractClaudeArtifacts(conversation);

    return {
      conversation: genericConversation,
      artifacts,
      format: 'claude',
    };
  }

  private extractClaudeMessageText(message: ClaudeMessage): string {
    // Check if the text field has actual content
    if (message.text && !message.text.includes('This block is not supported') && message.text.trim()) {
      return message.text;
    }
    
    // Extract from content array
    const textParts: string[] = [];
    
    for (const item of message.content || []) {
      if (item.type === 'text' && item.text && item.text.trim()) {
        textParts.push(item.text);
      } else if (item.type === 'thinking' && item.thinking && item.thinking.trim()) {
        textParts.push(item.thinking);
      }
    }
    
    return textParts.join('\n\n');
  }

  private extractClaudeArtifacts(conversation: ClaudeConversation): LLMArtifact[] {
    const artifacts: LLMArtifact[] = [];
    
    for (const message of conversation.chat_messages) {
      if (message.sender === 'assistant' && message.text) {
        const artifactMatches = message.text.matchAll(
          /<antArtifact identifier="([^"]+)" type="([^"]+)"(?:\s+language="([^"]+)")?\s+title="([^"]+)">([\s\S]*?)<\/antArtifact>/g
        );
        
        for (const match of artifactMatches) {
          artifacts.push({
            identifier: match[1],
            type: match[2],
            language: match[3] || undefined,
            title: match[4],
            content: match[5].trim(),
          });
        }
      }
    }

    return artifacts;
  }

  private generateMarkdown(data: ConversationExport): string {
    const { conversation, artifacts, format } = data;
    const startDate = new Date(conversation.created_at);
    const conversationDate = startDate.toLocaleDateString('en-GB', {
      year: 'numeric',
      month: 'long', 
      day: 'numeric'
    });
    const conversationDateTime = startDate.toLocaleString('en-GB', {
      year: 'numeric',
      month: 'long', 
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZoneName: 'short'
    });

    const platformUrl = this.getPlatformUrl(conversation.id, format);
    const commandLineArgs = `--id ${conversation.id} --input ${this.inputFile}`;
    
    let markdown = `---
Date: ${conversationDateTime}
Duration: ${this.estimateDuration(conversation)}
Type: LLM Conversation
Platform: ${this.formatPlatformName(format)}
Status: Extracted
`;

    if (platformUrl) {
      markdown += `URL: ${platformUrl}\n`;
    }

    if (this.includeMetadata) {
      markdown += `Extracted by: extract-llm-conversation ${commandLineArgs}
Source file: ${this.inputFile}
`;
    }

    markdown += `Related Docs: []
---

# ${conversation.title} - ${conversationDate}

`;

    if (platformUrl) {
      markdown += `> **Original conversation:** [${platformUrl}](${platformUrl})  \n`;
    }

    if (this.includeMetadata) {
      markdown += `> **Extracted from:** \`${this.inputFile}\` using \`extract-llm-conversation ${commandLineArgs}\`

`;
    }

    markdown += `## Context & Goals

[Auto-extracted from ${this.formatPlatformName(format)} export - manual curation recommended]

${this.extractContextFromFirstMessages(conversation)}

## Main Discussion

`;

    // Process messages
    let currentSection = '';
    for (const message of conversation.messages) {
      if (message.sender === 'human') {
        const messagePreview = this.truncateText(message.text, 100);
        if (messagePreview.length > 20) {
          currentSection = this.generateSectionTitle(messagePreview);
          markdown += `\n### ${currentSection}\n\n`;
        }
        markdown += `**User:** "${this.cleanText(message.text)}"\n\n`;
      } else if (message.sender === 'assistant') {
        const cleanedText = this.removeArtifacts(message.text);
        if (cleanedText.trim()) {
          markdown += `**${this.formatPlatformName(format)}:** ${this.cleanText(cleanedText)}\n\n`;
        }
      }
    }

    // Add artifacts as appendices
    if (artifacts.length > 0) {
      markdown += `## Appendices

### Generated Artifacts

The following artifacts were generated during this conversation:

`;
      
      for (const artifact of artifacts) {
        markdown += `#### ${artifact.title}

**Type:** ${artifact.type}${artifact.language ? ` (${artifact.language})` : ''}  
**Identifier:** \`${artifact.identifier}\`

\`\`\`${artifact.language || 'text'}
${artifact.content}
\`\`\`

`;
      }
    }

    // Add metadata section
    if (this.includeMetadata) {
      markdown += `## Sources & References

- **Platform:** ${this.formatPlatformName(format)}
`;

      if (platformUrl) {
        markdown += `- **Original conversation:** [${this.formatPlatformName(format)}](${platformUrl})
`;
      }

      markdown += `- **Source file:** \`${this.inputFile}\`
- **Extraction command:** \`extract-llm-conversation ${commandLineArgs}\`
- **Extraction date:** ${new Date().toLocaleString('en-GB')}
- **Conversation created:** ${conversationDateTime}
- **Total messages:** ${conversation.messages.length}
${artifacts.length > 0 ? `- **Artifacts generated:** ${artifacts.length}` : ''}
`;
    }

    markdown += `
## Related Work

[To be filled manually based on any resulting documentation or implementation]

`;

    return markdown;
  }

  private getPlatformUrl(id: string, format: string): string | null {
    switch (format) {
      case 'claude':
        return `https://claude.ai/chat/${id}`;
      case 'chatgpt':
        return `https://chat.openai.com/c/${id}`;
      // Add more platform URL patterns
      default:
        return null;
    }
  }

  private formatPlatformName(format: string): string {
    const names: Record<string, string> = {
      claude: 'Claude',
      chatgpt: 'ChatGPT',
      gemini: 'Gemini',
    };
    return names[format] || format;
  }

  private estimateDuration(conversation: LLMConversation): string {
    const start = new Date(conversation.created_at);
    const end = new Date(conversation.updated_at);
    const durationMinutes = Math.round((end.getTime() - start.getTime()) / (1000 * 60));
    
    if (durationMinutes < 60) {
      return `~${durationMinutes} minutes`;
    } else {
      const hours = Math.floor(durationMinutes / 60);
      const minutes = durationMinutes % 60;
      return `~${hours}h ${minutes}m`;
    }
  }

  private extractContextFromFirstMessages(conversation: LLMConversation): string {
    const firstFewMessages = conversation.messages.slice(0, 3);
    const context = firstFewMessages
      .filter(msg => msg.sender === 'human')
      .map(msg => this.truncateText(msg.text, 200))
      .join(' ');
    
    return context || '[Context to be manually extracted from conversation]';
  }

  private generateSectionTitle(text: string): string {
    const words = text.toLowerCase().split(/\s+/).slice(0, 5);
    return words
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ')
      .replace(/[^\w\s]/g, '');
  }

  private cleanText(text: string): string {
    return text
      .replace(/\n\s*\n\s*\n/g, '\n\n')
      .replace(/^\s+|\s+$/g, '')
      .replace(/[ \t]+/g, ' ')
      .replace(/\n /g, '\n')
      .replace(/ \n/g, '\n');
  }

  private removeArtifacts(text: string): string {
    // Remove Claude artifacts - can be extended for other formats
    return text.replace(/<antArtifact[^>]*>[\s\S]*?<\/antArtifact>/g, '[Artifact generated - see Appendices]');
  }

  private truncateText(text: string, maxLength: number): string {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength).replace(/\s\S*$/, '') + '...';
  }

  private async generateFilename(conversationTitle: string, outputPath: string): Promise<string> {
    // Get current date in yyMMdd format
    const now = new Date();
    const year = now.getFullYear().toString().slice(-2);
    const month = (now.getMonth() + 1).toString().padStart(2, '0');
    const day = now.getDate().toString().padStart(2, '0');
    const datePrefix = `${year}${month}${day}`;
    
    // Convert title to filename-safe format
    const description = conversationTitle
      .toLowerCase()
      .replace(/[^\w\s-]/g, '')
      .replace(/\s+/g, '_')
      .replace(/_+/g, '_')
      .replace(/^_|_$/g, '');
    
    // Find next available letter
    try {
      const files = await readdir(outputPath);
      const pattern = new RegExp(`^${datePrefix}([a-z])_`);
      const usedLetters = new Set(
        files
          .map((file: string) => file.match(pattern)?.[1])
          .filter(Boolean)
      );

      const nextLetter = 'abcdefghijklmnopqrstuvwxyz'
        .split('')
        .find(letter => !usedLetters.has(letter)) || 'a';

      return `${datePrefix}${nextLetter}_${description}`;
    } catch {
      // If directory doesn't exist or can't be read, default to 'a'
      return `${datePrefix}a_${description}`;
    }
  }
}

// CLI setup
const cli = new Cli({
  binaryLabel: 'LLM Conversation Extractor',
  binaryName: 'extract-llm-conversation',
  binaryVersion: '1.0.0',
});

cli.register(ExtractLLMConversationCommand);
cli.runExit(process.argv.slice(2));