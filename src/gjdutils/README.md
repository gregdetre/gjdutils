# gjdutils

A collection of useful utility functions (strings, dates, data science/AI, web development, types, etc).

This is a smorgasbord of utility functions, patterns and convenient wrappers that I've found myself rewriting and reusing across multiple projects, gathered into one place.

Probably many of these exist elsewhere in libraries - if so, please let me know, because I'd probably rather use something cleaner and better-maintained.

Caveat emptor: some of these are old, and haven't been tested in a while.


## Highlights

### Audio: convenient microphone voice recognition with Whisper, and text-to-speech using ElevenLabs
```python
from gjdutils.outloud_text_to_speech import outloud
from gjdutils.voice_speechrecognition import recognise_speech

# Record speech and play it back in a different voice
text = recognise_speech("Say something!")  # Records from microphone until you press ENTER
outloud(text, prog="elevenlabs", mp3_filen="recording.mp3", should_play=True)  # Plays back what you said
```


### Run shell commands clearly & conveniently
```python
from gjdutils.cmd import run_cmd
from pathlib import Path

# Get Python version and capture the output
retcode, stdout, extra = run_cmd(
    "python --version",  # you can also provide as a list-of-strings
    before_msg="Checking Python version...",
    fatal_msg="Some problem running Python",  # will show up in red, sys.exit(1)
    verbose=0,  # Run silently unless there's an error
    **{"timeout": 5}  # Pass additional arguments to subprocess
)
print(f"Python version: {stdout}")  # e.g. "Python 3.9.7"
print(f"Ran command: {extra['cmd_str']}")  # plus lots of other stuff stored
```


### Environment variables with type validation and helpful error messages
```python
from gjdutils.env import get_env_var

api_key = get_env_var("OPENAI_API_KEY")  # Ensures non-empty by default
num_workers = get_env_var("NUM_WORKERS", typ=int)  # Validates and converts to int
```

To load environment variables from a `.env` file into your shell:
```bash
# First install gjdutils
pip install gjdutils

# Then source the export script with your .env file
source gjdutils-export-envs .env
```

### Strict Jinja templating that catches both undefined and unused variables
```python
from gjdutils.strings import jinja_render

template = "{{name}} is {{age}} years old"
context = {"name": "Bob", "unused": True}
text = jinja_render(template, context)  # will fail both because `age` is missing and `unused` is superfluous
```


### Set random seeds across Python, NumPy, PyTorch for reproducibility
```python
from gjdutils.rand import set_seeds

set_seeds(42)  # Sets seeds for random, numpy, torch if available
```


### Call Claude/OpenAI APIs with function calling, image analysis & JSON support
```python
from gjdutils.llms_claude import call_claude_gpt
from gjdutils.llm_utils import image_to_base64

response, extra = call_claude_gpt(
    "What's in this image?",
    image_filens=["path/to/image.jpg"],
    temperature=0.001
)
```


### Translate text between languages with Google Translate
```python
from gjdutils.google_translate import translate_text, detect_language

# First detect the language
text = "Bonjour le monde"
lang, confidence = detect_language(text)  # Returns ("fr", 0.98)

# Then translate to English
english_text, _ = translate_text(text, lang_src_code=lang, lang_tgt_code="en")  # Returns "Hello world"
```


### Calculate text similarity using longest common substring analysis
```python
from gjdutils.strings import calc_proportion_longest_common_substring
similarity = calc_proportion_longest_common_substring(["hello world", "hello there"])  # Returns ~0.45 for "hello" match
```


### Measure data uniformity & distribution with simple proportion analysis
```python
from gjdutils.dsci import calc_proportion_identical
uniformity = calc_proportion_identical(['a', 'a', 'a', 'b'])  # Returns 0.75 (75% are 'a')
```


### Generate deterministic cache keys for complex Python objects
```python
from gjdutils.caching import generate_mckey
cache_key = generate_mckey("myprefix", {"a": 100, "b": "foo"})  # Creates deterministic cache key
```


