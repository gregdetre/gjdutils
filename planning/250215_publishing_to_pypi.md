# Publishing gjdutils to PyPI

## Context
- First release of gjdutils to PyPI
- Version 0.2.0 (after rename from gdutils)
- Package contains utility functions for strings, dates, data science/AI, web development

## Prerequisites
- Python >=3.10
- Build tools: `pip install build twine`
- PyPI account with 2FA configured
- .pypirc file configured with test and prod PyPI credentials

## Steps

1. Build and test package locally:
   ```bash
   # Option 1: Automated testing script (recommended)
   python -m gjdutils.scripts.check_locally
   
   # Option 2: Manual steps
   # Clean any existing builds
   rm -rf dist/ build/
   
   # Build the package
   python -m build
   ```

2. Test PyPI Deployment:
   ```bash
   # Option 1: Automated testing script (recommended)
   python -m gjdutils.scripts.check_test_pypi
   
   # Option 2: Manual steps
   # Upload to test.pypi.org
   twine upload -r testpypi dist/*
   
   # Create a fresh virtualenv for testing
   python -m venv /tmp/test-gjdutils
   source /tmp/test-gjdutils/bin/activate
   
   # Test installation from test.pypi.org (with dependencies from PyPI)
   pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ gjdutils
   
   # Test basic functionality
   python -c "import gjdutils; print(gjdutils.__version__)"
   ```

3. Production PyPI Deployment:
   ```bash
   # Upload to PyPI
   twine upload dist/*
   
   # Create a fresh virtualenv for testing
   python -m venv /tmp/prod-gjdutils
   source /tmp/prod-gjdutils/bin/activate
   
   # Test installation
   pip install gjdutils
   
   # Test basic functionality
   python -c "import gjdutils; print(gjdutils.__version__)"
   ```

## Optional Features
Package has several optional feature sets that can be installed:
```bash
pip install "gjdutils[dt]"        # Date/time utilities
pip install "gjdutils[llm]"       # AI/LLM integrations
pip install "gjdutils[audio_lang]" # Speech/translation
pip install "gjdutils[html_web]"   # Web scraping
pip install "gjdutils[dev]"        # Development tools
```

## Progress Tracking

### Current State
- Package renamed to gjdutils
- Version 0.2.0 ready for release
- All tests passing

### Next Steps
1. Build package:
   - Clean existing builds
   - Run build command
   - Verify dist/ contents

2. Test deployment:
   - Upload to test.pypi.org
   - Test installation in fresh virtualenv
   - Verify basic functionality

3. Production deployment:
   - Upload to PyPI
   - Test installation
   - Verify functionality

### Post-deployment
- [ ] Update GitHub release description
- [ ] Announce release (if needed)
- [ ] Update documentation with PyPI installation instructions 