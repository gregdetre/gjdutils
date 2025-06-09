# TEMPLATE_FOR_CLAUDE_RULES.md

This is a template for `[PROJECT_ROOT]/CLAUDE.md` or a Cursor project-level rules file that should be included automatically in every single conversation with AI agents.

**Instructions**: Replace placeholders in `[BRACKETS]` with project-specific information. Remove sections that don't apply to your project.

---

# CLAUDE.md - [PROJECT_NAME] Codebase Guide

This document provides essential context for AI agents working on the [PROJECT_NAME] project.

## Essential References

see:
- `README.md` for project goals and features
- `docs/instructions/CODING_PRINCIPLES.md` for development principles
- `docs/instructions/GIT_COMMITS.md` for Git workflow
- `[docs/ARCHITECTURE.md]` for system architecture (if applicable)
- `[docs/SETUP.md]` for development setup (if applicable)

## Project Overview

[Brief description of what the project does, current phase/status, and main goals. 2-3 sentences.]

## Development Philosophy

Key principles that guide all development decisions:

- **[Primary principle].** [Brief explanation]
- **Fix the root cause rather than putting on a band-aid.** Avoid fallbacks & defaults - better to fail if input assumptions aren't being met.
- **If you hit any nasty surprises, stop & discuss with the user.** Don't push through unexpected issues.
- **No destructive or irreversible changes without checking with the user.** Be especially careful about operations that could involve data loss, affect databases, production systems, or user data. When in doubt, ask for explicit permission first.
- **Raise errors early, clearly & fatally.** Prefer explicit errors over silent failures.
- **If things don't make sense or seem like a bad idea, ask questions or discuss rather than just going along with it.** Be a good collaborator, and help make good decisions.

## Key Technical Decisions

[Include 3-5 most important architectural/technical choices]

- **Framework**: [e.g., Next.js with TypeScript, Django with Python, etc.]
- **Database**: [e.g., PostgreSQL, MongoDB, SQLite]
- **Styling**: [e.g., Tailwind CSS, styled-components]
- **Testing**: [e.g., Jest, pytest, etc.]
- **Deployment**: [e.g., Vercel, AWS, Docker]

## Build, Testing, and Debugging

### Local Development
- `[npm run dev | python manage.py runserver | etc.]` - Start development server
- `[npm run build | python -m pytest | etc.]` - Build/compile project
- `[npm test | pytest | etc.]` - Run tests
- `[npm run lint | flake8 | etc.]` - Check code quality

### Debugging
- Logs: `[dev.log | logs/ | etc.]` - Check recent output
- Tests: `[__tests__/ | tests/ | src/**/*.test.js]` - Test file locations
- Database: `[migrations/ | schema.sql | models.py]` - Schema and migration files

### Environment Setup
- Development server URL: `[http://localhost:3000 | http://127.0.0.1:8000]`
- Key environment variables: `[NEXT_PUBLIC_API_URL | DATABASE_URL | API_KEY]`
- Configuration files: `[.env.local | .env | config.py]`

## Project Structure

**Active Development**:
- Core implementation: `[src/ | app/ | lib/]`
- Tests: `[__tests__/ | tests/ | spec/]`
- Documentation: `docs/` (evergreen) and `[planning/ | decisions/]` (temporal)
- Configuration: `[package.json | pyproject.toml | Cargo.toml]`

**IGNORE** (if applicable):
- `[deprecated/ | old/ | backup/]` - Legacy/backup code
- `[node_modules/ | venv/ | target/]` - Dependencies/build artifacts

## Documentation Structure

Available documentation in `docs/`:
- `docs/instructions/` - Commands and processes for AI-assisted development
- `docs/reference/` - Technical reference and architecture docs
- `[docs/api/ | docs/guides/]` - Additional project-specific docs

## Context Window, Tasks, and Subagents

Use tasks whenever there's more than a couple of things to keep track of.

Use subagents appropriately:
- For verbose operations (tests, builds, git operations)
- For encapsulated tasks that don't need full conversation context
- When parallel execution would be beneficial
- Provide rich context about goals, constraints, and project patterns

## Code Style and Conventions

- Use [British/American] spelling consistently
- Follow existing patterns in the codebase
- Check for TypeScript/linting errors before committing: `[npm run lint]`
- Run tests after changes: `[npm test]`
- Follow commit message format from `docs/instructions/GIT_COMMITS.md`

## Important Environment Details

- Development framework: `[Node.js 18+ | Python 3.9+ | etc.]`
- Package manager: `[npm | yarn | pip | cargo]`
- Database: `[PostgreSQL 14+ | SQLite | etc.]`
- Current date: [Update with current date/season]

---

## Customization Notes

When adapting this template:

1. **Replace all `[BRACKETED]` placeholders** with project-specific information
2. **Remove inapplicable sections** (e.g., database info for static sites)
3. **Add project-specific sections** as needed (e.g., API keys, special workflows)
4. **Keep it concise** - This file should be scannable, not comprehensive
5. **Use signposting** - Point to detailed docs rather than duplicating content
6. **Update regularly** - Keep build commands and key info current

The goal is to give AI agents just enough context to be effective without overwhelming them with details that belong in dedicated documentation files.