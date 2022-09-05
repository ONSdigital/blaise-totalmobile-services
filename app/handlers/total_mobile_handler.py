import logging

from app.services.total_mobile_service import do_something_service
from app.utilities.parse_json import get_reference_number, validate_data
from models.totalmobile.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.questionnaire_service import QuestionnaireService
from services.update_case_service import UpdateCaseService


def submit_form_result_request_handler(
    request, questionnaire_service: QuestionnaireService
):
    data = request.get_json()
    validate_data(data)
    logging.info(f"Incoming request via 'submitformresultrequest' - {data}")

    totalmobile_case = TotalMobileIncomingUpdateRequestModel.import_request(data)

    update_case_service = UpdateCaseService()
    update_case_service.update_case(totalmobile_case, questionnaire_service)


def update_visit_status_request_handler(request):
    print("This is a basic placeholder per BLAIS5-3071")
    data = request.get_json()

    validate_data(data)
    reference_number = get_reference_number(data)
    do_something_service(reference_number)


def complete_visit_request_handler(request):
    print("This is a basic placeholder per BLAIS5-3071")
    data = request.get_json()

    validate_data(data)
    reference_number = get_reference_number(data)
    do_something_service(reference_number)
