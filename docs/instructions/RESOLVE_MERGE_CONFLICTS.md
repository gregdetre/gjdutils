# Resolve Merge Conflicts

Review:
- Git status
- the recent/relevant Git history
- planning docs for any relevant pieces of work
- the details of the merge conflict itself
- relevant code & docs, starting with relevant planning documents

Do you feel confident about how to resolve the merge conflict? Ask if you have questions.

Ultrathink.

Make a proposal. Don't make changes yet.

## Analysis Framework

### 1. Understand the Context
- **What branches are merging?** Examine the git log to understand what work each branch contains
- **What was the intent of each change?** Look at commit messages and planning docs
- **Are these related features or independent work?** Understanding the relationship helps resolve conflicts appropriately

### 2. Examine the Conflicts
- **What type of conflicts?** Content conflicts, structural conflicts, or semantic conflicts?
- **Which files are affected?** Code, configuration, documentation, or tests?
- **What are the competing changes?** Are they complementary or mutually exclusive?

### 3. Consider the Options
- **Merge both changes** - Often the right choice when changes are complementary
- **Choose one side** - When changes are mutually exclusive or one is clearly better
- **Create a hybrid solution** - Combine the best aspects of both approaches
- **Restructure the code** - Sometimes conflicts indicate a need for refactoring

### 4. Validate the Resolution
- **Does the merged code make sense?** Check for logical consistency
- **Are there any integration issues?** Consider how the combined changes work together
- **What tests or validation are needed?** Ensure the resolution doesn't break functionality

## Common Conflict Patterns

### Import/Dependency Conflicts
- Both branches added different imports → Keep both if they're needed
- Different versions of the same dependency → Choose the newer/better version
- Restructured imports → Follow the more systematic approach

### Feature Implementation Conflicts
- Different approaches to the same feature → Evaluate and choose the better implementation
- Independent features → Usually safe to merge both
- Refactoring conflicts → Follow the more complete/systematic refactoring

### Configuration Conflicts
- Different settings → Choose based on the target environment
- New vs modified config → Usually merge both changes
- Schema changes → Ensure compatibility with both sets of changes

### Documentation Conflicts
- Different descriptions → Merge to create comprehensive documentation
- Structural changes → Follow the more organized approach
- Version conflicts → Keep the most up-to-date information

## Resolution Strategy

1. **Start with automatic merges** - Let git handle what it can
2. **Resolve file by file** - Don't try to solve everything at once
3. **Understand before changing** - Make sure you know what each side is trying to achieve
4. **Test incrementally** - Validate each resolution as you go
5. **Document your reasoning** - Leave comments explaining non-obvious resolution choices

## When to Ask for Help

- **Unfamiliar code areas** - Don't guess if you don't understand the domain
- **Complex business logic** - When the conflict involves important business rules
- **Breaking changes** - If resolution might break existing functionality
- **Architectural decisions** - When conflicts reveal deeper design issues

Remember: A good merge conflict resolution preserves the intent of both changes while maintaining code quality and functionality.