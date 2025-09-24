# ChatGPT Image Generation (CLI + Python)

Last updated: 2025-09-24

## Overview

This doc covers a minimal command-line tool and Python usage to generate images with OpenAI's image generation API using the `gpt-image-1` model. It supports key parameters (model, n, seed, size or aspect_ratio), and writes images to files. It also supports providing existing images as inputs for edits and variations.

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
# Basic generation (text-to-image)
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
- `--embed-metadata/--no-embed-metadata`: when output is `.png`, embeds prompt and key parameters
  as PNG text chunks (`Prompt`, `Parameters` JSON). Default: embed.
- `--mode`: one of `generate` (default), `edit`, `variation`
- `--input|-i`: input image path(s). Required for `variation` (exactly 1). Required for `edit` (one or more; multiple images may be supported depending on SDK version).
- `--mask`: optional PNG mask (transparent regions indicate areas to edit). Used with `--mode edit`.

Examples:

```bash
# Square 1k image (generate)
gjdutils images generate "a cozy reading nook, soft sunlight, cinematic" -o nook.png --size 1024x1024

# Portrait aspect ratio (generate)
gjdutils images generate "a portrait of an astronaut in watercolor" -o astro.png --aspect-ratio 9:16

# Multiple outputs (generate)
gjdutils images generate "logo concepts for a mindful journaling app" -o logo.png --n 4 --size 512x512

# Edit an image in a masked region (edit)
gjdutils images generate "Add a red scarf around the cat's neck" \
  -i cat.png --mask mask.png \
  --mode edit --size 1024x1024 -o cat_scarf.png

# Edit with multiple input images (if supported by your SDK/version)
gjdutils images generate "Blend the style of style.png into subject.png" \
  -i subject.png -i style.png \
  --mode edit -o blended.png

# Create variations of an existing image (variation)
# Note: this endpoint doesn't require a prompt; pass a short placeholder if desired
gjdutils images generate "." -i logo.png --mode variation --n 4 --size 512x512 -o logo_var.png
```

## Python usage (library)

The CLI is implemented in `gjdutils/src/gjdutils/cli/images.py`. Programmatically, the underlying patterns are:

```python
# Text-to-image (generate)
from openai import OpenAI
import base64, pathlib

client = OpenAI()  # uses OPENAI_API_KEY from env
result = client.images.generate(
    model="gpt-image-1",
    prompt="A watercolor painting of a fox in a forest",
    n=1,
    size="1024x1024",
)
img_b64 = result.data[0].b64_json
pathlib.Path("fox.png").write_bytes(base64.b64decode(img_b64))

# Image edit (image + optional mask)
with open("cat.png", "rb") as image_f, open("mask.png", "rb") as mask_f:
    result = client.images.edits(
        model="gpt-image-1",
        image=image_f,           # or [image1_f, image2_f] if supported by your SDK version
        mask=mask_f,             # optional
        prompt="Add a red scarf around the cat's neck",
        n=1,
        size="1024x1024",
    )
img_b64 = result.data[0].b64_json
pathlib.Path("cat_scarf.png").write_bytes(base64.b64decode(img_b64))

# Image variation (single image, no mask)
with open("logo.png", "rb") as image_f:
    result = client.images.variations(
        model="gpt-image-1",
        image=image_f,
        n=4,
        size="512x512",
    )
for i, item in enumerate(result.data, start=1):
    pathlib.Path(f"logo_var_{i}.png").write_bytes(base64.b64decode(item.b64_json))
```

## Key concepts

- **Model**: `gpt-image-1` is OpenAI's image generation model.
- **Determinism**: `seed` parameter is accepted but may not be honored by the API; OpenAI's image generation doesn't guarantee deterministic results even with the same seed. Default is 42 for consistency.
- **Sizing vs aspect ratio**: pass `size` for explicit pixel dimensions or `aspect_ratio` for flexible sizing while constraining proportions. Provide only one. Some endpoints (edits/variations) may only support a subset of sizes; if a size is unsupported, use a standard square size like `1024x1024`.
- **Batching**: `n` images per prompt in one call. The CLI writes multiple files when `n > 1`.

## Best practices

- **Keep prompts clear**: specify style, subject, medium, and constraints.
- **Use `--seed 42`**: for consistency across generations (though results may still vary).
- **Save with versioning**: pick filenames that encode prompt or seed, or save to a dated folder.
- **Embed metadata**: keep `--embed-metadata` on to preserve the prompt/parameters inside PNG files.

## Common gotchas

- Providing both `--size` and `--aspect-ratio` will error; they are mutually exclusive.
- Missing `OPENAI_API_KEY`: export it or place it in `.env.local`.
- Streaming is not applicable for image bytes; the CLI warns and proceeds synchronously.
- `variation` requires exactly one `-i/--input` image.
- `edit` requires at least one `-i/--input` image and can optionally include `--mask`. Multiple input images may or may not be supported depending on your OpenAI SDK version.

## Resources

- OpenAI Images API docs: `https://platform.openai.com/docs/guides/images`
- OpenAI Python SDK: `https://github.com/openai/openai-python`

## Changelog

- 2025-09-24: Initial version, adds `gjdutils images generate` CLI and this reference.
- 2025-09-24: Add `--mode`, `--input`, `--mask` for edits and variations; update examples.
