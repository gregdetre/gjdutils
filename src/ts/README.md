# gjdutils TypeScript Utilities

A collection of general-purpose TypeScript utilities and CLI tools for development workflows.

## Installation

```bash
cd gjdutils
npm install
npm run build
```

## Available Tools

### CLI Utilities

#### sequential-datetime-prefix
Generate sequential datetime prefixes in yyMMdd[x]_ format for organizing files by date.

```bash
# Generate next available prefix for a folder
npx tsx src/ts/cli/sequential-datetime-prefix.ts planning/

# Output: 241225a_ (if no files exist for today)
# Output: 241225b_ (if 241225a_ already exists)
```

#### extract-llm-conversation
Extract and format LLM conversations from JSON exports to structured markdown.

```bash
# Extract single conversation
npx tsx src/ts/cli/extract-llm-conversation.ts --uuid <conversation-id> --input conversations.json

# Extract multiple conversations
npx tsx src/ts/cli/extract-llm-conversation.ts --uuid id1,id2,id3 --input conversations.json --output docs/
```

### Script Utilities

#### count-lines
Count lines of code with configurable exclusions.

```bash
# Count all code
npx tsx src/ts/scripts/count-lines.ts

# Count by file
npx tsx src/ts/scripts/count-lines.ts --by-file

# Exclude tests
npx tsx src/ts/scripts/count-lines.ts --exclude-tests
```

#### git-worktree-sync
Synchronize Git worktree branches with main branch.

```bash
# From feature branch: sync main → current
npx tsx src/ts/scripts/git-worktree-sync.ts

# From main: sync specific branch → main
npx tsx src/ts/scripts/git-worktree-sync.ts --branch feature-branch

# From main: sync all worktrees → main
npx tsx src/ts/scripts/git-worktree-sync.ts
```

### Critique Tools

#### llm-critique-planning-docs
Generate comprehensive codebase context and send to LLMs for planning document critique.

```bash
# Critique with default model
npx tsx src/ts/critique/llm-critique-planning-docs.ts planning/my-plan.md

# Use specific model
npx tsx src/ts/critique/llm-critique-planning-docs.ts --model anthropic:claude-3-opus:latest planning/my-plan.md

# Include specific files
npx tsx src/ts/critique/llm-critique-planning-docs.ts --files src/api.ts --files lib/db.ts planning/my-plan.md
```

#### parse-llm-output
Parse LLM critique output and format it nicely.

```bash
# Parse from file
npx tsx src/ts/critique/parse-llm-output.ts critique-output.json

# Parse from stdin
cat critique-output.json | npx tsx src/ts/critique/parse-llm-output.ts
```

## Development

```bash
# Build TypeScript
npm run build

# Watch mode for development
npm run watch

# Clean build artifacts
npm run clean
```

## Contributing

When adding new utilities:
1. Follow the existing patterns for CLI tools using Clipanion
2. Make tools configurable and general-purpose
3. Add comprehensive documentation and examples
4. Include type definitions for better IDE support

## License

MIT License - see root LICENSE file for details.