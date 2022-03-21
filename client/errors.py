from typing import Any
import json


class AuthException(Exception):
    pass


class BadRequest(Exception):
    def __init__(self, error_message: str = "", error_details: Any = None) -> None:
        super().__init__()
        self.error_message = error_message
        self.error_details = error_details

    def __str__(self) -> str:
        if self.error_details != None:
            return json.dumps(self.error_details)
        return self.error_message
