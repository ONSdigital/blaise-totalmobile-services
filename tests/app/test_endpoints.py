import json
from unittest import mock


def assert_security_headers_are_present(response):
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Strict-Transport-Security"] == "max-age=86400"
    assert response.headers["Cache-Control"] == "no-store"
    assert response.headers["Pragma"] == "no-cache"
    assert response.headers["Content-Security-Policy"] == "default-src 'self'"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_health_check(client):
    response = client.get("/bts/V1/health")
    assert json.loads(response.get_data(as_text=True)) == {"healthy": True}
    assert response.status_code == 200
    assert_security_headers_are_present(response)


@mock.patch("app.endpoints.update_visit_status_request_handler")
def test_update_visit_status_request(mock_handler, client, test_auth_header):
    response = client.post("/bts/updatevisitstatusrequest", headers=test_auth_header)
    assert response.status_code == 200
    assert response.text == "ok"
    mock_handler.assert_called()
    assert_security_headers_are_present(response)


@mock.patch("app.endpoints.submit_form_result_request_handler")
def test_submit_form_result_request(mock_handler, client, test_auth_header):
    response = client.post("/bts/submitformresultrequest", headers=test_auth_header)
    assert response.status_code == 200
    assert response.text == "ok"
    mock_handler.assert_called()
    assert_security_headers_are_present(response)


@mock.patch("app.endpoints.complete_visit_request_handler")
def test_complete_visit_request(mock_handler, client, test_auth_header):
    response = client.post("/bts/completevisitrequest", headers=test_auth_header)
    assert response.status_code == 200
    assert response.text == "ok"
    mock_handler.assert_called()
    assert_security_headers_are_present(response)


def test_update_visit_status_request_returns_401_without_auth(
    client, upload_visit_status_request_sample
):
    response = client.post(
        "/bts/updatevisitstatusrequest",
        json=upload_visit_status_request_sample,
    )
    assert response.status_code == 401


def test_submit_form_result_request_returns_401_without_auth(
    client, submit_form_result_request_sample
):
    response = client.post(
        "/bts/submitformresultrequest",
        json=submit_form_result_request_sample,
    )
    assert response.status_code == 401


def test_complete_visit_request_returns_401_without_auth(
    client, complete_visit_request_sample
):
    response = client.post(
        "/bts/completevisitrequest",
        json=complete_visit_request_sample,
    )
    assert response.status_code == 401
