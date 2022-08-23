import logging
from app.services.total_mobile_service import (
    do_something_service,
)
from app.utilities.parse_json import (
    get_reference_number,
    validate_data,
)
from appconfig.config import Config
from models.totalmobile.totalmobile_incoming_update_request_model import TotalMobileIncomingUpdateRequestModel
from services import update_case_service


def submit_form_result_request_handler(request, questionnaire_service):
    config = Config.from_env()
    data = request.get_json()
    validate_data(data)
    logging.info(f"Incoming request via 'submitformresultrequest' - {data}")

    totalmobile_case = TotalMobileIncomingUpdateRequestModel.import_request(data)

    update_case_service.update_case(totalmobile_case, config, questionnaire_service)


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
