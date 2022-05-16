import pytest
import json

from app.app import app, load_config, setup_app

load_config(app)
setup_app(app)


@pytest.mark.parametrize(
    "url, expected_function_name",
    [
        (
            "/ons/totalmobile-incoming/SubmitFormResultRequest",
            "submit_form_result_request",
        ),
        (
            "/ons/totalmobile-incoming/UpdateVisitStatusRequest",
            "update_visit_status_request",
        ),
        (
            "/ons/totalmobile-incoming/CompleteVisitRequest",
            "complete_visit_request"
        ),
        (
            "/totalmobile-service/health",
            "health_check"
        ),
    ],
)
def test_an_endpoint_url_maps_to_the_expected_function_name(
    url, expected_function_name
):
    # arrange
    rules = app.url_map.iter_rules()

    # act
    result = [
        rule
        for rule in rules
        if expected_function_name in rule.endpoint
        if url in str(rule)
    ]

    # assert
    assert result


def test_update_visit_status_request_returns_401_without_auth(
        client, upload_visit_status_request_sample
):
    response = client.post(
        "/ons/totalmobile-incoming/UpdateVisitStatusRequest",
        json=upload_visit_status_request_sample,
    )
    assert response.status_code == 401


def test_submit_form_result_request_returns_401_without_auth(
    client, submit_form_result_request_sample
):
    response = client.post(
        "/ons/totalmobile-incoming/SubmitFormResultRequest",
        json=submit_form_result_request_sample,
    )
    assert response.status_code == 401


def test_complete_visit_request_returns_401_without_auth(
    client, complete_visit_request_sample
):
    response = client.post(
        "/ons/totalmobile-incoming/CompleteVisitRequest",
        json=complete_visit_request_sample,
    )
    assert response.status_code == 401


def test_health_check(
    client
):
    response = client.get(
        "/ons/totalmobile-incoming/V1/health"
    )
    assert json.loads(response.get_data(as_text=True)) == {"healthy": True}
    assert response.status_code == 200
