import logging

from models.create.cma.totalmobile_incoming_frs_request_model import (
    TotalMobileIncomingFRSRequestModel,
)
from models.update.cma.totalmobile_incoming_frs_unallocation_request_model import (
    TotalMobileIncomingFRSUnallocationRequestModel,
)
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.create.cma.frs_case_allocation_service import FRSCaseAllocationService
from services.update.lms_update_case_service import LMSUpdateCaseService


# TODO - refactor the handler to handle LMS/FRS UpdateCaseService.
def submit_form_result_request_handler(request, update_case_service: LMSUpdateCaseService):
    data = request.get_json()
    totalmobile_case = TotalMobileIncomingUpdateRequestModel.import_request(data)
    update_case_service.update_case(totalmobile_case)


def create_visit_request_handler(
    request, frs_case_allocation_service: FRSCaseAllocationService
):
    data = request.get_json()
    totalmobile_frs_case = TotalMobileIncomingFRSRequestModel.import_request(data)
    frs_case_allocation_service.create_case(totalmobile_frs_case)


def force_recall_visit_request_handler(
    request, frs_case_allocation_service: FRSCaseAllocationService
):
    data = request.get_json()
    totalmobile_unallocation_frs_case = (
        TotalMobileIncomingFRSUnallocationRequestModel.import_request(data)
    )
    frs_case_allocation_service.unallocate_case(totalmobile_unallocation_frs_case)
    return
