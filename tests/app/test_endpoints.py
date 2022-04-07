from app.app import app, load_config, setup_app


load_config(app)
setup_app(app)


def test_update_visit_status_request_returns_200(
    client, upload_visit_status_request_sample, test_auth_header
):
    response = client.post(
        "/ons/totalmobile-incoming/UpdateVisitStatusRequest",
        json=upload_visit_status_request_sample,
        headers=test_auth_header,
    )
    assert response.status_code == 200


def test_update_visit_status_request_returns_401_without_auth(
    client, upload_visit_status_request_sample
):
    response = client.post(
        "/ons/totalmobile-incoming/UpdateVisitStatusRequest",
        json=upload_visit_status_request_sample,
    )
    assert response.status_code == 401


def test_submit_form_result_request_returns_200(
    client, submit_form_result_request_sample, test_auth_header
):
    response = client.post(
        "/ons/totalmobile-incoming/SubmitFormResultRequest",
        json=submit_form_result_request_sample,
        headers=test_auth_header,
    )
    assert response.status_code == 200


def test_submit_form_result_request_returns_401_without_auth(
    client, submit_form_result_request_sample
):
    response = client.post(
        "/ons/totalmobile-incoming/SubmitFormResultRequest",
        json=submit_form_result_request_sample,
    )
    assert response.status_code == 401


def test_complete_visit_request_returns_200(
    client, complete_visit_request_sample, test_auth_header
):
    response = client.post(
        "/ons/totalmobile-incoming/CompleteVisitRequest",
        json=complete_visit_request_sample,
        headers=test_auth_header,
    )
    assert response.status_code == 200


def test_complete_visit_request_returns_401_without_auth(
    client, complete_visit_request_sample
):
    response = client.post(
        "/ons/totalmobile-incoming/CompleteVisitRequest",
        json=complete_visit_request_sample,
    )
    assert response.status_code == 401
