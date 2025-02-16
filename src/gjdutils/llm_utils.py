import base64
import io
import json
from typing import Any, Literal, Optional

from anthropic import Anthropic
from openai import OpenAI

from gjdutils.llms_claude import call_claude_gpt
from gjdutils.llms_openai import call_openai_gpt
from gjdutils.strings import jinja_render


MODEL_TYPE = Literal["openai", "claude"]


def proc_llm_out_json(s: str):
    # TODO probably we don't need this function any more, because OpenAI will guarantee JSON output
    """
    If GPT-4 returns json output like this:

    ```json
    ...
    ```

    This strips away that markdown wrapping.

    Alternatively, consider using llm_prompt_json()
    """
    s = s.strip()
    # remove the markdown code wrapping
    if s.startswith("```json") and s.endswith("```"):
        s = s[7:-3]
    try:
        j = json.loads(s)
    except json.JSONDecodeError:
        print("Failed to parse JSON:", s)
        raise
    return j


def image_to_base64_resized(image_full_filen: str, resize_target_size_kb: int = 100):
    from PIL import Image

    # based on https://claude.ai/chat/d0eb1f39-3f42-4cb5-a2ec-5aa102c60ea0
    assert resize_target_size_kb > 0
    with Image.open(image_full_filen) as img_orig:
        width_orig, height_orig = img_orig.size
        # Calculate initial file size
        temp_buffer = io.BytesIO()
        img_orig.save(temp_buffer, format=img_orig.format)
        img_resized = img_orig.copy()
        current_size_kb = len(temp_buffer.getvalue()) / 1024

        # Iteratively resize until file size is below target
        resize_factor = 0.9
        while current_size_kb > resize_target_size_kb:
            resize_factor *= resize_factor
            width = int(width_orig * resize_factor)
            height = int(height_orig * resize_factor)
            img_resized = img_orig.resize(
                (width, height), Image.LANCZOS  # type: ignore
            )  #  type: ignore
            # Check new file size
            temp_buffer = io.BytesIO()
            img_resized.save(temp_buffer, format=img_orig.format)
            current_size_kb = len(temp_buffer.getvalue()) / 1024

        # Convert final resized image to base64
        img_bytes = io.BytesIO()
        img_resized.save(img_bytes, format=img_orig.format)
        img_buffer = img_bytes.getvalue()

    return img_buffer


def image_to_base64(img_full_filen: str, resize_target_size_kb: Optional[int] = None):
    # from https://chat.openai.com/c/35f15af9-b947-4fa6-acbe-2a5ed26e7547
    if resize_target_size_kb is None:
        with open(img_full_filen, "rb") as image_file:
            img_bytes = image_file.read()
    else:
        img_bytes = image_to_base64_resized(img_full_filen, resize_target_size_kb)
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")
    return img_b64


def image_to_base64_basic(image_filen: str) -> str:
    with open(image_filen, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("ascii")


def contents_for_images(image_filens: list[str], resize_target_size_kb: int):
    # assert (
    #     1 <= len(image_filens) <= 10
    # ), "You can only provide between 1 and 10 images"
    base64_images = []
    new_contents = []
    for image_filen in image_filens:
        base64_image = image_to_base64(
            image_filen, resize_target_size_kb=resize_target_size_kb
        )
        filen_content = {
            "type": "text",
            "text": f"Filename: {image_filen}",
        }
        img_content = {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
        }
        base64_images.append(base64_image)
        new_contents.extend([filen_content, img_content])
    return new_contents, base64_images


def generate_gpt_from_template(
    client: Anthropic | OpenAI,
    prompt_template_var: str,
    context_d: dict,
    response_json: bool,
    image_filens: list[str] | str | None = None,
    model_type: MODEL_TYPE = "claude",
    max_tokens: Optional[int] = None,
    prompt_template_filen: str = "prompt_templates",  # i.e. prompt_templates.py
    verbose: int = 0,
) -> tuple[str | dict[str, Any], dict[str, Any]]:
    """
    e.g.
        generate_gpt_from_template("quick_search_for_word", {"word_tgt": word}, True, verbose)
    """
    # dynamically import `template_var` from prompt_templates as `prompt_template`
    prompt_template = getattr(__import__(prompt_template_filen), prompt_template_var)
    prompt = jinja_render(prompt_template, context_d)
    if model_type == "openai":
        assert isinstance(client, OpenAI), "Expected OpenAI client"
        out, _, extra = call_openai_gpt(
            prompt,
            client=client,
            image_filens=image_filens,
            response_json=response_json,
            max_tokens=max_tokens,
        )
    else:
        assert isinstance(client, Anthropic), "Expected Anthropic client"
        out, extra = call_claude_gpt(
            prompt,
            client=client,
            image_filens=image_filens,
            response_json=response_json,
            max_tokens=max_tokens if max_tokens is not None else 4096,
        )
    if response_json:
        assert isinstance(out, dict), f"Expected dict, got {type(out)}"
    else:
        assert isinstance(out, str), f"Expected str, got {type(out)}"
    if verbose >= 1:
        print(
            f"Called GPT on '{prompt_template_var}', context keys {list(context_d.keys())}"
        )
    extra.update(
        {
            "model_type": model_type,
            "prompt_template": prompt_template_var,
            "prompt_context_d": context_d,
        }
    )
    return out, extra  # type: ignore
