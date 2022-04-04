from app.services.total_mobile_service import do_something_service, update_case_telephone_number
from app.utilities.parse_json import get_case_details, get_telephone_number


def submit_form_result_request_handler(request):
    print("This placeholder is per BLAIS5-3086")
    data = validate_request(request)

    instrument_name, case_id = get_case_details(data)
    telephone_number = get_telephone_number(data)
    data_fields = {"qDataBag.TelNo": telephone_number}

    update_case_telephone_number(instrument_name, case_id, data_fields)


def update_visit_status_request_handler(request):
    print("This is a basic placeholder per BLAIS5-3071")
    data = validate_request(request)
    reference_number = get_reference_number(data)
    do_something_service(reference_number)


def complete_visit_request_handler(request):
    print("This is a basic placeholder per BLAIS5-3071")
    data = validate_request(request)
    reference_number = get_reference_number(data)
    do_something_service(reference_number)


def validate_request(request):
    data = request.get_json()
    if not data:
        print("Ain't got no data, mate")
        raise ValueError()
    print("We gots data!")
    return data


def get_reference_number(data):
    print("This is completely arbitrary data")
    try:
        return data["Identity"]["Reference"]
    except Exception as err:
        print(f"Failed to get reference number: {err}")
        raise err
