from datetime import datetime
from dataclasses import dataclass
from abc import abstractmethod
from typing import Optional, List

from models.base_model import BaseModel

@dataclass
class AddressCoordinates:
    latitude: Optional[str]
    longitude: Optional[str]


@dataclass
class Address:
    address_line_1: Optional[str]
    address_line_2: Optional[str]
    address_line_3: Optional[str]
    county: Optional[str]
    town: Optional[str]
    postcode: Optional[str]
    coordinates: AddressCoordinates


@dataclass
class AddressDetails:
    reference: Optional[str]
    address: Address


@dataclass
class CaseInformationBaseModel(BaseModel):
    questionnaire_name: str
    case_id: Optional[str]
    tla: str
    data_model_name: Optional[str]
    wave: Optional[int]
    wave_com_dte: Optional[datetime]
    address_details: AddressDetails
    priority: Optional[str]
    field_case: Optional[str]
    field_region: Optional[str]
    field_team: Optional[str]

    @property
    @abstractmethod
    def has_uac(self) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def required_fields_from_blaise() -> List:
        pass

    @staticmethod
    def convert_indicator_to_y_n_or_empty(value: Optional[str]):
        if not value or value == "":
            return ""

        return "Y" if value == "1" else "N"

    @staticmethod
    def convert_string_to_integer(value: str) -> int:
        if value == "":
            return 0
        return int(value)

    @staticmethod
    def string_to_bool(value: Optional[str]) -> bool:
        if value == "" or value is None:
            return False
        return True