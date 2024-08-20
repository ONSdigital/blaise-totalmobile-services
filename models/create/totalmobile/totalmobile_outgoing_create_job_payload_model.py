from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Reference:
    reference: str


@dataclass
class Skill:
    identity: Reference


@dataclass
class DueDate:
    end: Optional[datetime]


@dataclass
class AddressCoordinates:
    latitude: Optional[str]
    longitude: Optional[str]


@dataclass
class Address:
    addressLine1: Optional[str]
    addressLine2: Optional[str]
    addressLine3: Optional[str]
    addressLine4: Optional[str]
    postCode: Optional[str]
    coordinates: AddressCoordinates


@dataclass
class AddressDetails:
    reference: str
    address: str
    addressDetail: Address


@dataclass
class ContactDetails:
    name: Optional[str]


@dataclass
class AdditionalProperty:
    name: str
    value: Optional[str]


@dataclass
class TotalMobileOutgoingCreateJobPayloadModel:
    identity: Reference
    description: str
    origin: str
    duration: int
    workType: str
    skills: List[Skill]
    dueDate: DueDate
    location: AddressDetails
    contact: ContactDetails
    attributes: List[AdditionalProperty]
    additionalProperties: List[AdditionalProperty]

    def to_payload(self) -> dict[str, str]:
        payload = asdict(self)
        payload["dueDate"]["end"] = (
            self.dueDate.end.strftime("%Y-%m-%d") if self.dueDate.end else ""
        )
        return payload
