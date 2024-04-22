def get_list_from_str_or_list(str_or_list: str | list[str]) -> list[str]:
    """
    e.g.
      - get_list_from_str_or_list("asdf") -> ["asdf"]
      - get_list_from_str_or_list(["asdf"]) -> ["asdf"]
    """
    if isinstance(str_or_list, str):
        aliases = [str_or_list]
    elif isinstance(str_or_list, list):
        aliases = str_or_list
    else:
        raise Exception(f"Unknown typ: {type(str_or_list)}")
    return aliases
