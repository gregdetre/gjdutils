# Non-Interactive AI Assistant Usage

Non-interactive mode allows AI assistants to execute tasks without human intervention.

**Note**: This document is specifically written for Claude Code (`claude -p`) but the principles apply to other AI tools.

## See Also

- `../WRITE_PLANNING_DOC.md` - Creating structured task documents
- `../GIT_COMMITS.md` - Git workflow practices
- `../CODING_PRINCIPLES.md` - Development principles
- Planning documents in your project's planning/ directory

## Tool Access Philosophy

**Non-interactive AI assistants typically cannot:**
- Run applications (no access to development servers, browsers, or live applications)
- Execute tests interactively (no access to test runners that require interaction)
- Access specialized MCP tools (browser automation, database queries)
- Commit changes to git (this should be handled externally)
- Access running development servers or databases

**Non-interactive AI assistants can:**
- Read, write, and edit files
- Perform static analysis of code
- Search and research via web
- Use basic command line tools for file operations
- Generate and modify documentation
- Analyse project structure and dependencies

## Basic Usage

### Claude Code Example
```bash
claude -p "your task description" \
  --allowedTools "Bash Edit MultiEdit Read Write Glob Grep LS Task WebFetch WebSearch TodoRead TodoWrite" \
  --output-format stream-json
```

### Using Wrapper Scripts

Consider creating a wrapper script (e.g., `scripts/ai-batch.sh`) to standardize your non-interactive AI usage patterns.

## Planning Document Integration

Non-interactive mode works best with well-structured planning documents (see `WRITE_PLANNING_DOC.md`). Feed the AI the entire planning document content:

```bash
# Claude Code example
./scripts/claude-batch.sh "$(cat planning/your_task.md)"
```

This approach:
- Provides complete context upfront
- Reduces need for clarifying questions
- Enables autonomous task execution
- Works well with parallel execution

## CI/CD Integration

### Example GitHub Actions Workflow
```yaml
name: AI-Assisted Development
on:
  workflow_dispatch:
    inputs:
      task_description:
        description: 'Task for AI to execute'
        required: true

jobs:
  ai-task:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install AI Tools
        run: npm install -g @anthropic-ai/claude-code
      - name: Run AI Task
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          claude -p "${{ github.event.inputs.task_description }}" \
            --allowedTools "Edit MultiEdit Read Write Glob Grep LS Task WebFetch WebSearch" \
            --output-format stream-json
```

## Tool Configuration

### Recommended Tool Set
- **Core file operations**: `Edit MultiEdit Read Write`
- **Search and discovery**: `Glob Grep LS`
- **Research and analysis**: `WebFetch WebSearch`
- **Task management**: `TodoRead TodoWrite`
- **Basic system operations**: `Bash` (limited to file operations)
- **Subtask delegation**: `Task`

### Security Considerations
- Use specific tool allowlists rather than broad permissions
- Limit shell access to safe operations
- Run in isolated environments for untrusted tasks
- Store API keys securely in CI environments

## Error Handling

Non-interactive mode requires robust error handling since AI cannot ask for clarification:

### In Task Descriptions
```markdown
# Task: Refactor authentication system

## Error Handling
- If compilation errors occur, document them in /tmp/issues.md
- If tests would be needed, create them but note they cannot be run
- If unclear about implementation details, make reasonable assumptions and document them

## Constraints  
- Cannot run application or tests
- Cannot commit changes
- Must work with existing code patterns
```

### In Wrapper Scripts
```bash
ai-batch() {
    # ... setup ...
    
    if ! claude -p "$prompt" --allowedTools "$tools" --output-format stream-json; then
        echo "AI task failed. Check output above for details."
        return 1
    fi
}
```

## Best Practices

1. **Provide complete context** in planning documents
2. **Specify constraints clearly** (no testing, no commits, etc.)
3. **Use structured output** for automation parsing
4. **Handle failures gracefully** in CI environments
5. **Limit scope** to tasks that don't require runtime verification
6. **Document assumptions** when requirements are ambiguous

## Unresolved Questions

### Git & Branch Management
- Should AI be able to make its own Git commits?
- Should wrapper scripts automatically create branches for each task?
- How should branch naming be standardised for parallel execution?
- Should cleanup of completed branches be automated?

### Output Format
- Is `stream-json` the best format for CI integration?
- Should results be structured differently for different use cases?
- How should partial results be handled if AI is interrupted?

### Task Scope
- Should there be timeout limits for long-running tasks?

### Error Recovery
- How should the system handle partial completions?
- Should failed tasks be automatically retried with modified parameters?
- What level of rollback capability is needed?