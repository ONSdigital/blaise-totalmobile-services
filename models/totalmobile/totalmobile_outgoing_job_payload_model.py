from dataclasses import asdict, dataclass
from datetime import datetime
from typing import List, Optional, Type, TypeVar

from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.totalmobile.totalmobile_reference_model import TotalmobileReferenceModel

T = TypeVar("T")


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
    address: str
    addressDetail: Address


@dataclass
class ContactDetails:
    name: str


@dataclass
class AdditionalProperty:
    name: str
    value: str


@dataclass
class TotalMobileOutgoingJobPayloadModel:
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

    @staticmethod
    def create_job_reference(questionnaire_name: str, case_id: str) -> str:
        reference_model = TotalmobileReferenceModel(questionnaire_name, case_id)
        return reference_model.create_reference()

    @staticmethod
    def create_description(
        questionnaire_name: str, questionnaire_case: BlaiseCaseInformationModel
    ) -> str:
        uac_string = (
            ""
            if questionnaire_case.uac_chunks is None
            else f"{questionnaire_case.uac_chunks.uac1} {questionnaire_case.uac_chunks.uac2} {questionnaire_case.uac_chunks.uac3}"
        )
        due_date_string = (
            ""
            if questionnaire_case.wave_com_dte is None
            else questionnaire_case.wave_com_dte.strftime("%d/%m/%Y")
        )
        return (
            f"UAC: {uac_string}\n"
            f"Due Date: {due_date_string}\n"
            f"Study: {questionnaire_name}\n"
            f"Case ID: {questionnaire_case.case_id}"
        )

    @staticmethod
    def concatenate_address_line(questionnaire_case: BlaiseCaseInformationModel) -> str:
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

    @classmethod
    def import_case(
        cls: Type[T],
        questionnaire_name: str,
        questionnaire_case: BlaiseCaseInformationModel,
    ) -> T:
        total_mobile_case = TotalMobileOutgoingJobPayloadModel(
            identity=Reference(
                reference=cls.create_job_reference(
                    questionnaire_name, questionnaire_case.case_id
                )
            ),
            description=cls.create_description(questionnaire_name, questionnaire_case),
            origin="ONS",
            duration=15,
            workType="LMS",
            skills=[Skill(identity=Reference(reference="LMS"))],
            dueDate=DueDate(end=questionnaire_case.wave_com_dte),
            location=AddressDetails(
                address=cls.concatenate_address_line(questionnaire_case),
                addressDetail=Address(
                    addressLine1=questionnaire_case.address_details.address.address_line_1,
                    addressLine2=questionnaire_case.address_details.address.address_line_2,
                    addressLine3=questionnaire_case.address_details.address.address_line_3,
                    addressLine4=questionnaire_case.address_details.address.county,
                    addressLine5=questionnaire_case.address_details.address.town,
                    postCode=questionnaire_case.address_details.address.postcode,
                    coordinates=AddressCoordinates(
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
                AdditionalProperty(name="tla", value="LMS"),
                AdditionalProperty(name="wave", value=questionnaire_case.wave),
                AdditionalProperty(name="priority", value=questionnaire_case.priority),
                AdditionalProperty(
                    name="fieldRegion", value=questionnaire_case.field_region
                ),
                AdditionalProperty(
                    name="fieldTeam", value=questionnaire_case.field_team
                ),
            ],
        )

        if questionnaire_case.uac_chunks is not None:
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
