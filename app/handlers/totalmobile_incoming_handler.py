from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.update.update_case_service import UpdateCaseService


def submit_form_result_request_handler(request, update_case_service: UpdateCaseService):
    data = request.get_json()
    totalmobile_case = TotalMobileIncomingUpdateRequestModel.import_request(data)
    update_case_service.update_case(totalmobile_case)


def update_visit_status_request_handler(request):
    data = request.get_json()
    return


def complete_visit_request_handler(request):
    data = request.get_json()
    return
