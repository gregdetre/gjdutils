from typing import Any, Literal, Optional

from anthropic import Anthropic
from openai import OpenAI

from gjdutils.llms_claude import call_claude_gpt
from gjdutils.llms_openai import call_openai_gpt
from gjdutils.strings import jinja_render


MODEL_TYPE = Literal["openai", "claude"]


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
