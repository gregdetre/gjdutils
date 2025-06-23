# PORT_DOCS_TO_GJDUTILS.md - Documentation Sharing Instruction

This instruction helps you share valuable AI-assisted programming documentation between projects, particularly when porting from specific project documentation to general-purpose documentation repositories.

## Context

When working on AI-assisted programming projects, you often develop valuable documentation, instructions, and processes that could benefit other projects. This instruction provides a systematic approach to:

1. Identify documentation worth sharing
2. Generalize project-specific content
3. Maintain quality while making content broadly applicable
4. Keep multiple documentation repositories synchronized

## When to Use This Instruction

Use this when you want to:
- Share AI-assisted programming techniques with the wider community
- Port documentation from a specific project to a general-purpose repository
- Synchronize improvements between related documentation repositories
- Contribute to open-source documentation collections

## Process Overview

### 1. Documentation Audit
Compare documentation between source project and target repository:
- **Files that exist in both**: Compare versions and identify improvements to port
- **Files unique to source**: Evaluate for general applicability
- **Files unique to target**: Consider if they should be ported back to source
- **Naming inconsistencies**: Identify opportunities for standardization

### 2. Generalization Strategy
When porting project-specific documentation to general repositories:

**Remove/Generalize:**
- Specific tool references (e.g., `./scripts/specific-script.ts` → `date` command)
- Project-specific terminology and jargon
- Hardcoded file paths and directory structures
- References to specific frameworks or technologies (unless the doc is about that framework)
- Internal project references and links

**Keep/Preserve:**
- Core methodologies and processes
- Best practices and principles
- Template structures and formats
- Examples (but make them generic)
- Quality guidelines and standards

### 3. Content Categories

**High-Value Documentation for Sharing:**
- Process instructions (planning, research, documentation)
- Methodology guides (parallel research, conversation capture)
- Best practices (coding principles, workflow practices)
- Template documents (planning templates, instruction formats)
- Automation guides (CI/CD integration, non-interactive usage)

**Project-Specific Documentation (Keep Local):**
- Architecture decisions specific to the project
- Implementation details tied to specific technologies
- Deployment and infrastructure specifics
- Business logic and domain-specific processes

## Implementation Steps

### Phase 1: Audit and Planning
1. **List all documentation** in both source and target repositories
2. **Categorize by portability**: Generalizable vs. project-specific
3. **Identify improvements** in either direction
4. **Create task list** with specific actions and priorities

### Phase 2: High-Value Porting
1. **Start with methodology documents** - these tend to be most valuable and generalizable
2. **Port process instructions** - planning, research, documentation practices
3. **Share automation guides** - CI/CD, non-interactive usage patterns
4. **Include this instruction** as an example for other projects

### Phase 3: Bidirectional Updates
1. **Update existing docs** with improvements from either side
2. **Consolidate similar documents** with different names
3. **Standardize naming conventions** across repositories
4. **Fix cross-references** and internal links

### Phase 4: Maintenance
1. **Review ported docs** for consistency and quality
2. **Test all references** and links
3. **Update cross-references** between documents
4. **Establish synchronization process** for future updates

## Generalization Guidelines

### Terminology Updates
- "Subagents" → "Parallel AI assistants" or "Separate AI instances"
- Tool-specific terms → Generic equivalents
- Project names → "Your project" or generic placeholders
- Specific commands → Generic command patterns

### Reference Updates
- Specific scripts → Generic commands or patterns
- Project file paths → Generic directory structures
- Internal links → Generic reference patterns
- Tool-specific examples → Platform-agnostic examples

### Example Transformations
```markdown
# Before (Project-Specific)
Use `./scripts/generate-sequential-datetime-prefix.ts planning/` to get the date prefix

# After (Generalized)  
Use `date +"%y%m%d"` to get the current date for the prefix
```

```markdown
# Before (Project-Specific)
Follow instructions in `docs/instructions/WRITE_EVERGREEN_DOC.md`

# After (Generalized)
Follow documentation writing best practices for structure and clarity
```

## Quality Assurance

### Content Quality
- **Preserve core value**: Don't lose the essential insights while generalizing
- **Maintain completeness**: Ensure generalized versions are still actionable
- **Check examples**: Make sure generic examples still illustrate the concepts
- **Verify references**: Ensure all links and cross-references work

### Structural Quality
- **Consistent formatting**: Follow the target repository's style
- **Clear headings**: Make navigation easy across all ported documents
- **Logical organization**: Maintain coherent structure after generalization
- **Appropriate length**: Keep documents focused and useful

## Maintenance Strategy

### Regular Synchronization
1. **Periodic reviews** of both repositories for new valuable content
2. **Bidirectional updates** when improvements are made
3. **Version tracking** to know which documents have been synchronized
4. **Change documentation** to track what was modified during porting

### Documentation Lifecycle
1. **Create** new documentation in the most appropriate repository
2. **Evaluate** for sharing potential during regular reviews
3. **Port** valuable content using this process
4. **Maintain** synchronization for ongoing improvements
5. **Archive** outdated content appropriately

## Integration with Other Projects

This instruction itself demonstrates the principle - it can be used by any project wanting to share documentation with general-purpose repositories like gjdutils.

### For Project Maintainers
- Use this process to contribute your AI-assisted programming insights to the community
- Regularly audit your documentation for sharing opportunities
- Consider which practices would benefit other projects

### For Repository Maintainers
- Use this process to systematically incorporate improvements from contributing projects
- Maintain quality standards while welcoming diverse contributions
- Provide clear guidelines for contributors using this process

This approach ensures valuable AI-assisted programming techniques are shared effectively while maintaining quality and broad applicability.