def update_visit_status_request_handler(request):
    data = request.get_json()
    if not data:
        return "No data sent", 500

    try:
        return data["Identity"]["Reference"]
    except Exception as err:
        print(f"Failed to get reference number: {err}")
        return err, 500


def submit_form_result_request_handler(request):
    data = request.get_json()
    if not data:
        return "No data sent", 500

    try:
        return data["Result"]["Association"]["Reference"]
    except Exception as err:
        print(f"Failed to get reference number: {err}")
        return err, 500


def complete_visit_request_handler(request):
    data = request.get_json()
    if not data:
        return "No data sent", 500

    try:
        return data["Identity"]["Reference"]
    except Exception as err:
        print(f"Failed to get reference number: {err}")
        return err, 500
