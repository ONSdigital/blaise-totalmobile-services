from services.total_mobile_service import persist_request_service


def update_visit_status_request_handler(request):
    data = request.get_json()
    if not data:
        return "No data sent", 500

    try:
        reference = data["Identity"]["Reference"]
    except Exception as err:
        print(f"Failed to get reference number: {err}")
        return err, 500

    return persist_request_service(reference, "UPDATE")


def submit_form_result_request_handler(request):
    data = request.get_json()
    if not data:
        return "No data sent", 500

    try:
        reference = data["Result"]["Association"]["Reference"]
    except Exception as err:
        print(f"Failed to get reference number: {err}")
        return err, 500

    return persist_request_service(reference, "SUBMITTED")


def complete_visit_request_handler(request):
    data = request.get_json()
    if not data:
        return "No data sent", 500

    try:
        reference = data["Identity"]["Reference"]
    except Exception as err:
        print(f"Failed to get reference number: {err}")
        return err, 500

    return persist_request_service(reference, "COMPLETED")
