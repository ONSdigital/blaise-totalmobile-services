import logging
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
from services import questionnaire_service


def submit_form_result_request_handler(request):
    print("This placeholder is per BLAIS5-3086 to update Telephone Number in Blaise")
    data = request.get_json()
    validate_data(data)
    
    questionnaire_name, case_id = get_case_details(data)
    logging.info(f'Successfully found questionnaire {questionnaire_name} in Blaise')
    logging.info(f'Successfully found case {case_id} for questionnaire {questionnaire_name} in Blaise')

    telephone_number = get_telephone_number(data)
    
    print(f"Updating telephone number for {questionnaire_name}, {case_id}, please wait...")
    config = Config.from_env()
    questionnaire_service.update_case_field(questionnaire_name, case_id, "qDataBag.TelNo", telephone_number, config)
    #if above failed, log an error "failed to update case xx for questionnaire yy"


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
