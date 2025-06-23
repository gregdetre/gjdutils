# Update Housekeeping Documentation

This document describes the process for keeping project documentation up-to-date as the codebase evolves. Documentation housekeeping should be performed regularly to ensure accuracy and prevent confusion.

## See also

- Documentation organisation guide (if available) - Comprehensive guide to all project documentation organisation and navigation
- `UPDATE_DOCUMENTATION_ORGANISATION_DOC.md` - Run after this process to update documentation organisation guide (if available)
- `WRITE_EVERGREEN_DOC.md` - Guidelines for writing evergreen documentation
- `WRITE_PLANNING_DOC.md` - Guidelines for ephemeral planning documents
- AI instruction maintenance guide (if available, e.g. `TEMPLATE_FOR_CLAUDE_RULES.md` for `CLAUDE.md`) - Maintaining AI agent context as part of housekeeping
- `GIT_COMMITS.md` - How to commit documentation updates

## When to Update Documentation

Perform documentation housekeeping:
- After implementing major features
- When architectural decisions change
- When you notice outdated information while working
- As a periodic maintenance task (e.g., weekly/monthly)
- Before major releases or milestones

## Process Overview

### Step 1: Comprehensive Review

Read all key documentation to understand the current state:
1. `README.md` - Project overview and goals
2. Documentation organisation guide (if available) - Documentation structure and navigation guide
3. `../reference/*.md` and `*.md` - All evergreen documentation
4. Recent `planning/*.md` - Latest decisions and changes
5. Key code files and API routes
6. Configuration files and migrations

Use parallel AI assistants where appropriate to maintain context window efficiency.

### Step 2: Identify potential improvements

Look for:
- **Feature Status Mismatches** - Documentation says "not implemented" but code exists
- **Architectural Drift** - Documentation describes old approaches superseded by new decisions
- **Missing High-level Docs** - Missing high-level/overview evergreen/reference documentation, e.g. README, SETUP, ARCHITECTURE, PRODUCT VISION, CODING_PRINCIPLES/GUIDELINES, PROJECT_STRUCTURE, TESTING, UI_INTERFACE and/or STYLING/DESIGN, etc. These are just examples - use your judgment about which high-level docs would be most relevant to this particular codebase.
- **Missing Features** - New functionality not documented
- **Broken Cross-References** - Links to renamed/removed files
- **Duplicate Information** - Same content in multiple places (consolidate to one location)
- **Incomplete Sections** - Placeholder or stub documentation
- **Unclear Filenames** - Documentation files with ambiguous or overly brief names that don't clearly indicate content
- **Not that useful** - Information that isn't very relevant or adding much. Either remove or make it more concise
- **No longer useful** - Information that may have been useful in the past, but is out-of-date or no longer so useful. Either remove, make it more concise, or move into an Appendix as a historical record (if you think it still has some value as background)

Follow these principles:
1. **Single Source of Truth** - Information should exist in one canonical location
2. **Cross-Reference** - Link to canonical docs rather than duplicating content
3. **Transitional States** - Document both current and target states during migrations
4. **Clear Status** - Mark features/approaches as current, deprecated, or planned

### Step 3: Make prioritised suggestions

Discuss proposed changes to the user, usually grouped by priority (most important/valuable/problematic first).

Agree a plan with the user, and execute it, defaulting to highest-priority first.

- Use tasks and parallel AI assistance (provided with rich context to make sure they make correct/useful/sensible/aligned changes).

- Commit in batches (following `GIT_COMMIT_CHANGES.md`), using parallel AI assistants if available.


### Step 4: Review

Review where we are, and consider whether there's anything remaining, or any other gaps/improvements we're now noticing.


### Step 5: Late-stage housekeeping steps

After completing the main documentation updates:

1. **Update documentation organisation guide**: If your project has a documentation organisation guide, update it to ensure it reflects any structural changes made during housekeeping.

2. **Update AI agent context if needed**: If your project has AI instruction files (e.g. `CLAUDE.md`), consider whether changes affect essential AI agent context:
   - New build commands or debugging tools
   - Architectural changes affecting project structure
   - New documentation requiring signposts

#### Common Update Patterns

**Feature Implementation Status**
```markdown
# Before
**Missing Features**
- API integration not yet implemented
- Data processing not built

# After  
**Implemented Features**
- API integration with external service ✓
- Data processing with advanced filtering ✓

**Planned Features**
- File upload functionality
- User management
```

**Architectural Changes**
```markdown
# Add transitional documentation
**Current State**: Code uses component-based architecture
**Target State**: Modular service architecture (see ARCHITECTURE.md)
**Migration Status**: Schema exists, code needs updating
```

**Cross-References**
```markdown
# Instead of duplicating configuration info
see `../reference/CONFIGURATION.md` for configuration architecture
```

**Filename Clarification**
```markdown
# Before
MUTATIONS.md
SETUP.md
API_UTILS.md

# After (with git mv)
MUTATIONS_DOCUMENT_CONTENT_TRANSFORMS.md
SETUP_DEVELOPMENT_ENVIRONMENT.md
API_STRING_REPLACEMENT_UTILITIES.md
```

### Step 6: Suggest a commit to the user (following `GIT_COMMITS.md`)


## Documentation Quality Checklist

Before committing, ensure:
- [ ] No contradictions between documents
- [ ] Status accurately reflects implementation
- [ ] Cross-references are valid
- [ ] Transitional states are clearly marked
- [ ] "See also" sections are comprehensive
- [ ] Examples match current code patterns
- [ ] Technical details are accurate
- [ ] Documentation organisation guide (if available) reflects any structural changes

## Common Pitfalls

1. **Over-updating** - Don't change accurate historical records in planning docs
2. **Under-referencing** - Always add "see also" links for related topics
3. **Duplication** - Resist copying content; link to canonical source
4. **Vague Status** - Be specific about what's implemented vs planned


## Typos and tightening

If you notice typos, fix them.

If you notice places where the doc could be a bit more concise, or more tightly worded, without changing the meaning, then make the changes.

If you notice ways in which you think the doc should be improved, which *would* change the meaning, discuss them with the user. Don't make changes that will change the meaning without explicit permission.