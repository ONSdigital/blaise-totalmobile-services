import logging
from urllib.error import HTTPError
from app.services.total_mobile_service import (
    do_something_service,
)
from app.utilities.parse_json import (
    get_case_details,
    get_reference_number,
    get_telephone_number,
    validate_data,
)
from appconfig.config import Config


def submit_form_result_request_handler(request, questionnaire_service):
    data = request.get_json()
    validate_data(data)
    
    questionnaire_name, case_id = get_case_details(data)
    logging.info(f'Successfully found questionnaire {questionnaire_name} in Blaise')
    logging.info(f'Successfully found case {case_id} for questionnaire {questionnaire_name} in Blaise')

    telephone_number = get_telephone_number(data)
    
    print(f"Updating telephone number for {questionnaire_name}, {case_id}, please wait...")
    config = Config.from_env()
    try:
        questionnaire_service.update_case_field(questionnaire_name, case_id, "qDataBag.TelNo", telephone_number, config)
    except HTTPError:
        logging.error("Could not find questionnaire LMS2206_AA1 in Blaise")


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
