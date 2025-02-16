import llm
import json
import openai
import os
from pprint import pprint
from typing import Any, Optional

from gjdutils.llms_openai import (
    DEFAULT_MODEL_NAME,
    MODEL_NAME_GPT4_TURBO,
    OPENAI_API_KEY,
    GranularityTyps,
    call_openai_gpt,
    call_openai_gpt_with_retry,
    call_openai_gpt_with_retry_and_backoff,
)
from gjdutils.prompt_templates import summarise_list_of_texts_as_one, summarise_text
from gjdutils.rand import DEFAULT_RANDOM_SEED
from gjdutils.strings import jinja_render


DEFAULT_MODEL = llm.get_model(DEFAULT_MODEL_NAME)
DEFAULT_MODEL.key = os.environ.get("OPENAI_API_KEY")


def model_from_model_name(model_name: Optional[str] = None, verbose: int = 0):
    if model_name is None:
        model = DEFAULT_MODEL
    else:
        if verbose > 0:
            print("MODEL:", model_name)
        model = llm.get_model(model_name)
        model.key = OPENAI_API_KEY
    return model, model_name


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


def llm_prompt(
    prompt: str,
    model_name: Optional[str] = None,
    temperature: Optional[float] = 0.01,
    max_tokens: Optional[int] = None,
    to_json: bool = False,
    verbose: int = 1,
):
    model, _ = model_from_model_name(model_name)
    response = model.prompt(prompt, temperature=temperature, max_tokens=max_tokens)
    if verbose > 0:
        for chunk in response:
            print(chunk, end="")
        print()
    llm_out = response.text()
    llm_json = proc_llm_out_json(llm_out) if to_json else None
    extra = {
        "prompt": prompt,
        "model_name": model_name,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "response": response,
        "llm_out": llm_out,
        "llm_json": llm_json,
    }
    return llm_json if to_json else llm_out, extra


def llm_prompt_json(
    prompt: str,
    functions: list[dict],
    model_name: str = MODEL_NAME_GPT4_TURBO,
    temperature: Optional[float] = 0.01,
    verbose: int = 1,
):
    """
    Based on https://platform.openai.com/docs/guides/gpt/function-calling

    Simon Willison's LLM library doesn't seem to support function calling,
    so we're using the OpenAI Python API directly.

    Doesn't actually call the function - we're just using the function-calling
    API to ensure we get back json that matches our defined schema.

    e.g. functions = [
        {
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
        }
    ]
    """
    # model, model_name = model_from_model_name(model_name)
    assert functions, "PROMPT_JSON requires at least one function"
    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(  # type: ignore
        model=model_name,
        messages=messages,
        # if you try and set this to None or [] you get an error, so we'll require at least one actual function (see assert above)
        functions=functions,
        temperature=temperature,
        seed=DEFAULT_RANDOM_SEED,
    )
    response_message = response["choices"][0]["message"]  # type: ignore

    if response_message.get("function_call"):
        function_name = response_message["function_call"]["name"]
        function_args = json.loads(response_message["function_call"]["arguments"])
        llm_out = {
            "role": "function",
            "name": function_name,
            "args": function_args,
            # "content": function_response,
        }

        # if call_function:
        #     Step 3: call the function
        #     # Note: the JSON response may not always be valid; be sure to handle errors
        #     available_functions = {
        #         "get_current_weather": get_current_weather,
        #     }  # only one function in this example, but you can have multiple
        #     function_to_call = available_functions[function_name]
        #     function_response = function_to_call(
        #         location=function_args.get("location"),
        #         unit=function_args.get("unit"),
        #     )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                # "content": function_response,
            }
        )
        # if call_function:
        #     )  # extend conversation with function response
        #     second_response = openai.ChatCompletion.create(
        #         model="gpt-3.5-turbo-0613",
        #         messages=messages,
        #         seed=DEFAULT_RANDOM_SEED,
        #     )  # get a new response from GPT where it can see the function response
        #     return second_response
    else:
        function_name = None
        function_args = None
        llm_out = response_message["content"]

    extra = {
        "prompt": prompt,
        "model_name": model_name,
        "functions": functions,
        "temperature": temperature,
        "messages": messages,
        "response": response,
        "response_message": response_message,
        "function_name": function_name,
        "function_args": function_args,
    }
    if verbose > 0:
        if isinstance(llm_out, str):
            print(llm_out)
        else:
            pprint(llm_out)
    return llm_out, extra


def llm_generate_summary(
    txt_or_txts: str | list[str],
    granularity: Optional[GranularityTyps] = None,
    n_truncate_words=None,
    model_name: Optional[str] = None,
    max_tokens: Optional[int] = None,
    verbose: int = 1,
):
    """
    TXT_OR_TXTS can either be a single string,
    or a list of strings (in which case it tries to find the summary that unifies them).

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

    if model_name is None:
        model_name = "gpt-3.5-turbo"
    extra = {"input": locals()}
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

    llm_out, llm_extra = llm_prompt(
        prompt, model_name=model_name, max_tokens=max_tokens, verbose=0
    )
    extra.update(
        {
            "context": context,
            "prompt": prompt,
            "llm_out": llm_out,
            "llm_extra": llm_extra,
        }  # type: ignore
    )
    if verbose > 0:
        print("Summary:", llm_out)
    if verbose > 1:
        print(f"PROMPT:\n{prompt}")
    extra = {
        "model_name": model_name,
        "prompt": prompt,
    }
    return llm_out, extra


def llm_fix_json(broken_j: str, model_name: str = "gpt-3.5-turbo"):
    broken_j = broken_j.strip()
    prompt = (
        """
Here is some output from an LLM that is supposed to be pure, valid JSON, but it is broken. Return valid JSON, stripping away any extraneous commentary or prose, but maintaining the structure and meaning of the original data as closely as possible.

If the json is already valid, return it unchanged.

Err on the side of caution: if you're confused about what to do with the input, or if it's ambiguous how best to fix the json, or it is not possible to fix the json, or any other error or uncertainty, return 'ERROR'.

----

%s
"""
        % broken_j
    )
    prompt = prompt.strip()
    fixed_j, extra = llm_prompt(prompt, model_name=model_name, temperature=0.001)
    fixed_j = fixed_j.strip()  # type: ignore
    try:
        json.loads(fixed_j)
        # TODO check that the before and after are similar lengths and substantially similar strings
        return fixed_j
    except:
        raise


if __name__ == "__main__":
    # txt = prompt('What is the capital of France?')
    txt = llm_prompt("What is the capital of France?")
