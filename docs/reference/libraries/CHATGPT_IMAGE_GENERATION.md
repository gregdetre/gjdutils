# ChatGPT Image Generation (CLI + Python)

Last updated: 2025-09-24

## Overview

This doc covers a minimal command-line tool and Python usage to generate images with OpenAI's image generation API using the `gpt-image-1` model. It supports key parameters (model, n, seed, size or aspect_ratio), and writes images to files.

- Default model: `gpt-image-1`
- Default n: `1`
- Default seed: `42`
- Stream: not used for images
- Provide either `--size` or `--aspect-ratio` (mutually exclusive)

## Use cases

- Quickly iterate on prompts from the terminal
- Scriptable image batch generation
- Deterministic-ish results with a fixed `--seed`

## Getting started

1) Ensure you have an OpenAI API key available in your environment. The CLI will try to read `OPENAI_API_KEY` from your environment, or fall back to parsing `.env.local`.

2) The CLI is available under the `gjdutils` Typer app: `gjdutils images generate`.

3) Install optional dependency group (if needed for OpenAI client):

```bash
pip install "gjdutils[llm]"
```

This includes `openai` and `pillow` (pillow is not required by the CLI; `openai` is).

## CLI reference

Command:

```bash
gjdutils images generate "A watercolor painting of a fox in a forest" \
  --out fox.png \
  --model gpt-image-1 \
  --n 1 \
  --seed 42 \
  --size 1024x1024
```

- `prompt` (positional): text prompt
- `--out|-o`: output filename. If `--n > 1`, files will be suffixed `_1`, `_2`, ...
- `--model`: default `gpt-image-1`
- `--n`: default `1`
- `--seed`: default `42`
- `--size`: e.g., `256x256`, `512x512`, `1024x1024`
- `--aspect-ratio`: e.g., `1:1`, `16:9`, `9:16` (mutually exclusive with `--size`)
- `--env-file`: defaults to `.env.local`; parsed only if `OPENAI_API_KEY` missing from env
- `--stream/--no-stream`: accepted but images are returned non-streaming

Examples:

```bash
# Square 1k image
gjdutils images generate "a cozy reading nook, soft sunlight, cinematic" -o nook.png --size 1024x1024

# Portrait aspect ratio
gjdutils images generate "a portrait of an astronaut in watercolor" -o astro.png --aspect-ratio 9:16

# Multiple outputs
gjdutils images generate "logo concepts for a mindful journaling app" -o logo.png --n 4 --size 512x512
```

## Python usage (library)

The CLI is implemented in `gjdutils/src/gjdutils/cli/images.py`. Programmatically, the underlying pattern is:

```python
from openai import OpenAI

client = OpenAI()  # uses OPENAI_API_KEY from env
result = client.images.generate(
    model="gpt-image-1",
    prompt="A watercolor painting of a fox in a forest",
    n=1,
    seed=42,
    size="1024x1024",      # or aspect_ratio="1:1" (mutually exclusive)
    response_format="b64_json",
)
# Save first image
import base64, pathlib
img_b64 = result.data[0].b64_json
pathlib.Path("fox.png").write_bytes(base64.b64decode(img_b64))
```

## Key concepts

- **Model**: `gpt-image-1` is OpenAI's image generation model.
- **Determinism**: `seed` can stabilize results somewhat; changes to prompts or parameters will still affect outputs.
- **Sizing vs aspect ratio**: pass `size` for explicit pixel dimensions or `aspect_ratio` for flexible sizing while constraining proportions. Provide only one.
- **Batching**: `n` images per prompt in one call. The CLI writes multiple files when `n > 1`.

## Best practices

- **Keep prompts clear**: specify style, subject, medium, and constraints.
- **Use `--seed`**: for iterative experimentation.
- **Save with versioning**: pick filenames that encode prompt or seed, or save to a dated folder.

## Common gotchas

- Providing both `--size` and `--aspect-ratio` will error; they are mutually exclusive.
- Missing `OPENAI_API_KEY`: export it or place it in `.env.local`.
- Streaming is not applicable for image bytes; the CLI warns and proceeds synchronously.

## Resources

- OpenAI Images API docs: `https://platform.openai.com/docs/guides/images`
- OpenAI Python SDK: `https://github.com/openai/openai-python`

## Changelog

- 2025-09-24: Initial version, adds `gjdutils images generate` CLI and this reference.
