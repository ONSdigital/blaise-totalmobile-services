from typing import Optional

from models.common.totalmobile.totalmobile_reference_model import (
    TotalmobileReferenceModel,
)
from models.create.blaise.blaise_create_case_model import BlaiseCreateCaseModel
from models.create.totalmobile.totalmobile_outgoing_create_job_payload_model import (
    AdditionalProperty,
    Address,
    AddressCoordinates,
    AddressDetails,
    ContactDetails,
    DueDate,
    Reference,
    Skill,
    TotalMobileOutgoingCreateJobPayloadModel,
)


class TotalmobilePayloadMapperService:
    def map_totalmobile_payload_model(
        self,
        questionnaire_name: str,
        questionnaire_case: BlaiseCreateCaseModel,
    ) -> TotalMobileOutgoingCreateJobPayloadModel:
        payload_model = TotalMobileOutgoingCreateJobPayloadModel(
            identity=Reference(
                reference=self.create_job_reference(
                    questionnaire_name, questionnaire_case.case_id
                )
            ),
            description=self.get_job_description(questionnaire_case),
            origin="",
            duration=15,
            workType=questionnaire_name[0:3],
            skills=[Skill(identity=Reference(reference=questionnaire_name[0:3]))],
            dueDate=DueDate(end=None),
            location=AddressDetails(
                reference=self.set_location_reference(questionnaire_case),
                address=self.concatenate_address(questionnaire_case),
                addressDetail=Address(
                    addressLine1=self.concatenate_address_line1(questionnaire_case),
                    addressLine2=questionnaire_case.address_line_3,
                    addressLine3=questionnaire_case.county,
                    addressLine4=questionnaire_case.town,
                    postCode=questionnaire_case.postcode,
                    coordinates=self.set_address_coordinates(
                        latitude=questionnaire_case.latitude,
                        longitude=questionnaire_case.longitude,
                    ),
                ),
            ),
            contact=ContactDetails(name=questionnaire_case.postcode),
            attributes=[],
            additionalProperties=self.get_job_additional_properties(questionnaire_case),
        )

        if questionnaire_name.startswith("LMS"):
            return self.map_additional_lms_properties(questionnaire_case, payload_model)
        elif questionnaire_name.startswith("FRS"):
            return payload_model

        raise Exception

    def map_additional_lms_properties(
        self,
        questionnaire_case: BlaiseCreateCaseModel,
        payload_model: TotalMobileOutgoingCreateJobPayloadModel,
    ) -> TotalMobileOutgoingCreateJobPayloadModel:
        payload_model.origin = "ONS"
        payload_model.dueDate.end = questionnaire_case.wave_com_dte
        payload_model.attributes = [
            AdditionalProperty(name="Region", value=questionnaire_case.field_region),
            AdditionalProperty(name="Team", value=questionnaire_case.field_team),
        ]

        if questionnaire_case.uac_chunks is not None:
            payload_model.additionalProperties.extend(
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

        return payload_model

    @staticmethod
    def create_job_reference(questionnaire_name: str, case_id: Optional[str]) -> str:
        reference_model = TotalmobileReferenceModel.from_questionnaire_and_case(
            questionnaire_name, case_id
        )
        return reference_model.create_reference()

    @staticmethod
    def get_job_additional_properties(
        questionnaire_case: BlaiseCreateCaseModel,
    ) -> list[AdditionalProperty]:
        case_overview = questionnaire_case.create_case_overview_for_interviewer()
        additional_properties = [
            AdditionalProperty(name=name, value=value)
            for name, value in case_overview.items()
        ]
        return additional_properties

    @staticmethod
    def get_job_description(questionnaire_case: BlaiseCreateCaseModel) -> str:

        return questionnaire_case.create_case_description_for_interviewer()

    @staticmethod
    def concatenate_address(questionnaire_case: BlaiseCreateCaseModel) -> str:
        fields = [
            questionnaire_case.address_line_1,
            questionnaire_case.address_line_2,
            questionnaire_case.address_line_3,
            questionnaire_case.town,
            questionnaire_case.postcode,
        ]
        concatenated_address = ", ".join(
            [str(i) for i in fields if i != "" and i is not None]
        )
        return concatenated_address

    @staticmethod
    def concatenate_address_line1(
        questionnaire_case: BlaiseCreateCaseModel,
    ) -> str:
        fields = [
            questionnaire_case.address_line_1,
            questionnaire_case.address_line_2,
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
    def set_location_reference(questionnaire_case: BlaiseCreateCaseModel):
        return (
            "" if questionnaire_case.reference is None else questionnaire_case.reference
        )
