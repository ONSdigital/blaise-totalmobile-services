from services.cma_blaise_service import CMABlaiseService
from services.create.cma.frs_case_allocation_service import FRSCaseAllocationService


class CMAServiceFacade:
    def __init__(
        self,
        cma_blaise_service: CMABlaiseService,
        frs_case_allocation_service: FRSCaseAllocationService,
    ):
        self.cma_blaise_service = cma_blaise_service
        self.frs_case_allocation_service = frs_case_allocation_service

    def remove_case_from_cma(self, questionnaire_name: str, case_id: str) -> None:
        if not self.cma_blaise_service.questionnaire_exists(questionnaire_name):
            raise ValueError(
                f"Questionnaire {questionnaire_name} does not exist in CMA."
            )

        cma_guid = "1234"  # TODO: This should be dynamically retrieved
        cma_case = self.cma_blaise_service.case_exists(cma_guid, case_id)

        if cma_case:
            self.frs_case_allocation_service.create_new_entry_for_special_instructions(
                cma_case, questionnaire_name
            )
