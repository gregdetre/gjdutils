# Git Worktrees Setup and Workflow

Multi-worktree development setup for parallel feature development using a hub-and-spoke model with protected main branch.

> **Ported from**: Spideryarn Reading project's GIT_WORKTREES.md
> **Changes**: Generalized paths, removed project-specific references, made configurable for any project

## See also

- `git-worktree-sync.ts` - Branch synchronisation tool implementation
- `git-worktree-sync-all.ts` - Wrapper script for automated two-way sync across all worktrees
- General Git worktree documentation: `git help worktree`

## Quick Start

**Basic sync commands:**
```bash
# From any worktree: pull latest from main
git-worktree-sync

# From main: merge a specific worktree
git-worktree-sync --branch feature-1

# From main: merge all matching worktrees
git-worktree-sync --pattern "feature-*"

# Automated two-way sync all worktrees (from main)
git-worktree-sync-all

# Sync without running dependency install (faster when dependencies unchanged)
git-worktree-sync-all --run-deps=false

# Use yarn instead of npm
git-worktree-sync-all --deps-command "yarn install"
```

**Autostash support:** The scripts automatically handle uncommitted changes using Git's `--autostash` feature. Your changes are safely stashed before merge and reapplied afterward.

## Principles

- **Protected main branch**: Never work directly on main; all changes go through feature branches
- **Hub-and-spoke model**: Each worktree syncs only with main, not with other worktrees
- **Configurable worktrees**: Use any naming pattern for worktree branches
- **Simple synchronisation**: One-way merge at a time, no complex cross-worktree syncing

## Setting Up Multi-Worktree Environment

### Directory Structure Example
```
/path/to/your/project/
├── myproject/              # Main branch (protected, read-only)
├── myproject-feature1/     # Feature development
├── myproject-feature2/     # Feature development
├── myproject-hotfix/       # Hotfix development
└── myproject-experiment/   # Experimental work
```

### Initial Setup

1. **Navigate to repository directory**:
   ```bash
   cd /path/to/your/project/myproject
   ```

2. **Create worktree branches** (use any naming pattern you prefer):
   ```bash
   git checkout main
   git checkout -b feature1
   git checkout -b feature2
   git checkout -b hotfix
   git checkout -b experiment
   git checkout main  # Return to main
   ```

3. **Create worktree directories**:
   ```bash
   # From within the main repository
   git worktree add ../myproject-feature1 feature1
   git worktree add ../myproject-feature2 feature2
   git worktree add ../myproject-hotfix hotfix
   git worktree add ../myproject-experiment experiment
   ```

4. **Set up each worktree environment**:
   ```bash
   # Copy any necessary config files to each worktree
   cp .env.local ../myproject-feature1/
   cp .env.local ../myproject-feature2/
   # ... and so on for each worktree
   
   # Install dependencies in each worktree if needed
   cd ../myproject-feature1 && npm install
   cd ../myproject-feature2 && npm install
   # ... and so on
   ```

5. **Configure unique settings** in each worktree if needed:
   - Update port numbers in environment files
   - Adjust any worktree-specific configuration

## Development Workflow

### Starting Development

Choose an available worktree for your task:
```bash
cd myproject-feature1
# Start your development server, make changes, etc.
```

### Synchronisation Process

The sync scripts automatically detect your current branch and sync with main:

```bash
# From any worktree directory
git-worktree-sync
```

#### From a worktree branch
Merges main → current worktree:
```bash
# In myproject-feature1
git-worktree-sync  # Merges main → feature1
```

#### From main branch
You have several options:

1. **Sync a specific worktree**:
   ```bash
   # In myproject (main branch)
   git-worktree-sync --branch feature1  # Merges feature1 → main
   ```

2. **Sync all worktrees matching a pattern**:
   ```bash
   # In myproject (main branch)
   git-worktree-sync --pattern "feature*"  # Merges all feature* branches → main
   ```

3. **Sync all worktrees at once**:
   ```bash
   # In myproject (main branch)
   git-worktree-sync-all  # Two-way sync with all matching branches
   ```

**Two-step process for full sync**:

Manual approach:
1. From main: Run sync to merge worktree changes into main
2. From each worktree: Run sync to pull latest main changes

Automated approach (recommended):
- From main: `git-worktree-sync-all` - automatically performs both steps and runs dependency install

### Dependency Management

**Automatic dependency synchronisation**: By default, `git-worktree-sync-all` runs dependency installation in main and each worktree after successful Git sync.

**Benefits**:
- Ensures consistent dependencies across all worktrees
- Prevents "module not found" errors when code changes introduce new dependencies
- Supports different package managers (npm, yarn, pnpm)

**Configuration options**:
```bash
# Default: sync Git + run npm ci
git-worktree-sync-all

# Use yarn instead of npm
git-worktree-sync-all --deps-command "yarn install"

# Use pnpm
git-worktree-sync-all --deps-command "pnpm install"

# Skip dependency install for faster execution
git-worktree-sync-all --run-deps=false
```

### Working with Feature Branches

For complex or risky work, create feature branches from a worktree:

```bash
# In myproject-feature1
git checkout -b complex-feature
# Work on feature...
# When done, merge back to feature1
git checkout feature1
git merge complex-feature
git branch -d complex-feature
```

### Pushing to Remote

Only push the main branch to origin:
```bash
# After syncing to main
cd myproject
git push origin main
```

