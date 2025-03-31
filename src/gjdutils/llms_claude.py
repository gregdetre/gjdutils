import json
from pathlib import Path
from anthropic import Anthropic, NOT_GIVEN
from typing import Optional

from gjdutils.image_utils import image_to_base64_basic
from gjdutils.env import get_env_var


CLAUDE_API_KEY = get_env_var("CLAUDE_API_KEY")
# https://docs.anthropic.com/en/docs/about-claude/models
MODEL_NAME_CLAUDE_SONNET_GOOD_LATEST = "claude-3-7-sonnet-latest"
MODEL_NAME_CLAUDE_SONNET_CHEAP_LATEST = "claude-3-5-haiku-latest"


def img_as_content_dict(img_filen: str):
    media_type_from_extension = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
        ".gif": "image/gif",
        ".bmp": "image/bmp",
        ".tiff": "image/tiff",
        ".ico": "image/vnd.microsoft.icon",
        ".svg": "image/svg+xml",
        ".heic": "image/heic",
        ".heif": "image/heif",
    }

    ext = Path(img_filen).suffix
    if ext not in media_type_from_extension:
        raise ValueError(f"Unknown image file extension: {img_filen}")
    media_type = media_type_from_extension[ext]

    img_base64 = image_to_base64_basic(img_filen)
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": media_type,
            "data": img_base64,
        },
    }


def call_claude_gpt(
    prompt: str,
    tools: Optional[list[dict]] = None,
    image_filens: str | list[str] | None = None,
    image_resize_target_size_kb: Optional[int] = 100,
    client: Optional[Anthropic] = None,
    model: str = MODEL_NAME_CLAUDE_SONNET_GOOD_LATEST,
    temperature: Optional[float] = 0.001,
    response_json: bool = False,
    # seed: Optional[int] = DEFAULT_RANDOM_SEED,
    max_tokens: int = 4096,
    verbose: int = 0,
):
    """Call Claude API with support for text, images, and function calling"""
    from gjdutils.llm_utils import extract_json_from_markdown

    extra = locals()
    extra.pop("client")

    if tools is not None:
        raise NotImplementedError(
            "I think tools are supported, but not implemented in this function"
        )

    if client is None:
        client = Anthropic(api_key=CLAUDE_API_KEY)

    # Prepare image contents if provided
    contents = []
    if image_filens:
        if isinstance(image_filens, str):
            image_filens = [image_filens]
        assert image_resize_target_size_kb is not None
        for i, img_filen in enumerate(image_filens):
            contents.extend(
                [
                    {"type": "text", "text": f"Image {i+1}:"},
                    img_as_content_dict(image_filens[i]),
                    # {
                    #     "type": "image",
                    #     "source": {
                    #         "type": "base64",
                    #         "media_type": "image/jpeg",  # Adjust based on actual image type
                    #         "data": b64,
                    #     },
                    # },
                ]
            )

    # if response_json:
    #     # Add instruction to respond in JSON format - be very explicit
    #     prompt = f"Please provide your response in valid JSON format without any markdown formatting or backticks. Provide ONLY the JSON object, not any explanatory text before or after the JSON. {prompt}"

    contents.append({"type": "text", "text": prompt})

    # not supported
    # response_format = {"type": "json_object"} if response_json else None

    # Make API call
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": contents}],
        temperature=temperature if temperature is not None else NOT_GIVEN,
        # seed=seed,
        # response_format=response_format,
    )

    msg = response.content[0].text  # type: ignore
    if response_json:
        # print("Processing JSON response from Claude...")
        try:
            # print(f"Raw Claude response before JSON parsing: {msg}")

            # Use our utility function to handle markdown-wrapped JSON
            clean_json_text = extract_json_from_markdown(msg, verbose=True)

            msg = json.loads(clean_json_text)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Raw message causing error: {msg}")
            print(f"Cleaned: {clean_json_text}")
            # Return a structured error response instead of failing
            msg = {
                "error": "Failed to parse API response",
                "raw_response": msg[:500] if msg else "Empty response",
            }
    extra.update(
        {
            "response": response.model_dump(),
            "msg": msg,
            # "tool_calls": tool_calls,
            "model": model,
            "contents": contents,
        }
    )

    if verbose >= 2:
        print(f"PROMPT:\n{prompt}")
    if verbose >= 1:
        print(f"LLM MESSAGE:\n{msg}")
    if verbose >= 2:
        # print(f"TOOL CALLS:\n{tool_calls}")
        print(f"LLM RESPONSE:\n{json.dumps(response.model_dump(), indent=2)}")
    return msg, extra
