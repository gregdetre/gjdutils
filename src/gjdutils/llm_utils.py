from typing import Any, Literal, Optional, Union
from pathlib import Path
import json

from anthropic import Anthropic
from openai import OpenAI

from gjdutils.llms_claude import call_claude_gpt
from gjdutils.llms_openai import call_openai_gpt
from gjdutils.strings import jinja_render


MODEL_TYPE = Literal["openai", "claude"]


def extract_json_from_markdown(text: str, verbose: bool = False) -> str:
    """
    Extracts JSON content from text that may be wrapped in markdown code blocks.

    Args:
        text: The text that may contain JSON, possibly within markdown code blocks
        verbose: Whether to print debug information

    Returns:
        A string containing just the JSON content (still as a string, not parsed)
    """
    # If it's already valid JSON, return as is
    try:
        json.loads(text)
        if verbose:
            print("Input is already valid JSON")
        return text
    except json.JSONDecodeError:
        # Not valid JSON, may be wrapped in markdown
        pass

    # Handle JSON wrapped in markdown code blocks
    if text.strip().startswith("```") and "```" in text:
        if verbose:
            print("Detected markdown code block")

        # Extract content between backticks
        parts = text.split("```", 2)
        if len(parts) >= 2:
            extracted = parts[1]  # Get the middle part

            # Remove the language identifier if present
            if extracted.strip().startswith("json"):
                extracted = extracted[4:].strip()
            else:
                extracted = extracted.strip()

            # If there are closing backticks, remove everything from them onwards
            if "```" in extracted:
                extracted = extracted.split("```", 1)[0].strip()

            if verbose:
                print(f"Extracted content from markdown: {extracted[:50]}...")

            return extracted

    # If we got here, we couldn't extract JSON from markdown
    return text


def generate_gpt_from_template(
    client: Anthropic | OpenAI,
    prompt_template: Union[str, Path],
    context_d: dict,
    response_json: bool,
    image_filens: list[str] | str | None = None,
    model_type: MODEL_TYPE = "claude",
    max_tokens: Optional[int] = None,
    verbose: int = 0,
) -> tuple[str | dict[str, Any], dict[str, Any]]:
    """Generate a response from GPT using a template.

    Args:
        client: The Anthropic or OpenAI client
        prompt_template: Either a template string or Path to a template file
        context_d: Dictionary of variables to render in the template
        response_json: Whether to parse the response as JSON
        image_filens: Optional paths to image files to include
        model_type: Which model type to use ("openai" or "claude")
        max_tokens: Maximum tokens in the response
        verbose: Verbosity level
    """
    # Load template content from Path or use string directly
    if isinstance(prompt_template, Path):
        with open(prompt_template, "r") as f:
            template_content = f.read()
        template_name = prompt_template.stem
    else:
        template_content = prompt_template
        template_name = "template from input string"

    prompt = jinja_render(template_content, context_d)
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
        print(f"{out=}")
        print(f"{max_tokens=}")
    if response_json:
        assert isinstance(out, dict), f"Expected dict, got {type(out)}"
    else:
        assert isinstance(out, str), f"Expected str, got {type(out)}"
    if verbose >= 1:
        print(f"Called GPT on '{template_name}', context keys {list(context_d.keys())}")
    extra.update(
        {
            "model_type": model_type,
            "prompt_template": template_name,
            "prompt_context_d": context_d,
        }
    )
    return out, extra  # type: ignore
