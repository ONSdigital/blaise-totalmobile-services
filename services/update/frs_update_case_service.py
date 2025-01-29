import logging

from enums.questionnaire_case_outcome_codes import FRSQuestionnaireOutcomeCodes
from models.update.blaise_update_case_model import BlaiseUpdateCase
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.blaise_service import RealBlaiseService
from services.update.update_case_service_base import UpdateCaseServiceBase


class FRSUpdateCaseService(UpdateCaseServiceBase):
    def __init__(self, blaise_service: RealBlaiseService):
        super().__init__(blaise_service)
        self._blaise_service = blaise_service

    def update_case(
        self, totalmobile_request: TotalMobileIncomingUpdateRequestModel
    ) -> None:
        self.validate_questionnaire_exists(totalmobile_request.questionnaire_name)

        blaise_case = self.get_existing_blaise_case(
            totalmobile_request.questionnaire_name, totalmobile_request.case_id
        )

        if totalmobile_request.outcome_code in {
            enum.value for enum in FRSQuestionnaireOutcomeCodes
        }:
            self._update_case_outcome_code(totalmobile_request, blaise_case)
            return

        logging.info(
            f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
            f"has not been updated in Blaise (Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )

    def _update_case_outcome_code(
        self,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
        blaise_case: BlaiseUpdateCase,
    ) -> None:

        fields_to_update = {}

        fields_to_update.update(
            # TODO - this needs adjusting for FRS
            # TODO - I need me some base and children classes
            blaise_case.get_outcome_code_fields(totalmobile_request)
        )

        self._blaise_service.update_case(
            totalmobile_request.questionnaire_name,
            totalmobile_request.case_id,
            fields_to_update,
        )

        logging.info(
            f"Outcome code updated (Questionnaire={totalmobile_request.questionnaire_name}, "
            f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )
