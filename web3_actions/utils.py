import json
from typing import Union, Optional


def read_json(path: str, encoding: Optional[str] = None) -> dict:
    return json.load(open(path, encoding=encoding))
