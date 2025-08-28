# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

see also: `README.md`

## Development Commands

**Setup:**
```bash
# Install in editable mode with all dependencies
pip install -e ".[all_no_dev, dev]"

# Or use the convenience script
python -m gjdutils.scripts.install_all_dev_dependencies
```

**Testing:**
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_strings.py

# Run with verbose output
pytest -v
```

**Linting:**
```bash
# Format code (uses black)
black src/ tests/

# Lint code (uses flake8)
flake8 src/ tests/
```

**Building:**
```bash
# Build package
python -m build

# Clean build directories
rm -rf dist/ build/ *.egg-info/
```

**PyPI Deployment:**
```bash
# Full deployment workflow (includes all checks)
gjdutils pypi deploy all

# Individual steps
gjdutils pypi check local    # Test locally
gjdutils pypi deploy test    # Deploy to Test PyPI
gjdutils pypi deploy prod    # Deploy to Production PyPI
```

## Architecture Overview

**Module Organization:**
- **Core utilities**: `strings`, `files`, `dicts`, `lists`, `functions` - fundamental data manipulation
- **System interaction**: `cmd`, `shell`, `env`, `runtime` - process execution and environment management  
- **AI/LLM**: `llm_utils`, `llms_claude`, `llms_openai` - unified interface for AI services
- **Data science**: `dsci`, `num`, `indexing` - analysis and numerical operations
- **Audio/Voice**: `audios`, `voice_speechrecognition`, `outloud_text_to_speech` - speech processing
- **Web/HTML**: `html`, `web`, `google_translate` - web scraping and content processing

**CLI Structure:**
Built with Typer in hierarchical command groups:
- Main app in `cli/main.py` registers subcommands
- PyPI management in `cli/pypi/` (check, deploy commands)
- Utility commands: `check-git-clean`, version display
- Special entry point: `gjdutils-export-envs` for shell environment setup

**Key Patterns:**
- **Optional dependencies**: Features grouped by domain (`audio_lang`, `llm`, `dsci`, etc.)
- **Error handling**: Uses `gjdutils.shell.fatal_error_msg()` for CLI error reporting
- **Versioning**: Dynamic version from `__version__.py`, integrated into deployment checks
- **Environment management**: `.env` file support with shell script generation

**Testing Strategy:**
- Integration tests for CLI commands in `test_cli.py`
- Environment variable testing in `test_env_integration.py`
- Unit tests follow `test_{module}.py` naming convention
- Uses pytest with typer testing utilities

**Deployment Process:**
1. Update version in `__version__.py`
2. Ensure git working directory is clean
3. Use `gjdutils pypi deploy all` for full automated workflow
4. Each step includes verification and rollback capabilities