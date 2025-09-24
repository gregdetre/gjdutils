import base64
import io
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List

import typer

from openai import OpenAI, NOT_GIVEN

from gjdutils.env import get_env_var


app = typer.Typer(
    help="Generate images via OpenAI from the command line",
    add_completion=True,
    no_args_is_help=True,
    context_settings={"help_option_names": ["-h", "--help"]},
)


class ImageMode(str):
    GENERATE = "generate"
    EDIT = "edit"
    VARIATION = "variation"


def _ensure_api_key_loaded(env_file: Optional[Path]) -> str:
    """Return OPENAI_API_KEY, attempting to load from an env file if needed.

    This prefers the already-exported environment variable. If missing and an
    env_file is provided and exists (e.g., ".env.local"), it will be parsed
    minimally to set the variable for the current process.
    """
    try:
        return get_env_var("OPENAI_API_KEY")
    except Exception:
        if env_file and env_file.exists():
            # Minimal parser to avoid extra dependencies; supports KEY=VALUE lines
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    continue
                key, value = line.split("=", 1)
                key = key.strip()
                value = value.strip().strip('"').strip("'")
                if key == "OPENAI_API_KEY" and value:
                    # Late import to avoid polluting env unless needed
                    import os

                    os.environ[key] = value
                    break
        # Try again (will raise if still missing)
        return get_env_var("OPENAI_API_KEY")


