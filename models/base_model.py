from dataclasses import fields


class BaseModel:

    @staticmethod
    def validate_dataclass_model_fields_are_populated(model) -> bool:
        for field in fields(model):
            if getattr(model, field.name) is None or getattr(model, field.name) == "":
                return False

        return True
