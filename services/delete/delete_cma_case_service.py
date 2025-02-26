from enums.questionnaire_case_outcome_codes import FRSQuestionnaireOutcomeCodes
from models.update.totalmobile_incoming_update_request_model import TotalMobileIncomingUpdateRequestModel
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

    def remove_case_from_cma(self, totalmobile_request: TotalMobileIncomingUpdateRequestModel) -> None:
        if not self.cma_blaise_service.questionnaire_exists(totalmobile_request.questionnaire_name):
            raise ValueError(
                f"Questionnaire {totalmobile_request.questionnaire_name} does not exist in CMA."
            )

        cma_guid = "1234"  # TODO: This should be dynamically retrieved but I can't remember what it is or where we get it from, but I remember it's weird!
        cma_case = self.cma_blaise_service.case_exists(cma_guid, totalmobile_request.case_id)

        if cma_case and (totalmobile_request.outcome_code in (FRSQuestionnaireOutcomeCodes.remove_from_cma_set())):
            self.frs_case_allocation_service.create_new_entry_for_special_instructions(
                cma_case, totalmobile_request.questionnaire_name
            )
