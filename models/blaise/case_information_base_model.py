from abc import abstractmethod
from dataclasses import fields
from typing import Any

from models.base_model import BaseModel


class CaseInformationBaseModel(BaseModel):
    @property
    @abstractmethod
    def has_uac(self) -> bool:
        pass

  