Worktree branches remain local-only unless explicitly needed for collaboration.

## Common Commands

### Worktree Management
```bash
# List all worktrees
git worktree list

# Remove a worktree
git worktree remove myproject-feature1

# Clean up stale worktree metadata
git worktree prune
```

### Branch Status
```bash
# Check which branches need syncing
git branch -vv

# See commit differences
git log main..feature1 --oneline
git log feature1..main --oneline
```

### Script Configuration
```bash
# Use custom branch pattern
git-worktree-sync --pattern "dev-*"

# Use custom main branch name
git-worktree-sync --main develop

# Verbose output
git-worktree-sync -v

# Custom dependency command
git-worktree-sync-all --deps-command "yarn install --frozen-lockfile"
```

## Conflict Resolution

### Merge Conflicts
When merge conflicts occur:
1. **Resolve conflicts** in the affected files
2. **Stage resolved files**: `git add <files>`
3. **Complete merge**: `git commit`
4. **Continue**: Re-run sync script

### Autostash Conflicts
If Git reports "Applying autostash resulted in conflicts":
1. **Check stashed changes**: `git stash show -p`
2. **Options**:
   - Resolve manually: `git stash pop` then fix conflicts
   - Discard stash: `git stash drop` (if changes no longer needed)
   - Keep stash: Leave it and continue working

### Sync-All Partial Failures
When syncing all worktrees partially fails:

1. **Script reports status**:
   ```
   ✅ Synced 2/3 worktrees to main
   ⚠️  Failed: feature2
   📋 Next: resolve conflicts in main, commit, then re-run this script
   ```

2. **Fix conflicts in main**:
   ```bash
   git status               # See conflicted files
   # Edit files to resolve conflicts
   git add <resolved-files>
   git commit
   ```

3. **Re-run sync-all**:
   ```bash
   git-worktree-sync-all    # Retries failed branches
   ```

**Recovery tip**: Git merges are idempotent - re-running skips already-synced branches.

## Troubleshooting

### Worktree Errors
If "worktree already exists" error:
```bash
# First, clean up stale metadata
git worktree prune

# If the error persists, force remove and re-add
git worktree remove --force <path-to-worktree>
git worktree add ../myproject-feature1 feature1
```

### Sync Script Issues
If sync script not found in a worktree:
1. Manually sync from main first: `git merge main`
2. The script will be available after merge
3. Or install the scripts globally: `npm install -g gjdutils-ts`

### Directory Structure Validation
The sync scripts validate your worktree setup before running. Common issues:

- **Unexpected directories**: Remove or rename to match your pattern
- **Missing branches**: Create the branch or remove the directory
- **Pattern mismatches**: Adjust the `--pattern` option

## Configuration Examples

### Small Team Setup
```bash
# Create worktrees for team members
git checkout -b alice-work
git checkout -b bob-work
git checkout -b shared-integration

git worktree add ../project-alice alice-work
git worktree add ../project-bob bob-work
git worktree add ../project-integration shared-integration

# Sync specific team branches
git-worktree-sync --pattern "*-work"
```

### Feature-Based Setup
```bash
# Create feature-specific worktrees
git checkout -b feature-auth
git checkout -b feature-payments
git checkout -b feature-dashboard

git worktree add ../project-auth feature-auth
git worktree add ../project-payments feature-payments
git worktree add ../project-dashboard feature-dashboard

# Sync feature branches
git-worktree-sync --pattern "feature-*"
```

### Environment-Based Setup
```bash
# Create environment worktrees
git checkout -b dev-environment
git checkout -b staging-test
git checkout -b production-hotfix

git worktree add ../project-dev dev-environment
git worktree add ../project-staging staging-test
git worktree add ../project-hotfix production-hotfix

# Different sync strategies for different environments
git-worktree-sync --branch production-hotfix  # High priority
git-worktree-sync --pattern "dev-*"           # Development branches
```

## Best Practices

1. **Clean commits**: Commit frequently with clear messages
2. **Regular syncing**: Sync with main at least daily to avoid conflicts
3. **Branch hygiene**: Delete feature branches after merging
4. **Worktree purpose**: Keep track of what each worktree is working on
5. **Pattern consistency**: Use consistent naming patterns for easier automation
6. **Dependency management**: Let the sync tools handle dependency updates automatically
7. **Environment isolation**: Use different ports/configs for concurrent development

## Limitations

- All worktrees share the same local Git repository
- Cannot checkout the same branch in multiple worktrees
- Worktree branches are typically local-only (not pushed to origin)
- Manual two-step process required for bidirectional sync (automated by sync-all script)

## Advanced Usage

### Custom Sync Scripts
You can create project-specific wrapper scripts:

```bash
#!/bin/bash
# project-sync.sh
export MAIN_BRANCH=develop
export WORKTREE_PATTERN="task-*"
export DEPS_COMMAND="pnpm install --frozen-lockfile"

git-worktree-sync-all \
  --main $MAIN_BRANCH \
  --pattern "$WORKTREE_PATTERN" \
  --deps-command "$DEPS_COMMAND" \
  "$@"
```

### Integration with CI/CD
```bash
# In your CI pipeline
git-worktree-sync --branch $FEATURE_BRANCH --main $TARGET_BRANCH
git-worktree-sync-all --run-deps=false  # Skip deps in CI
```

This setup provides a robust, scalable workflow for parallel development with Git worktrees.