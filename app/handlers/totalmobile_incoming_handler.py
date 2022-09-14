import logging

from app.utilities.parse_json import get_reference_number
from models.totalmobile.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.placeholder_service import do_something_service
from services.update_case_service import UpdateCaseService


def submit_form_result_request_handler(request, update_case_service: UpdateCaseService):
    logging.info(f"Incoming request via the 'submitformresultrequest' endpoint")
    data = request.get_json()
    totalmobile_case = TotalMobileIncomingUpdateRequestModel.import_request(data)
    update_case_service.update_case(totalmobile_case)


def update_visit_status_request_handler(request):
    logging.info(f"Incoming request via the 'updatevisitstatusrequest' endpoint")
    print("This is a basic placeholder per BLAIS5-3071")
    data = request.get_json()
    reference_number = get_reference_number(data)
    do_something_service(reference_number)


def complete_visit_request_handler(request):
    logging.info(f"Incoming request via the 'completevisitrequest' endpoint")
    print("This is a basic placeholder per BLAIS5-3071")
    data = request.get_json()
    reference_number = get_reference_number(data)
    do_something_service(reference_number)
