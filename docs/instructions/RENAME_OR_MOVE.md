# Rename or Move Files

- Rename or move a file or files as per the user's explicit instructions. 
  - If asked to propose/discuss, then don't make changes until they have been agreed with the user.
  - If things are confusing, or you see potential problems, or have a better idea, then you should ask questions, raise concerns, make suggestions, etc.

- If there are multiple files, use tasks and subagents (provided with rich context) to:
  - Do the rename/move
    - Prefer to use `git mv` rather than `mv`, where appropriate. Or if there is a special tool for doing the move (e.g. a syntactically-aware refactoring tool, use that)
  - Search carefully for all the places that refer to each file, and update them appropriately.
    - Be careful not to break/disrupt functionality.

- IMPORTANT: If in doubt, or you notice any issues/surprises/complications stop and ask.

- Once you have finished, commit these changes as a single commit, following `GIT_COMMITS.md`

## Process Guidelines

### Before Starting
1. **Understand the scope** - How many files are affected?
2. **Check for references** - What refers to these files?
3. **Identify risks** - What could break with this change?
4. **Plan the approach** - Git mv, refactoring tools, or simple moves?

### During Execution
1. **Use appropriate tools**:
   - `git mv` for version-controlled files
   - IDE refactoring tools for code symbols
   - Search and replace for documentation references
   
2. **Search thoroughly for references**:
   - Import/require statements
   - Documentation links
   - Configuration files
   - Build scripts and manifests
   - Test files
   - Comments and README files

3. **Test incrementally** if possible:
   - Check that code still compiles
   - Run relevant tests
   - Verify documentation links

### Common Reference Patterns
- **Code**: `import './old-name'`, `require('../old-path')`
- **Documentation**: `[link](old-path.md)`, `see old-file.js`
- **Configuration**: File paths in package.json, tsconfig.json, etc.
- **Build systems**: File references in build scripts, CI configs
- **URLs**: Repository links, deployment paths

### Safety Checks
- **Backup important changes** before large moves
- **Use git status** to review all affected files
- **Test functionality** after the move
- **Review commit diff** before finalizing

### Complex Scenarios
For large refactoring operations:
1. Break into smaller, atomic moves when possible
2. Use subagents to handle different aspects (code vs docs vs config)
3. Consider doing a trial run or creating a branch first
4. Coordinate with team members if this affects shared code

Remember: It's better to ask questions and move carefully than to break working functionality.