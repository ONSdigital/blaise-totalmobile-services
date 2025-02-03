import logging
from typing import Dict

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

        if self._should_update_case_outcome_code(totalmobile_request):
            self._update_case_outcome_code(totalmobile_request, blaise_case)
            return

        self._log_no_update(blaise_case, totalmobile_request)

    def _update_case_outcome_code(
        self,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
        blaise_case: BlaiseUpdateCase,
    ) -> None:

        fields_to_update = self._get_fields_to_update_case_outcome_code(
            blaise_case, totalmobile_request
        )

        self._log_attempting_to_update_case(totalmobile_request)

        self._blaise_service.update_case(
            totalmobile_request.questionnaire_name,
            totalmobile_request.case_id,
            fields_to_update,
        )

        self._log_outcome_code_updated(
            blaise_case, totalmobile_request
        )

    @staticmethod
    def _should_update_case_outcome_code(
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> bool:
        return totalmobile_request.outcome_code in {
            enum.value for enum in FRSQuestionnaireOutcomeCodes
        }

    @staticmethod
    def _get_fields_to_update_case_outcome_code(
        blaise_case: BlaiseUpdateCase,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> Dict[str, str]:
        return {**blaise_case.get_outcome_code_fields(totalmobile_request)}

    @staticmethod
    def _log_outcome_code_updated(
        blaise_case: BlaiseUpdateCase,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> None:
        logging.info(
            f"Outcome code updated (Questionnaire={totalmobile_request.questionnaire_name}, "
            f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )

    @staticmethod
    def _log_attempting_to_update_case(
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> None:
        logging.info(
            f"Attempting to update case {totalmobile_request.case_id} in questionnaire {totalmobile_request.questionnaire_name} in Blaise"
        )

    @staticmethod
    def _log_no_update(
        blaise_case: BlaiseUpdateCase,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> None:
        logging.info(
            f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
            f"has not been updated in Blaise (Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )
