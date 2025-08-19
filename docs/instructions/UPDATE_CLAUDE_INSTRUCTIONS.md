# Updating AI Agent Instructions

Guidelines for maintaining CLAUDE.md (or equivalent Cursor rules file) to help AI agents operate effectively on your codebase.

## See also

- `CLAUDE.md` - The main instructions file for AI agents (or `.cursorrules`, etc.)
- `WRITE_EVERGREEN_DOC.md` - General documentation writing guidelines
- `UPDATE_HOUSEKEEPING_DOCUMENTATION.md` - Documentation maintenance process

## Purpose of Agent Instructions File

This file (CLAUDE.md, .cursorrules, etc.) serves as the primary orientation document for AI agents working on your codebase. It should provide essential context and signposts without duplicating information that exists elsewhere in the documentation.

## What to Include

### Essential Project Context
- **Project overview** - Brief description of goals and current phase
- **Architecture summary** - Key framework and storage decisions
- **Build commands** - How to run, test, and debug the application
- **Project structure** - Where to find different types of code/docs

### Debugging and Development Aids
- **Type checking** - Commands for compilation errors
- **Linting** - Code quality checking commands
- **Testing** - Test commands and coverage info
- **Log files** - Location of development logs
- **Test locations** - Where to find existing tests
- **Database info** - Migration files and schema documentation

### Navigation Signposts
- **Architecture docs** - Link to main architecture documentation
- **Planning docs** - Point to recent decisions and planning documents
- **Specific domains** - Database, API, UI components documentation

### Operational Guidelines
- **Git practices** - Reference to commit and workflow guidelines
- **Code style** - Spelling preferences, existing patterns
- **Environment setup** - Key variables and configuration

## What NOT to Include

- **Detailed instructions** - These belong in specific domain docs
- **Code examples** - Link to actual implementation files instead
- **Duplicate information** - Always reference canonical source
- **Step-by-step tutorials** - These belong in setup documentation

## Maintenance Principles

### Conciseness
Keep the instructions file focused and scannable. Each section should be 3-5 bullet points maximum. Use signposting rather than explanation.

### Signposting Over Duplication
Instead of explaining how something works, point to where the information lives:
- "Database schema: `migrations/` directory and `../reference/DATABASE_SCHEMA.md`"
- "Testing: Framework setup in test config, tests in `tests/` or `__tests__/`"

### Current State Focus
Document what exists now, not what's planned. Use status indicators (✓ implemented, 📋 planned) when helpful.

### User-Driven Updates
Update the instructions file based on:
- **User feedback** - What agents needed but couldn't find
- **Common pain points** - Debugging paths that weren't obvious
- **New major features** - Changes to build process, architecture
- **Structural changes** - New documentation, moved files

## Review Triggers

Update your agent instructions when:
- AI agents struggle to find essential information
- Major architectural changes occur
- New debugging tools or processes are added
- Project structure changes significantly
- User identifies missing signposts during development

## Quality Checklist

Before updating agent instructions:
- [ ] Information is essential for AI agent effectiveness
- [ ] No duplication of content available elsewhere
- [ ] All links and references are valid
- [ ] Debugging paths are clear and actionable
- [ ] Structure remains scannable and concise
- [ ] Cross-references point to canonical sources

## Tool-Specific Considerations

### Claude Code (CLAUDE.md)
- Include tasks and subagents guidance for context window management
- Reference specific tools and permissions needed
- Include parallel tool execution patterns
- Document debugging workflows for command-line environments

### Cursor (.cursorrules)
- Include workspace configuration hints where relevant
- Reference model selection best practices if applicable
- Include shortcuts and workflow patterns for IDE users
- Consider IDE-specific debugging approaches

### Other AI Tools
- Adapt structure to tool capabilities and limitations
- Include tool-specific workflow patterns
- Reference appropriate documentation formats for the platform
- Consider different context window constraints

## Customization Guidelines

When maintaining CLAUDE.md:

1. **Keep project-specific** - Tailor content to actual codebase needs
2. **Remove inapplicable sections** - Don't include generic content that doesn't apply
3. **Add project-specific sections** as needed (API keys, special workflows, domain knowledge)
4. **Maintain conciseness** - File should be scannable, not comprehensive
5. **Use signposting approach** - Point to detailed docs rather than duplicating content
6. **Update regularly** - Keep build commands and key information current

## Essential References Structure

When organizing the "See also" section in CLAUDE.md, consider this structure:

```markdown
see:
- `README.md` for project goals and features
- `docs/reference/CODING_PRINCIPLES.md` for development principles
- `docs/instructions/GIT_COMMIT_CHANGES.md` for Git workflow
- `docs/reference/ARCHITECTURE_OVERVIEW.md` for system architecture
- `docs/reference/[DOMAIN]_*.md` for specific domain documentation
```

This provides a logical hierarchy from general (README) to specific (domain docs).