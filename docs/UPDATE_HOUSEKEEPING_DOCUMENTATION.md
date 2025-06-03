# Update Housekeeping Documentation

This document describes the process for keeping project documentation up-to-date as the codebase evolves. Documentation housekeeping should be performed regularly to ensure accuracy and prevent confusion.

## See also

- `docs/DOCUMENTATION_ORGANISATION.md`
- `docs/WRITE_EVERGREEN_DOC.md` - Guidelines for writing evergreen documentation
- `docs/WRITE_PLANNING_DOC.md` - Guidelines for ephemeral planning documents
- `docs/GIT_COMMITS.md` - How to commit documentation updates

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
2. `docs/*.md` - All evergreen documentation
3. Recent `planning/*.md` - Latest decisions and changes
4. Key code files and API routes
5. Configuration files and migrations

Use subagents where appropriate to maintain context window efficiency.

### Step 2: Identify Outdated Content

Look for:
- **Feature Status Mismatches** - Documentation says "not implemented" but code exists
- **Architectural Drift** - Documentation describes old approaches superseded by new decisions
- **Missing Features** - New functionality not documented
- **Broken Cross-References** - Links to renamed/removed files
- **Duplicate Information** - Same content in multiple places (consolidate to one location)
- **Incomplete Sections** - Placeholder or stub documentation

### Step 3: Update Documentation

Follow these principles:
1. **Single Source of Truth** - Information should exist in one canonical location
2. **Cross-Reference** - Link to canonical docs rather than duplicating content
3. **Transitional States** - Document both current and target states during migrations
4. **Clear Status** - Mark features/approaches as current, deprecated, or planned

### Step 4: Suggest any potentially missing/obsolete documents to the user

(If the user agrees, then add/remove accordingly).

### Step 5: Update project configuration documentation if needed

Consider whether changes affect essential project configuration or AI agent context:
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
see `docs/CONFIGURATION.md` for configuration architecture
```

### Step 6: Suggest a commit to the user (following `docs/GIT_COMMITS.md`)

1. **Self-Review** - Re-read all changes for consistency
2. **Test Links** - Verify cross-references work
3. **Check Examples** - Ensure code examples match current implementation
4. **Commit Message** - Follow `docs/GIT_COMMITS.md` guidelines

Example commit message:
```
docs: update documentation to reflect current implementation

- Update PROJECT_STATUS.md with implemented features
- Reflect architecture transition in relevant docs
- Add cross-references between related documentation
- Update component documentation with current functionality
```

## Documentation Quality Checklist

Before committing, ensure:
- [ ] No contradictions between documents
- [ ] Status accurately reflects implementation
- [ ] Cross-references are valid
- [ ] Transitional states are clearly marked
- [ ] "See also" sections are comprehensive
- [ ] Examples match current code patterns
- [ ] Technical details are accurate

## Common Pitfalls

1. **Over-updating** - Don't change accurate historical records in planning docs
2. **Under-referencing** - Always add "see also" links for related topics
3. **Duplication** - Resist copying content; link to canonical source
4. **Vague Status** - Be specific about what's implemented vs planned
5. **Missing Context** - Explain why architectural changes were made
