from app.services.total_mobile_service import do_something_service, update_case_telephone_number
from app.utilities.parse_json import validate_data, get_case_details, get_telephone_number, get_reference_number


def submit_form_result_request_handler(request):
    print("This placeholder is per BLAIS5-3086 to update Telephone Number in Blaise")

    data = request.get_json()
    validate_data(data)

    instrument_name, case_id = get_case_details(data)
    telephone_number = get_telephone_number(data)

    return update_case_telephone_number(instrument_name, case_id, telephone_number)


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
