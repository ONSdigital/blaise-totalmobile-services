import logging
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Optional, Type, TypeVar

from models.blaise.blaise_case_information_base_model import (
    BlaiseCaseInformationBaseModel,
)
from models.totalmobile.totalmobile_reference_model import TotalmobileReferenceModel

T = TypeVar("T", bound="TotalMobileOutgoingCreateJobPayloadModel")


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
        logging.info(f'DEBUG: payload["dueDate"]["end"]: {payload["dueDate"]["end"]} for {payload["description"]}')
        return payload

    @staticmethod
    def create_job_reference(questionnaire_name: str, case_id: Optional[str]) -> str:
        reference_model = TotalmobileReferenceModel.from_questionnaire_and_case(
            questionnaire_name, case_id
        )
        return reference_model.create_reference()

    @staticmethod
    def get_job_description(questionnaire_case: BlaiseCaseInformationBaseModel) -> str:

        return questionnaire_case.create_case_description_for_interviewer()

    @staticmethod
    def concatenate_address(questionnaire_case: BlaiseCaseInformationBaseModel) -> str:
        fields = [
            questionnaire_case.address_details.address.address_line_1,
            questionnaire_case.address_details.address.address_line_2,
            questionnaire_case.address_details.address.address_line_3,
            questionnaire_case.address_details.address.town,
            questionnaire_case.address_details.address.postcode,
        ]
        concatenated_address = ", ".join(
            [str(i) for i in fields if i != "" and i is not None]
        )
        return concatenated_address

    @staticmethod
    def concatenate_address_line1(
        questionnaire_case: BlaiseCaseInformationBaseModel,
    ) -> str:
        fields = [
            questionnaire_case.address_details.address.address_line_1,
            questionnaire_case.address_details.address.address_line_2,
        ]
        concatenated_address_line1 = ", ".join(
            [str(i) for i in fields if i != "" and i is not None]
        )

        return (
            concatenated_address_line1[:50]
            if len(concatenated_address_line1)
            else concatenated_address_line1
        )

    @staticmethod
    def set_address_coordinates(
        latitude: Optional[str], longitude: Optional[str]
    ) -> AddressCoordinates:

        if not latitude or not longitude:
            return AddressCoordinates(latitude=None, longitude=None)

        return AddressCoordinates(
            latitude=latitude,
            longitude=longitude,
        )

    @staticmethod
    def set_location_reference(questionnaire_case):
        return (
            ""
            if questionnaire_case.address_details.reference is None
            else questionnaire_case.address_details.reference
        )

    @classmethod
    def import_case(
        cls: Type[T],
        questionnaire_name: str,
        questionnaire_case: BlaiseCaseInformationBaseModel,
    ) -> T:
        total_mobile_case = cls(
            identity=Reference(
                reference=cls.create_job_reference(
                    questionnaire_name, questionnaire_case.case_id
                )
            ),
            description=cls.get_job_description(questionnaire_case),
            origin="ONS",
            duration=15,
            workType=questionnaire_case.tla,
            skills=[Skill(identity=Reference(reference=questionnaire_case.tla))],
            dueDate=DueDate(end=questionnaire_case.wave_com_dte),
            location=AddressDetails(
                reference=cls.set_location_reference(questionnaire_case),
                address=cls.concatenate_address(questionnaire_case),
                addressDetail=Address(
                    addressLine1=cls.concatenate_address_line1(questionnaire_case),
                    addressLine2=questionnaire_case.address_details.address.address_line_3,
                    addressLine3=questionnaire_case.address_details.address.county,
                    addressLine4=questionnaire_case.address_details.address.town,
                    postCode=questionnaire_case.address_details.address.postcode,
                    coordinates=cls.set_address_coordinates(
                        latitude=questionnaire_case.address_details.address.coordinates.latitude,
                        longitude=questionnaire_case.address_details.address.coordinates.longitude,
                    ),
                ),
            ),
            contact=ContactDetails(
                name=questionnaire_case.address_details.address.postcode
            ),
            attributes=[
                AdditionalProperty(
                    name="Region", value=questionnaire_case.field_region
                ),
                AdditionalProperty(name="Team", value=questionnaire_case.field_team),
            ],
            additionalProperties=[
                AdditionalProperty(
                    name="surveyName", value=questionnaire_case.data_model_name
                ),
                AdditionalProperty(name="tla", value=questionnaire_case.tla),
                AdditionalProperty(name="wave", value=str(questionnaire_case.wave)),
                AdditionalProperty(name="priority", value=questionnaire_case.priority),
                AdditionalProperty(
                    name="fieldRegion", value=questionnaire_case.field_region
                ),
                AdditionalProperty(
                    name="fieldTeam", value=questionnaire_case.field_team
                ),
            ],
        )

        if questionnaire_case.has_uac and questionnaire_case.uac_chunks is not None:
            total_mobile_case.additionalProperties.extend(
                [
                    AdditionalProperty(
                        name="uac1", value=questionnaire_case.uac_chunks.uac1
                    ),
                    AdditionalProperty(
                        name="uac2", value=questionnaire_case.uac_chunks.uac2
                    ),
                    AdditionalProperty(
                        name="uac3", value=questionnaire_case.uac_chunks.uac3
                    ),
                ]
            )

        return total_mobile_case
