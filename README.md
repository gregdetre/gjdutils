# gjdutils

A collection of useful utility functions (strings, dates, data science/AI, web development, types, etc).

## Installation

```bash
pip install gjdutils
```

For optional features:
```bash
pip install "gjdutils[dt]"   # Date/time utilities
pip install "gjdutils[llm]"  # AI/LLM integrations
pip install "gjdutils[audio_lang]"  # Speech/translation, language-related
pip install "gjdutils[html_web]"    # Web scraping

pip install "gjdutils[dev]"  # Development tools (for tweaking `gjdutils` itself, e.g. pytest)

# Install all optional dependencies at once (except `dev`, which is used for developing `gjdutils` itself)
pip install "gjdutils[all_no_dev]"
```

### Development Setup

If you're developing `gjdutils` itself, install in editable mode:
```bash
# (Assumes you have already setup your virtualenv)
# from the gjdutils root directory
pip install -e ".[all_no_dev, dev]"     # Install all optional dependencies
```

Or if you're feeling lazy and can't remember that command, just use:

```bash
python scripts/install_all_dev_dependencies.py
```


### Adding to requirements.txt

To add to your `requirements.txt` in editable mode, e.g. to install all optional dependencies:
```text
-e "git+https://github.com/gregdetre/gjdutils.git#egg=gjdutils[all_no_dev]"
```
