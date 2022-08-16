import logging
from app.services.total_mobile_service import (
    do_something_service,
)
from app.utilities.parse_json import (
    get_reference_number,
    validate_data,
)
from appconfig.config import Config
from models.totalmobile_incoming_case_model import TotalMobileIncomingCaseModel


def submit_form_result_request_handler(request, update_blaise_case_service):
    config = Config.from_env()
    data = request.get_json()
    validate_data(data)

    totalmobile_case = TotalMobileIncomingCaseModel.import_case(data)

    update_blaise_case_service.update_case(totalmobile_case, config)


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
