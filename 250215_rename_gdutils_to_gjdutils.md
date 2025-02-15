# Renaming gdutils to gjdutils

## Context
- Renaming project from `gdutils` to `gjdutils` (existing `gdutils` name is taken)
- Package contains utility functions for strings, dates, data science/AI, web development
- Currently at version 0.1.0, moving to 0.2.0 for the rename

## Files Requiring Updates
1. Package files:
   - pyproject.toml:
     - Update name from "GDutils" to "GJDutils"
     - Update GitHub URLs from gdutils to gjdutils
   - __VERSION__.py: Update version to 0.2.0
   - Rename directory from gdutils/ to gjdutils/
   - Update imports in all Python files:
     - `from gdutils import ...`
     - `import gdutils`
     - References like `gdutils.something()`

2. Documentation/Meta:
   - README.md: Update all references and examples
   - .gitignore: Check for any gdutils-specific entries
   - Any additional .md files in docs/ or root directory

## Steps

0. Backup (Important!)
   ```bash
   # Create a backup branch
   git checkout -b backup-before-rename
   git push origin backup-before-rename
   # Return to main
   git checkout main
   ```

1. Rename GitHub Repository (✓ DONE)
   - In GitHub web UI: Settings -> rename repository from 'gdutils' to 'gjdutils'
   - Update local git remote:
     ```bash
     git remote set-url origin https://github.com/gregdetre/gjdutils.git
     ```
   - Verify: `git remote -v`

2. Local Development Changes
   a. Create a new branch for rename changes:
      ```bash
      git checkout -b rename-to-gjdutils
      ```
   
   b. Update configuration files:
      - ✓ Update version to 0.2.0 in __VERSION__.py
      - ✓ Update pyproject.toml with new name and URLs
      - ✓ Update README.md with new package name
      - ✓ Review other documentation files
   
   c. Rename the local directory:
      ```bash
      # From the parent directory containing gdutils/
      mv gdutils gjdutils
      ```
   
   d. Update all internal imports and references

3. Testing
   - ✓ Run existing tests to ensure they pass
   - ✓ Test local import: `pip install -e .`
   - ✓ Verify imports work

## Progress Tracking

### ✓ Completed Steps
- ✓ Created backup branch
- ✓ Renamed GitHub repository
- ✓ Updated local git remote
- ✓ Updated version to 0.2.0 in __VERSION__.py
- ✓ Updated pyproject.toml with new name and URLs
- ✓ Renamed source directory from src/gdutils to src/gjdutils
- ✓ Updated imports in Python files to use gjdutils
- ✓ Updated test files to use gjdutils
- ✓ Fixed package __init__.py to expose version
- ✓ Verified all tests are passing
- ✓ Committed all changes to rename-to-gjdutils branch
- ✓ Merged rename-to-gjdutils to main
- ✓ Tagged v0.2.0

### Files Updated
- [x] pyproject.toml
- [x] __VERSION__.py
- [x] tests/test_gdutils.py (imports updated)
- [x] All Python files in src/gjdutils/ (imports updated)
- [x] README.md

## Next Steps
See @250215_publishing_to_pypi.md for next steps on publishing to PyPI.



