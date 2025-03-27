import logging

from requests import JSONDecodeError

from enums.questionnaire_case_outcome_codes import FRSQuestionnaireOutcomeCodes
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.cma_blaise_service import CMABlaiseService
from services.create.cma.frs_case_allocation_service import FRSCaseAllocationService


class DeleteCMACaseService:
    def __init__(
        self,
        cma_blaise_service: CMABlaiseService,
        frs_case_allocation_service: FRSCaseAllocationService,
    ):
        self.cma_blaise_service = cma_blaise_service
        self.frs_case_allocation_service = frs_case_allocation_service

    def remove_case_from_cma(
        self, totalmobile_request: TotalMobileIncomingUpdateRequestModel
    ) -> None:
        if totalmobile_request.outcome_code not in (
            FRSQuestionnaireOutcomeCodes.remove_from_cma_set()
        ):
            logging.info(
                f"Totalmobile case has an outcome code of {totalmobile_request.outcome_code} "
                f"and should not to be removed from CMA."
            )
            return

        questionnaire = self._get_questionnaire_and_validate(
            totalmobile_request.questionnaire_name
        )
        cma_case = self._get_cma_case_and_validate(
            questionnaire, totalmobile_request.case_id
        )

        logging.info(
            f"Case {totalmobile_request.case_id} for questionnaire {questionnaire['name']} with an outcome code of "
            f"{totalmobile_request.outcome_code} will be recalled from CMA."
        )
        self.frs_case_allocation_service.create_new_entry_for_special_instructions(
            cma_case, totalmobile_request.questionnaire_name
        )

    def _get_questionnaire_and_validate(self, questionnaire_name):
        try:
            questionnaire = self.cma_blaise_service.questionnaire_exists(
                questionnaire_name
            )
        except JSONDecodeError:
            raise ValueError(
                f"Questionnaire {questionnaire_name} does not exist in CMA."
            )
        if not questionnaire:
            raise ValueError(
                f"Questionnaire {questionnaire_name} does not exist in CMA."
            )
        return questionnaire

    def _get_cma_case_and_validate(self, questionnaire, case_id):
        cma_case = self.cma_blaise_service.case_exists(questionnaire["id"], case_id)
        if not cma_case:
            raise ValueError(
                f"Case {case_id} for questionnaire {questionnaire['name']} does not exist in CMA."
            )
        return cma_case