@app.command()
def generate(
    prompt: str = typer.Argument(..., help="Text prompt to generate the image(s) for."),
    out: Path = typer.Option(
        Path("image.png"),
        "--out",
        "-o",
        help="Output filename. If n>1, suffixes like _1, _2 are added before extension.",
    ),
    model: str = typer.Option(
        "gpt-image-1", "--model", help="OpenAI image model to use. Default: gpt-image-1",
    ),
    n: int = typer.Option(1, "--n", help="Number of images to generate. Default: 1"),
    seed: int = typer.Option(42, "--seed", help="Random seed for reproducibility. Default: 42"),
    stream: bool = typer.Option(
        False,
        "--stream/--no-stream",
        help="Stream server events (not currently supported for images). Default: no-stream",
    ),
    size: Optional[str] = typer.Option(
        "1024x1024",
        "--size",
        help="Image size, e.g. 256x256, 512x512, 1024x1024. Mutually exclusive with --aspect-ratio.",
    ),
    aspect_ratio: Optional[str] = typer.Option(
        None,
        "--aspect-ratio",
        help="Image aspect ratio, e.g. 1:1, 16:9, 9:16. Mutually exclusive with --size.",
    ),
    env_file: Optional[Path] = typer.Option(
        Path(".env.local"),
        "--env-file",
        help="Path to env file containing OPENAI_API_KEY. Default: .env.local",
    ),
    embed_metadata: bool = typer.Option(
        True,
        "--embed-metadata/--no-embed-metadata",
        help="Embed prompt and parameters in PNG metadata (if output is .png). Default: embed",
    ),
    mode: str = typer.Option(
        ImageMode.GENERATE,
        "--mode",
        help="Operation mode: generate (default), edit, or variation",
    ),
    input: Optional[List[Path]] = typer.Option(
        None,
        "--input",
        "-i",
        help="Path(s) to input image(s). Used with --mode edit (1+ images) or variation (exactly 1).",
    ),
    mask: Optional[Path] = typer.Option(
        None,
        "--mask",
        help="Optional mask image (PNG with transparent regions to edit). Used with --mode edit.",
    ),
):
    """Generate one or more images and write them to disk."""

    # stream flag accepted for API parity; not used by this SDK call

    _ = _ensure_api_key_loaded(env_file)

    client = OpenAI()  # picks up OPENAI_API_KEY from env

    # Determine effective size. Some SDK versions accept only size, not aspect_ratio.
    # Map common aspect ratios to supported sizes when provided.
    def map_aspect_ratio_to_size(ratio: str) -> str:
        r = ratio.strip()
        # Allowed sizes (as of current SDK): 1024x1024, 1024x1536 (portrait), 1536x1024 (landscape)
        if r in {"1:1", "1x1"}:
            return "1024x1024"
        if r in {"16:9", "16x9"}:
            return "1536x1024"
        if r in {"9:16", "9x16"}:
            return "1024x1536"
        # Fallback: default square
        return "1024x1024"

    effective_size = size if size else "1024x1024"
    if aspect_ratio:
        effective_size = map_aspect_ratio_to_size(aspect_ratio)

    # Branch by mode
    result = None
    mode_normalized = (mode or ImageMode.GENERATE).lower().strip()

    if mode_normalized == ImageMode.GENERATE:
        # Ignore input/mask if provided
        result = client.images.generate(
            model=model,
            prompt=prompt,
            n=n,
            size=effective_size,  # type: ignore[arg-type]
        )

    elif mode_normalized == ImageMode.EDIT:
        # Require at least one input image
        if not input or len(input) == 0:
            raise typer.BadParameter("--input is required for --mode edit (one or more images).")

        # Open input files
        image_files = [p for p in input]
        opened_images = []
        opened_mask = None
        try:
            for p in image_files:
                opened_images.append(p.open("rb"))
            if mask is not None:
                opened_mask = mask.open("rb")

            # Pass single file or list depending on count
            image_param = opened_images[0] if len(opened_images) == 1 else opened_images

            result = client.images.edits(
                model=model,
                image=image_param,  # type: ignore[arg-type]
                mask=opened_mask if opened_mask is not None else NOT_GIVEN,
                prompt=prompt,
                n=n,
                size=effective_size,  # type: ignore[arg-type]
            )
        finally:
            for f in opened_images:
                try:
                    f.close()
                except Exception:
                    pass
            if opened_mask is not None:
                try:
                    opened_mask.close()
                except Exception:
                    pass

    elif mode_normalized == ImageMode.VARIATION:
        # Require exactly one input image
        if not input or len(input) != 1:
            raise typer.BadParameter("--input must be provided exactly once for --mode variation.")
        image_path = input[0]
        with image_path.open("rb") as f:
            result = client.images.variations(
                model=model,
                image=f,
                n=n,
                size=effective_size,  # type: ignore[arg-type]
            )

    else:
        raise typer.BadParameter("--mode must be one of: generate, edit, variation")

    # Write images to files
    data_items = getattr(result, "data", None) or []
    if not data_items:
        raise typer.Exit(code=1)

    def _write_item(idx: int, item, path: Path):
        b64 = getattr(item, "b64_json", None)
        if b64:
            image_bytes = base64.b64decode(b64)
            path.parent.mkdir(parents=True, exist_ok=True)
            if embed_metadata and path.suffix.lower() == ".png":
                try:
                    from PIL import Image
                    from PIL.PngImagePlugin import PngInfo

                    meta = {
                        "prompt": prompt,
                        "model": model,
                        "n": n,
                        "seed": seed,
                        "size": size,
                        "aspect_ratio": aspect_ratio,
                        "effective_size": effective_size,
                        "openai_created": getattr(result, "created", None),
                        "generator": "gjdutils images generate",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                    }
                    img = Image.open(io.BytesIO(image_bytes))
                    pnginfo = PngInfo()
                    pnginfo.add_text("Prompt", prompt)
                    pnginfo.add_text("Parameters", json.dumps(meta, ensure_ascii=False))
                    img.save(path, format="PNG", pnginfo=pnginfo)
                    typer.echo(f"Wrote {path} (with metadata)")
                    return
                except Exception:
                    # Fallback to raw bytes
                    pass
            path.write_bytes(image_bytes)
            typer.echo(f"Wrote {path}")
            return
        url = getattr(item, "url", None)
        if url:
            try:
                import requests  # optional
            except Exception:
                raise typer.Exit(code=2)
            resp = requests.get(url, timeout=60)
            resp.raise_for_status()
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(resp.content)
            typer.echo(f"Wrote {path}")
            return
        raise typer.Exit(code=1)

    if n == 1:
        _write_item(1, data_items[0], out)
        return

    stem = out.stem
    suffix = out.suffix or ".png"
    parent = out.parent
    for idx, item in enumerate(data_items, start=1):
        out_i = parent / f"{stem}_{idx}{suffix}"
        _write_item(idx, item, out_i)


if __name__ == "__main__":
    app()


