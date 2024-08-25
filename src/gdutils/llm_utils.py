import base64
import io
from PIL import Image
import json
from typing import Optional


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
    except:
        print(s)
        raise Exception("Could not parse JSON from LLM output")
    return j


def image_to_base64_resized(image_full_filen: str, resize_target_size_kb: int = 100):
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
