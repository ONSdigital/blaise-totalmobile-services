from dataclasses import fields
from typing import Any


class BaseModel:
    @staticmethod
    def validate_dataclass_model_fields_are_populated(model) -> bool:
        for field in fields(model):
            if getattr(model, field.name) is None or getattr(model, field.name) == "":
                return False

        return True

    @staticmethod
    def dictionary_keys_exist(element, *keys) -> bool:
        """
        Check if *keys (nested) exists in `element` (dict).
        """
        if not isinstance(element, dict):
            raise AttributeError("keys_exists() expects dict as first argument.")
        if len(keys) == 0:
            raise AttributeError(
                "keys_exists() expects at least two arguments, one given."
            )

        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except (KeyError, IndexError):
                return False
        return True

    @staticmethod
    def get_dictionary_keys_value_if_they_exist(element, *keys) -> Any:
        """
        Check if *keys (nested) exists in `element` (dict).
        """
        if not isinstance(element, dict):
            raise AttributeError("keys_exists() expects dict as first argument.")
        if len(keys) == 0:
            raise AttributeError(
                "keys_exists() expects at least two arguments, one given."
            )

        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except KeyError:
                return None
        return None if _element == "" else _element
