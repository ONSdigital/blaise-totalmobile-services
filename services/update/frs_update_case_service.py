import logging
from typing import Dict

from enums.blaise_fields import BlaiseFields
from enums.questionnaire_case_outcome_codes import FRSQuestionnaireOutcomeCodes
from models.update.frs_blaise_update_case_model import FRSBlaiseUpdateCase
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.blaise_service import RealBlaiseService
from services.update.update_case_service_base import UpdateCaseServiceBase


class FRSUpdateCaseService(UpdateCaseServiceBase[FRSBlaiseUpdateCase]):
    def __init__(self, blaise_service: RealBlaiseService):
        super().__init__(blaise_service)

    def update_case(
        self, totalmobile_request: TotalMobileIncomingUpdateRequestModel
    ) -> None:
        self.validate_questionnaire_exists(totalmobile_request.questionnaire_name)

        blaise_case = self.get_existing_blaise_case(
            totalmobile_request.questionnaire_name, totalmobile_request.case_id
        )

        fields_to_update = {}

        # TODO: For instances where an Outcome Code triggers the removal of the case from a workload
        #  (e.g. as it was marked as Completed) - it can also be removed from CMA as well as Blaise
        # if totalmonile_request.outcome_code in (e.g completed):
        # Remove from CMA
        # check with Martyn, what happens with Blaise?

        if totalmobile_request.outcome_code in (
            FRSQuestionnaireOutcomeCodes.outcome_update_set()
        ) and blaise_case.outcome_code not in (
            FRSQuestionnaireOutcomeCodes.completed_set()
        ):
            fields_to_update.update(
                blaise_case.get_outcome_code_fields(totalmobile_request)
            )

        if totalmobile_request.outcome_code in (
            FRSQuestionnaireOutcomeCodes.refusal_reason_set()
        ):
            # TODO: Remove from CMA

            fields_to_update.update(
                blaise_case.get_refusal_reason_fields(totalmobile_request)
            )

        if not fields_to_update:
            logging.info(
                f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
                f"has not been updated in Blaise (Blaise hOut={blaise_case.outcome_code}, "
                f"TM hOut={totalmobile_request.outcome_code})"
            )
            return

        self._blaise_service.update_case(
            totalmobile_request.questionnaire_name,
            totalmobile_request.case_id,
            fields_to_update,
        )

        if BlaiseFields.refusal_reason in fields_to_update:
            logging.info(
                f"Outcome code and refusal reason updated (Questionnaire={totalmobile_request.questionnaire_name}, "
                f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, TM RefReas={totalmobile_request.refusal_reason}, "
                f"TM hOut={totalmobile_request.outcome_code})"
            )
            return

        logging.info(
            f"Outcome code updated (Questionnaire={totalmobile_request.questionnaire_name}, "
            f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )

    def _return_survey_type_update_case_model(
        self, questionnaire_name, case: Dict[str, str]
    ) -> FRSBlaiseUpdateCase:
        return FRSBlaiseUpdateCase(questionnaire_name, case)
