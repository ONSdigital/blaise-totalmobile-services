from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.cma_delete_case_service import CMAServiceFacade
from services.update.frs_update_case_service import FRSUpdateCaseService


class FRSCaseOrchestrator:
    def __init__(
        self,
        update_case_service: FRSUpdateCaseService,
        cma_service_facade: CMAServiceFacade,
    ):
        self.update_case_service = update_case_service
        self.cma_service_facade = cma_service_facade

    def process_case_update(
        self, totalmobile_request: TotalMobileIncomingUpdateRequestModel
    ):
        # Update Blaise
        self.update_case_service.update_case(totalmobile_request)

        # Delete from CMA
        self.cma_service_facade.remove_case_from_cma(
            totalmobile_request.questionnaire_name, totalmobile_request.case_id
        )
