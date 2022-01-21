from typing import Any, List


class AlreadyExists(Exception):
    def __init__(self, fields: List[str], values: List[Any]):
        self.fields = fields
        self.values = values
