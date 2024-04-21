from typing import Any

def get_key_from_value(dictionary: dict, value: Any) -> Any:
    return list(dictionary.keys())[list(dictionary.values()).index(value)]