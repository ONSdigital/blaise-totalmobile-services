from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

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


@dataclass  # type: ignore #seems to be an issue with dataclass inheritance
class BlaiseCaseInformationBaseModel(BaseModel):
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
    def required_fields() -> List:
        pass
