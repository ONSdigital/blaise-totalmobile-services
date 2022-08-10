from dataclasses import dataclass, asdict
from typing import Type, TypeVar, List

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

    def to_payload(self) -> dict[str, str]:
        return asdict(self)

    @staticmethod
    def create_job_reference(questionnaire_name: str, case_id: str) -> str:
        return f"{questionnaire_name.replace('_', '-')}.{case_id}"

    @staticmethod
    def create_description(questionnaire_name: str, case_id: str) -> str:
        return f"Study: {questionnaire_name}\nCase ID: {case_id}"

    @classmethod
    def import_case(cls: Type[T], questionnaire_name: str, questionnaire_case: QuestionnaireCaseModel) -> T:
        return TotalMobileCaseModel(
            identity=Reference(reference=cls.create_job_reference(questionnaire_name, questionnaire_case.case_id)),
            description=cls.create_description(questionnaire_name, questionnaire_case.case_id),
            origin="ONS",
            duration=15,
            workType=questionnaire_case.survey_type,
            skills=[Skill(identity=Reference(reference=questionnaire_case.survey_type))],
            dueDate=DueDate(end=questionnaire_case.wave_com_dte),
            location=AddressDetails(addressDetail=Address(
                addressLine1=questionnaire_case.address_line_1,
                addressLine2=questionnaire_case.address_line_2,
                addressLine3=questionnaire_case.address_line_3,
                addressLine4=questionnaire_case.county,
                addressLine5=questionnaire_case.town,
                postCode=questionnaire_case.postcode,
                coordinates=AddressCoordinates(
                    latitude=questionnaire_case.latitude,
                    longitude=questionnaire_case.longitude
                ))
            ),
            contact=ContactDetails(name=questionnaire_case.postcode),
            additionalProperties=[
                AdditionalProperty(
                    name="surveyName",
                    value=questionnaire_case.data_model_name
                ),
                AdditionalProperty(
                    name="tla",
                    value=questionnaire_case.survey_type
                ),
                AdditionalProperty(
                    name="wave",
                    value=questionnaire_case.wave
                ),
                AdditionalProperty(
                    name="priority",
                    value=questionnaire_case.priority
                ),
                AdditionalProperty(
                    name="fieldTeam",
                    value=questionnaire_case.field_team
                ),
                AdditionalProperty(
                    name="uac1",
                    value=questionnaire_case.uac_chunks.uac1
                ),
                AdditionalProperty(
                    name="uac2",
                    value=questionnaire_case.uac_chunks.uac2
                ),
                AdditionalProperty(
                    name="uac3",
                    value=questionnaire_case.uac_chunks.uac3
                )
            ]
        )
