# Publishing gjdutils to PyPI

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
   
   b. Update configuration files (✓ IN PROGRESS):
      - ✓ Update version to 0.2.0 in __VERSION__.py
      - ✓ Update pyproject.toml with new name and URLs
      - ✓ Update README.md with new package name
      - Review other documentation files
   
   c. Rename the local directory:
      ```bash
      # From the parent directory containing gdutils/
      mv gdutils gjdutils
      ```
   
   d. Update all internal imports and references

3. Testing
   - Run existing tests to ensure they pass
   - Test local import: `pip install -e .`
   - Verify imports work in Python:
     ```python
     import gjdutils
     # Test key functionality
     ```

4. Test PyPI Deployment
   - Delete existing gdutils from test.pypi.org
   - Build package: `python -m build`
   - Upload to test.pypi.org: `twine upload -r testpypi dist/*`
   - Test installation: `pip install -i https://test.pypi.org/simple/ gjdutils`

5. Production PyPI Deployment
   - Upload to PyPI: `twine upload dist/*`
   - Verify installation: `pip install gjdutils`

## Dependencies
Currently managed in pyproject.toml with optional features:
- audio_lang: Speech/translation utilities
- dev: Development tools (black, pytest)
- dt: Date/time utilities
- html_web: Web scraping tools
- llm: AI/LLM integrations

## Notes
- Using hatchling for build system
- Requires Python >=3.10
- MIT License

## Prerequisites
- Python >=3.10
- Build tools: `pip install build twine`
- PyPI account with 2FA configured
- .pypirc file configured with test and prod PyPI credentials

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

### Current State
- On branch `rename-to-gjdutils`
- All files moved and imports updated
- All changes committed
- Tests passing

### Next Steps
1. Final documentation review:
   - Review README.md for any remaining gdutils references
   - Check any other documentation files in the repository

2. Build and test package:
   ```bash
   # Build the package
   python -m build
   
   # Upload to test.pypi.org
   twine upload -r testpypi dist/*
   
   # Test installation from test.pypi.org
   pip install -i https://test.pypi.org/simple/ gjdutils
   ```

3. If test deployment successful:
   - Upload to production PyPI: `twine upload dist/*`
   - Test installation: `pip install gjdutils`
   - Test basic functionality

4. Post-deployment:
   - Merge rename-to-gjdutils branch to main
   - Tag release v0.2.0
   - Update GitHub release notes

### Files Needing Updates
- [x] pyproject.toml
- [x] __VERSION__.py
- [x] tests/test_gdutils.py (imports updated)
- [x] All Python files in src/gjdutils/ (imports updated)
- [ ] README.md (needs final review)

## File Changes Tracking

### ✓ Configuration Files (Done)
- ✓ pyproject.toml
- ✓ __VERSION__.py
- ✓ README.md
- ✓ .gitignore (no changes needed)

### Python Files (To Do)
Files needing import updates:
```
# Will list files here after grep
```

Changes needed:
- `from gdutils import ...` → `from gjdutils import ...`
- `import gdutils` → `import gjdutils`
- Any string literals containing 'gdutils'
- Any references in docstrings or comments



