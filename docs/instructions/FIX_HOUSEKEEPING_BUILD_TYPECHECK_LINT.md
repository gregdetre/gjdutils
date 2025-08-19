# Fix Housekeeping Build, TypeCheck & Lint Issues

This is a periodic housekeeping task to maintain code quality and catch potential issues early in the development process.

## Goal

Systematically address build, TypeScript, and linting issues to prevent accumulation of technical debt and ensure the codebase remains healthy for AI-first development.

## Comprehensive Health Check Process

### Stage 1: Assessment & Prioritisation

#### Run Full Health Checks
```bash
# Type checking - most critical for runtime safety
npm run build            # Project build with some lenience
tsc --noEmit            # Strict TypeScript type checking

# Code quality and patterns  
npm run lint            # ESLint issues and warnings

# Functionality verification
npm test               # Test suite
npm run test:e2e       # E2E tests (if available and time permits)
```

#### Assess Scope & Impact
- **Count issues**: `tsc --noEmit 2>&1 | grep -c "error TS"` and `npm run lint 2>&1 | grep -c Warning`
- **Categorise by severity**:
  - 🔴 **BLOCKING**: TypeScript errors that could cause runtime failures
  - 🟡 **HIGH**: ESLint errors, deprecated patterns, security issues
  - 🟢 **LOW**: Style warnings, minor inconsistencies
- **Identify patterns**: Are errors clustered in specific files/areas?

#### Prioritisation Strategy
1. **Production code over test code**: Fix core functionality first
2. **Runtime safety over style**: TypeScript errors before ESLint warnings
3. **Recently modified files**: Focus on active development areas
4. **Shared/core modules**: Fix widely-used utilities before isolated features
5. **Quick wins**: Simple fixes that resolve multiple issues

### Stage 2: Systematic Resolution

#### Use Subagents (if available) for Investigation
Deploy subagents (if available) with specific focus areas:
```
"Investigate TypeScript errors in core modules - focus on main API routes and business logic. 
Categorise by: type safety issues, missing types, configuration problems. 
Suggest fix priorities and identify any dangerous patterns."
```

#### Fix in Batches
- **Batch by file/module**: Complete one area before moving to next
- **Batch by error type**: Fix all `exactOptionalPropertyTypes` issues together
- **Test after each batch**: Verify fixes don't break functionality

#### Safety Practices
- **Understand before fixing**: Don't apply mechanical fixes without understanding
- **Preserve functionality**: Use tests to verify changes don't break behaviour  
- **Conservative approach**: If unsure about a fix, mark for discussion rather than guessing
- **Document complex fixes**: Add comments explaining non-obvious corrections

### Stage 3: Verification & Prevention

#### Comprehensive Re-check
```bash
# Verify all issues resolved
npm run build && echo "✅ Build successful"
tsc --noEmit && echo "✅ TypeScript clean" 
npm run lint && echo "✅ Linting clean"
npm test && echo "✅ Tests passing"
```

#### Update Documentation
- Update any affected documentation files if patterns changed
- Note any systematic issues discovered for future prevention
- Update this document if new issue patterns emerge

#### Prevention Measures
- **Consider TypeScript config adjustments**: Should `exactOptionalPropertyTypes` be relaxed for legacy code?
- **Evaluate ESLint rules**: Are any rules generating more noise than value?
- **IDE integration**: Ensure development environment catches issues early
- **Documentation updates**: Add patterns to coding guidelines if needed

## Decision Framework

### When to Fix vs When to Document/Defer

**Fix Immediately**:
- Type errors that could cause runtime crashes
- Security-related linting issues  
- Deprecated API usage that could break in future updates
- Simple mechanical fixes (unused imports, missing semicolons)

**Document & Schedule**:
- Complex refactoring needs that require architectural decisions
- Issues in legacy code that isn't actively maintained
- Style inconsistencies that don't affect functionality
- Performance optimizations that need measurement

**Skip/Disable**:
- ESLint rules that conflict with project conventions
- TypeScript strictness that creates excessive overhead
- Test-only issues that don't affect production

### Stopping Criteria

**Stop and discuss with user if**:
- Fixes require significant architectural changes
- Multiple approaches exist with unclear trade-offs
- Error counts remain high after systematic fixing
- Tests start failing due to corrections
- Uncertainty about safety of changes

## Post-Completion Actions

1. **Commit in logical batches**: Group related fixes together
2. **Update issue tracking**: Note patterns for future housekeeping
3. **Review effectiveness**: Did this process catch important issues?
4. **Schedule next cycle**: Based on issue accumulation rate
5. **Share learnings**: Update team practices if systematic issues found

## Think Hard

Consider the bigger picture:
- Are we fixing symptoms or root causes?
- What does the error pattern tell us about our development process?
- Should we adjust our TypeScript/ESLint configuration for better AI-first development?
- Are there preventive measures (pre-commit hooks, CI checks) worth implementing?
- Is the balance right between strictness and development velocity?

Remember: The goal is sustainable code quality, not perfect cleanliness. Focus on issues that matter for functionality, security, and maintainability.