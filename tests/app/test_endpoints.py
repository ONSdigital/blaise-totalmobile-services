import pytest
from run import app as flask_app


def test_submit_form_result_request_maps_to_the_correct_url():
    # arrange
    adapter = flask_app.url_map.bind('')

    # act
    result = adapter.match("/ons/totalmobile-incoming/SubmitFormResultRequest", method='POST')

    # assert
    assert result is not None


@pytest.mark.parametrize(
    "url, expected_function_name",
    [
        ("/ons/totalmobile-incoming/SubmitFormResultRequest", "submit_form_result_request"),
        ("/ons/totalmobile-incoming/UpdateVisitStatusRequest", "update_visit_status_request"),
        ("/ons/totalmobile-incoming/CompleteVisitRequest", "complete_visit_request"),
    ],
)
def test_an_endpoint_url_maps_to_the_expected_function_name(url, expected_function_name):
    # arrange
    rules = flask_app.url_map.iter_rules()

    # act
    result = [rule for rule in rules if expected_function_name in rule.endpoint if url in str(rule)]

    # assert
    assert result
