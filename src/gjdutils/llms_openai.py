import json
from openai import OpenAI, NOT_GIVEN
from typing import Literal, Optional

from .prompt_templates import summarise_list_of_texts_as_one, summarise_text
from .rand import DEFAULT_RANDOM_SEED
from .strings import jinja_render
from gjdutils.image_utils import contents_for_images
from gjdutils.env import get_env_var


OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")
MODEL_NAME_GPT4 = "gpt-4"
MODEL_NAME_GPT35 = "gpt-3.5-turbo"
MODEL_NAME_GPT4_TURBO = "gpt-4-turbo"  # -1106-preview"
MODEL_NAME_GPT4O = "gpt-4o"
MODEL_NAME_GPT4O_MINI = "gpt-4o-mini"
MODEL_NAME_O1 = "o1-preview"
MODEL_NAME_O1_MINI = "o1-mini"
DEFAULT_MODEL_NAME = MODEL_NAME_GPT4O

MODELS_NO_TOOLS = [MODEL_NAME_O1, MODEL_NAME_O1_MINI]

# from https://github.com/openai/openai-python
ToolChoiceTyps = Literal["auto", "required", "none"]

GranularityTyps = Literal[
    "short phrase of just a few words",
    "short title",
    "short sentence",
    "at most a sentence",
    "sentence or two",
    "few sentences",
    "single short paragraph",
    "couple of paragraphs",
    "page",
]


def call_openai_gpt(
    prompt: str,
    tools: Optional[list[dict]] = None,
    tool_choice: Optional[ToolChoiceTyps] = None,
    image_filens: str | list[str] | None = None,
    image_resize_target_size_kb: Optional[int] = 100,
    client: Optional[OpenAI] = None,
    model: Optional[str] = None,
    temperature: Optional[float] = 0.001,
    max_tokens: int | None = None,
    # stop: Optional[list[str]] = None,
    response_json: bool = False,
    seed: Optional[int] = DEFAULT_RANDOM_SEED,
    verbose: int = 0,
):
    """
    Usage:

        client = OpenAI(
            api_key=OPENAI_API_KEY,
        )
        msg, tools, extra = call_gpt_uncached(client, "What is the capital of France?")

        @cachier()
        def call_gpt_cached(
            inp: str, tools: Optional[list[dict]] = None, tool_choice: ToolChoiceTyps = "auto"
        ):
            return call_gpt(client=client, inp=inp, tools=tools, tool_choice=tool_choice)

    https://platform.openai.com/docs/api-reference/chat/create?lang=python
    SAMPLE_TOOLS = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    The messages for images could look like this:
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Filename: cat.jpg"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAA..."
                    }
                },
                {
                    "type": "text",
                    "text": "Filename: dog.png"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJA..."
                    }
                },
                {
                    "type": "text",
                    "text": "Describe each of these images, referring to them by their filenames:"
                },
            ]
        }
    ]
    """

    extra = locals()
    extra.pop("client")  # to avoid caching issues, and because it includes the API key
    if client is None:
        client = OpenAI(api_key=OPENAI_API_KEY)
    if not tools:
        # otherwise you get a 400
        tool_choice = None
    if model is None:
        model = DEFAULT_MODEL_NAME
    if image_filens is None:
        base64_images = None
        image_contents = []
    else:
        if isinstance(image_filens, str):
            image_filens = [image_filens]
        assert (
            image_resize_target_size_kb is not None
        ), "You must provide a resize_target_size_kb"
        image_contents, base64_images = contents_for_images(
            image_filens, resize_target_size_kb=image_resize_target_size_kb
        )

    prompt_content = {"type": "text", "text": prompt}
    contents = image_contents + [prompt_content]
    messages = [{"role": "user", "content": contents}]
    response_format = {"type": "json_object"} if response_json else None
    if model in MODELS_NO_TOOLS:
        assert (
            tools is None
        ), "You cannot provide tools for models that don't support them"
        assert (
            tool_choice is None
        ), "You cannot provide tool_choice for models that don't support them"
        tools, tool_choice = NOT_GIVEN, NOT_GIVEN  # type: ignore
        # assert temperature is None, f"Temperature can't be set for {model}"
        temperature = NOT_GIVEN  # type: ignore
    response = client.chat.completions.create(
        model=model,
        messages=messages,  # type: ignore
        tools=tools,  # type: ignore
        tool_choice=tool_choice,  # type: ignore
        temperature=temperature,
        max_tokens=max_tokens if max_tokens is not None else NOT_GIVEN,
        # stop=stop,  # for some reason, setting this to None causes an error
        seed=seed,
        response_format=response_format,  # type: ignore
    )
    msg = response.choices[0].message.content  # could be empty
    if response_json:
        msg = json.loads(msg)  # type: ignore
    tool_calls = response.choices[0].message.tool_calls  # could be None or a list
    extra.update(
        {
            "response": response.model_dump(),
            "msg": msg,
            "tool_calls": tool_calls,
            "model": model,
            "base64_images": base64_images,
            "contents": contents,
            # "client": client,
        }
    )
    if verbose >= 2:
        print(f"PROMPT:\n{prompt}")
    if verbose >= 1:
        print(f"LLM MESSAGE:\n{msg}")
    if verbose >= 2:
        print(f"TOOL CALLS:\n{tool_calls}")
        print(f"LLM RESPONSE:\n{json.dumps(response.model_dump(), indent=2)}")
    return msg, tool_calls, extra


