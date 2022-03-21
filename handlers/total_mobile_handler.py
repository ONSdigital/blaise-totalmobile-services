from services.total_mobile_service import (
    update_visit_status_request_service, submit_form_result_request_service, complete_visit_request_service)


def update_visit_status_request_handler(request):
    data = request.get_json()
    if not data:
        return "No data sent", 500

    try:
        reference = data["Identity"]["Reference"]
    except Exception as err:
        print(f"Failed to get reference number: {err}")
        return err, 500

    return update_visit_status_request_service(reference)


def submit_form_result_request_handler(request):
    data = request.get_json()
    if not data:
        return "No data sent", 500

    try:
        reference = data["Result"]["Association"]["Reference"]
    except Exception as err:
        print(f"Failed to get reference number: {err}")
        return err, 500

    return submit_form_result_request_service(reference)


def complete_visit_request_handler(request):
    data = request.get_json()
    if not data:
        return "No data sent", 500

    try:
        reference = data["Identity"]["Reference"]
    except Exception as err:
        print(f"Failed to get reference number: {err}")
        return err, 500

    return complete_visit_request_service(reference)
