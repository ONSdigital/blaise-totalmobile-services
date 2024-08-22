import logging
from typing import Dict, List, Optional, Sequence

from models.common.totalmobile.totalmobile_reference_model import (
    TotalmobileReferenceModel,
)
from models.common.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from models.create.blaise.blaise_case_information_base_model import (
    BlaiseCaseInformationBaseModel,
)
from models.create.totalmobile.totalmobile_create_job_model import (
    TotalmobileCreateJobModel,
    TotalmobileCreateJobModelRequestJson,
)
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


class TotalmobileCreateJobMapperService:
    def map_totalmobile_create_job_models(
        self,
        questionnaire_name: str,
        cases: Sequence[BlaiseCaseInformationBaseModel],
        world_model: TotalmobileWorldModel,
    ) -> List[TotalmobileCreateJobModel]:

        job_models = [
            self.map_totalmobile_create_job_model(questionnaire_name, case, world_model)
            for case in cases
        ]

        logging.info(
            f"Finished mapping Totalmobile jobs for questionnaire {questionnaire_name}"
        )

        return job_models

    def map_totalmobile_create_job_model(
        self,
        questionnaire_name: str,
        case: BlaiseCaseInformationBaseModel,
        world_model: TotalmobileWorldModel,
    ) -> TotalmobileCreateJobModel:

        return TotalmobileCreateJobModel(
            questionnaire_name,
            world_model.get_world_id(case.field_region),
            case.case_id,
            self.map_totalmobile_job_payload(questionnaire_name, case),
        )

    def map_totalmobile_create_job_model_from_json(
        self, request_json: TotalmobileCreateJobModelRequestJson
    ) -> TotalmobileCreateJobModel:

        return TotalmobileCreateJobModel(
            questionnaire=request_json["questionnaire"],
            world_id=request_json["world_id"],
            case_id=request_json["case_id"],
            payload=request_json["payload"],
        )

    def map_totalmobile_job_payload(
        self, questionnaire_name: str, case: BlaiseCaseInformationBaseModel
    ) -> Dict[str, str]:
        logging.info(
            f"_map_totalmobile_job_payload for questionnaire {questionnaire_name} and case {case.case_id}"
        )
        totalmobile_outgoing_payload_model = self.map_totalmobile_payload_model(
            questionnaire_name, case
        )

        return totalmobile_outgoing_payload_model.to_payload()

    def map_totalmobile_payload_model(
        self,
        questionnaire_name: str,
        questionnaire_case: BlaiseCaseInformationBaseModel,
    ) -> TotalMobileOutgoingCreateJobPayloadModel:

        payload_model = TotalMobileOutgoingCreateJobPayloadModel(
            identity=Reference(
                reference=self.create_job_reference(
                    questionnaire_name, questionnaire_case.case_id
                )
            ),
            description=self.get_job_description(questionnaire_case),
            origin="ONS",   # TODO
            duration=15,    # TODO
            workType=questionnaire_case.tla,
            skills=[Skill(identity=Reference(reference=questionnaire_case.tla))],
            dueDate=DueDate(end=questionnaire_case.wave_com_dte),   # TODO
            location=AddressDetails(
                reference=self.set_location_reference(questionnaire_case),
                address=self.concatenate_address(questionnaire_case),
                addressDetail=Address(
                    addressLine1=self.concatenate_address_line1(questionnaire_case),
                    addressLine2=questionnaire_case.address_details.address.address_line_3,
                    addressLine3=questionnaire_case.address_details.address.county,
                    addressLine4=questionnaire_case.address_details.address.town,
                    postCode=questionnaire_case.address_details.address.postcode,
                    coordinates=self.set_address_coordinates(
                        latitude=questionnaire_case.address_details.address.coordinates.latitude,
                        longitude=questionnaire_case.address_details.address.coordinates.longitude,
                    ),
                ),
            ),
            contact=ContactDetails(
                name=questionnaire_case.address_details.address.postcode
            ),  # TODO
            attributes=[
                AdditionalProperty(
                    name="Region", value=questionnaire_case.field_region
                ),
                AdditionalProperty(name="Team", value=questionnaire_case.field_team),
            ],  # TODO
            additionalProperties=self.get_job_additional_properties(questionnaire_case),
        )

        if questionnaire_case.has_uac and questionnaire_case.uac_chunks is not None:
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
        questionnaire_case: BlaiseCaseInformationBaseModel,
    ) -> list[AdditionalProperty]:
        case_overview = questionnaire_case.create_case_overview_for_interviewer()
        additional_properties = [
            AdditionalProperty(name=name, value=value)
            for name, value in case_overview.items()
        ]
        return additional_properties

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
