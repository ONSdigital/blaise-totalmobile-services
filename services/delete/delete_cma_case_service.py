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
        if not self.cma_blaise_service.questionnaire_exists(
            totalmobile_request.questionnaire_name
        ):
            raise ValueError(
                f"Questionnaire {totalmobile_request.questionnaire_name} does not exist in CMA."
            )

        cma_guid = "1234"  # TODO: This is the questionnaire guid, and we need to get it from somewhere!
        cma_case = self.cma_blaise_service.case_exists(
            cma_guid, totalmobile_request.case_id
        )

        # TODO: Test cma_case returns the following expected fields
        # guid = case["fieldData"]["mainSurveyID"]
        # questionnaire_name = questionnaire_name
        # unique_case_id = case["fieldData"]["id"]
        # prev_interviewer = case["fieldData"]["cmA_ForWhom"]
        # current_timestamp = datetime.now()
        # formatted_date_time = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        if cma_case and (
            totalmobile_request.outcome_code
            in (FRSQuestionnaireOutcomeCodes.remove_from_cma_set())
        ):
            self.frs_case_allocation_service.create_new_entry_for_special_instructions(
                cma_case, totalmobile_request.questionnaire_name
            )