def llm_generate_summary(
    txt_or_txts: str | list[str],
    granularity: Optional[GranularityTyps] = None,
    full_txt_or_html: Optional[str] = None,
    n_truncate_words=None,
    model_name: Optional[str] = None,
    max_tokens: Optional[int] = None,
    verbose: int = 0,
):
    """
    TXT_OR_TXTS can either be a single string,
    or a list of strings (in which case it tries to find the summary that unifies them).

    FULL_TXT_OR_HTML is the full text or HTML that the text is a part of.
    It is used to provide context to the summarisation.

    TODO: I combined summarisation of text and list into one, but I'm not convinced
    it was such a good idea. It has made things unwieldy. I'm mostly focused on the
    summarisation of a single text for now.

    TODO maybe we don't need both MAX_TOKENS and N_TRUNCATE_WORDS. Maybe we can just
    use MAX_TOKENS and calculate N_TRUNCATE_WORDS from that.
    """

    def do_summarise_text(txt: str):
        if n_truncate_words:
            txt = txt[:n_truncate_words]
        context["txt"] = txt
        prompt = jinja_render(summarise_text, context)
        extra.update(
            {
                "txt": txt,  # type: ignore
            }
        )  # type: ignore
        return prompt

    def do_summarise_list(txts: list[str]):
        # UNTESTED
        txts = [txt.replace("\n", " ").replace("  ", " ").strip() for txt in txts]
        if max_tokens is not None:
            if n_truncate_words is None:  # type: ignore
                # assume a word is <1.5 tokens. so 3500 / 10 / 1.5 = 233
                n_truncate_words = int(max_tokens / len(txts) / 1.5)
        if n_truncate_words is not None:  # type: ignore
            txts = [txt[:n_truncate_words] for txt in txts if txt]  # type: ignore
        context["txts"] = txts  # type: ignore
        prompt = jinja_render(summarise_list_of_texts_as_one, context)
        extra.update(
            {
                "txts": txts,
                "max_tokens": max_tokens,
                "n_truncate_words": n_truncate_words,  # type: ignore
            }
        )  # type: ignore
        return prompt

    extra = {"input": locals()}
    if full_txt_or_html is not None:
        raise NotImplementedError("full_txt_or_html is not yet implemented")
    context = {
        "granularity": (
            "Adjust the length of your summary appropriately, based on the length and complexity of the text. For example, if the text is a paragraph, write a sentence or two. If it's a page, write a paragraph or so. If it's a book, write a page."
            if granularity is None
            else f"Write at most a {granularity}."
        )
    }
    assert txt_or_txts, "txt_or_txts must be non-empty"
    if isinstance(txt_or_txts, str):
        prompt = do_summarise_text(txt=txt_or_txts)
    elif isinstance(txt_or_txts, list):
        prompt = do_summarise_list(txts=txt_or_txts)
    else:
        raise TypeError("txt_or_txts must be str or list[str]: %s" % type(txt_or_txts))

    assert max_tokens is None, "max_tokens is not yet implemented"
    msg, tools, extra = call_openai_gpt(
        prompt=prompt, model=model_name
    )  # , max_tokens=max_tokens)
    extra.update(
        {
            "context": context,
            "prompt": prompt,
            "llm_msg": msg,
            "llm_tools": tools,
            "llm_extra": extra,
        }  # type: ignore
    )
    if verbose > 0:
        print("Summary:", msg)
    if verbose > 1:
        print(f"PROMPT:\n{prompt}")
    extra = {
        "model_name": model_name,
        "prompt": prompt,
    }
    return msg, extra


if __name__ == "__main__":
    # txt = prompt('What is the capital of France?')
    msg, _, _ = call_openai_gpt("What is the capital of France?")
    print(msg)