### Generate consistent hashes for caching/comparison
```python
from gjdutils.hashing import hash_readable

# Same input always produces same hash, even across sessions
config = {"foo": "bar"}
cache_key = hash_readable(config)  # e.g. "8f4e5d3..."
```


### Pretty-print and process HTML with customizable indentation
```python
from gjdutils.html import prettify_html

# Prettify a string of HTML (also useful for testing two HTML strings are identical without caring about whitespace)
html = "<div><p>Hello</p><p>World</p></div>" # Also works with BeautifulSoup elements
pretty = prettify_html(html, indent=4)  # Custom indentation
print(pretty)
# <div>
#     <p>Hello</p>
#     <p>World</p>
# </div>
```


### Debug by printing local variables, excluding noise
```python
from gjdutils.misc import print_locals

def my_function(x, y):
    z = x + y
    some_func = lambda x: x * 2
    _internal = "temp"
    # Print all local vars except functions and _prefixed
    print_locals(locals(), ignore_functions=True, ignore_underscores=True)
    # Output: {'x': 1, 'y': 2, 'z': 3}
```


### Generate readable random IDs (no confusing characters)
```python
from gjdutils.rand import gen_readable_rand_id

# Generate random ID without confusing chars (0/O, 1/I/l, etc)
uid = gen_readable_rand_id(n=7)  # e.g. "k8m5p3h"
```

----

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
python -m gjdutils.scripts.install_all_dev_dependencies
```


### Adding to requirements.txt

To add to your `requirements.txt` in editable mode, e.g. to install all optional dependencies:
```text
-e "git+https://github.com/gregdetre/gjdutils.git#egg=gjdutils[all_no_dev]"
```

## For gjdutils Developers

### Deployment Process

When you're ready to deploy a new version of `gjdutils`, follow these steps:

- Update the version number in `src/gjdutils/__version__.py`
- Ensure your Git working directory is clean (no uncommitted changes)
- Run the deployment scripts in this order:

```bash
# Test locally first (builds package and runs tests in a fresh venv)
python -m scripts.check_locally

# Deploy to PyPI Test and verify
python -m scripts.deploy_pypitest
python -m scripts.check_pypitest

# Deploy to PyPI Production and verify
python -m scripts.deploy_pypiprod
python -m scripts.check_pypiprod

# Or use the all-in-one deployment script that runs all the above
python -m scripts.deploy_all
```

Each script will:
- Verify prerequisites (git status, version numbers, etc.)
- Ask for confirmation before making changes
- Clean build directories
- Build and test the package
- Upload to the appropriate PyPI repository
- Verify the upload was successful

Note: The deployment scripts require you to have appropriate PyPI credentials configured.

### Setting Up Environment Variables

To set environment variables for development or testing, use the `gjdutils-export-envs` command:

1. Create a `.env` file with your environment variables:
```bash
# .env example
OPENAI_API_KEY=your-key-here
NUM_WORKERS=4
```

2. Source the script to load the variables:
```bash
source gjdutils-export-envs .env
```

This will export all non-commented variables from your `.env` file into your current shell session. You can verify it worked by checking any variable:
```bash
echo $OPENAI_API_KEY
```

## Command Line Interface

`gjdutils` comes with several helpful command-line tools:

```bash
# Show version information
gjdutils version

# PyPI package management commands
gjdutils pypi check local  # Test package installation locally
gjdutils pypi check test   # Test package from Test PyPI
gjdutils pypi check prod   # Test package from Production PyPI

gjdutils pypi deploy test  # Deploy to Test PyPI
gjdutils pypi deploy prod  # Deploy to Production PyPI
gjdutils pypi deploy all   # Run full deployment process (local -> test -> prod)

# Export environment variables from a .env file (must be sourced)
source gjdutils-export-envs .env
```
