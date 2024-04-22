import json


def proc_llm_out_json(s: str):
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
