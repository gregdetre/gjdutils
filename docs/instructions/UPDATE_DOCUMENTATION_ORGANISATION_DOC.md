# Update Documentation Organisation Doc

Creates or updates `docs/reference/DOCUMENTATION_ORGANISATION.md` - a navigational guide to all project documentation.

## See also

- `../reference/DOCUMENTATION_ORGANISATION.md` - Current documentation organisation guide
- `UPDATE_HOUSEKEEPING_DOCUMENTATION.md` - Run this first for content review
- `WRITE_EVERGREEN_DOC.md` - Structure guidelines

## Task

Create/update the documentation organisation guide with sensible categories and clear starting points for newcomers.

**Run after housekeeping**: This should be done after `UPDATE_HOUSEKEEPING_DOCUMENTATION.md` to ensure structural changes reflect current content.

## Content Requirements

1. **Use your judgement** to organise docs into sensible categories (don't move files, just categorise in the guide)
2. **Highlight key starting points** for newcomers and different personas
3. **Cover all significant docs** in relevant directories plus project root files like `README.md`, agent instruction files, and planning structure

## Process

1. **Discover**: Use Glob to find all documentation files
2. **Categorise**: Create logical groupings based on project needs and user personas
3. **Describe**: 1-2 sentences per doc, mark important/starter docs clearly

## Common Categories

### By User Type
- **New contributors** - Setup, architecture overview, coding principles
- **AI agents** - Instruction files, workflow docs, debugging guides
- **Maintainers** - Housekeeping processes, planning workflows

### By Content Type
- **Setup & Infrastructure** - Installation, configuration, tooling
- **Architecture & Design** - System overview, key decisions, patterns
- **Development Workflows** - Git, testing, debugging, planning
- **AI-Assisted Development** - Agent instructions, modes, processes
- **Domain-Specific** - Feature documentation, API references

### By Frequency
- **Daily use** - Common commands, debugging, development modes
- **Occasional** - Setup, major changes, housekeeping
- **Reference** - Architecture decisions, comprehensive guides

## Structure Template

```markdown
# Documentation Organisation

## Quick Start
- New to the project? Start here: ...
- Setting up development? See: ...
- Working with AI assistants? Begin with: ...

## By Category

### [Category Name]
Brief description of what this category covers.

- **[Important Doc]** (⭐ START HERE) - Brief description
- [Regular Doc] - Brief description
- [Another Doc] - Brief description

### [Another Category]
...

## By Persona
- **New Developer**: [doc1], [doc2], [doc3]
- **AI Agent**: [instruction1], [mode1], [process1]
- **Maintainer**: [housekeeping1], [planning1]
```

## Focus

**This task**: Documentation discovery, categorisation, and navigation structure
**Housekeeping**: Content accuracy, cross-references, implementation status

**Sequence**: Run housekeeping first to ensure content is current, then update organisation guide to reflect any structural changes.