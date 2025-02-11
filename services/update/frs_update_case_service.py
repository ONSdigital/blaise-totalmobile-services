import logging
from typing import Dict

from enums.questionnaire_case_outcome_codes import QuestionnaireOutcomeCodes
from models.update.blaise_update_case_model import BlaiseUpdateCaseBase
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.blaise_service import RealBlaiseService
from services.update.update_case_service_base import UpdateCaseServiceBase


class FRSUpdateCaseService(UpdateCaseServiceBase):
    def __init__(self, blaise_service: RealBlaiseService):
        super().__init__(blaise_service)

    def update_case(
        self, totalmobile_request: TotalMobileIncomingUpdateRequestModel
    ) -> None:
        self.validate_questionnaire_exists(totalmobile_request.questionnaire_name)

        blaise_case = self.get_existing_blaise_case(
            totalmobile_request.questionnaire_name, totalmobile_request.case_id
        )

        if totalmobile_request.outcome_code in (
            QuestionnaireOutcomeCodes.REFUSAL_HARD_460.value,
            QuestionnaireOutcomeCodes.REFUSAL_SOFT_461.value,
            QuestionnaireOutcomeCodes.INELIGIBLE_NO_TRACE_OF_ADDRESS_510.value,
            QuestionnaireOutcomeCodes.INELIGIBLE_VACANT_540.value,
            QuestionnaireOutcomeCodes.INELIGIBLE_NON_RESIDENTIAL_551.value,
            QuestionnaireOutcomeCodes.INELIGIBLE_INSTITUTION_560.value,
            QuestionnaireOutcomeCodes.INELIGIBLE_SECOND_OR_HOLIDAY_HOME_580.value,
            QuestionnaireOutcomeCodes.WRONG_ADDRESS_640.value,
        ):

            self.update_case_outcome_code(totalmobile_request, blaise_case)
            return

        logging.info(
            f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
            f"has not been updated in Blaise (Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )

    def update_case_outcome_code(
        self,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
        blaise_case: BlaiseUpdateCaseBase,
    ) -> None:

        fields_to_update = {}

        fields_to_update.update(
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
