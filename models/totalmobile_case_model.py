from dataclasses import dataclass, fields
from typing import Dict, Type, TypeVar, List

from models.questionnaire_case_model import QuestionnaireCaseModel

T = TypeVar('T')


@dataclass
class Reference:
    reference: str


@dataclass
class Skill:
    identity: Reference


@dataclass
class DueDate:
    end: str


@dataclass
class AddressCoordinates:
    latitude: str
    longitude: str


@dataclass
class Address:
    addressLine1: str
    addressLine2: str
    addressLine3: str
    addressLine4: str
    addressLine5: str
    postCode: str
    coordinates: AddressCoordinates


@dataclass
class AddressDetails:
    addressDetail: Address


@dataclass
class ContactDetails:
    name: str


@dataclass
class AdditionalProperty:
    name: str
    value: str


@dataclass
class TotalMobileCaseModel:
    identity: Reference
    description: str
    origin: str
    duration: int
    workType: str
    skills: List[Skill]
    dueDate: DueDate
    location: AddressDetails
    contact: ContactDetails
    additionalProperties: List[AdditionalProperty]

    @classmethod
    def import_questionnaire_case_data(cls: Type[T], questionnaire_case: QuestionnaireCaseModel) -> T:
        return TotalMobileCaseModel(
        )
