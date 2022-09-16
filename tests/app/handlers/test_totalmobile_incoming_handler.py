from unittest import mock

import pytest

from app.handlers.totalmobile_incoming_handler import submit_form_result_request_handler
from tests.helpers import incoming_request_helper


def test_submit_form_result_request_handler():

    mock_request = mock.Mock()
    mock_request.get_json.return_value = (
        incoming_request_helper.get_populated_update_case_refusal_request()
    )
    mock_update_case_service = mock.Mock()
    mock_update_case_service.update_case()

    submit_form_result_request_handler(mock_request, mock_update_case_service)

    mock_update_case_service.update_case.assert_called()


def test_submit_form_result_request_handler_blah():

    mock_request = mock.Mock()
    mock_request.get_json.return_value = (
        incoming_request_helper.get_malformed_update_case_request()
    )
    mock_update_case_service = mock.Mock()
    mock_update_case_service.update_case()

    with pytest.raises(Exception):
        submit_form_result_request_handler(mock_request, mock_update_case_service)
