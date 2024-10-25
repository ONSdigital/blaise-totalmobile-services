from unittest import mock

import pytest

from app.exceptions.custom_exceptions import InvalidTotalmobileFRSRequestException
from app.handlers.totalmobile_incoming_handler import (
    create_visit_request_handler,
    force_recall_visit_request_handler,
    submit_form_result_request_handler,
)
from tests.helpers import (
    incoming_request_helper,
    incoming_request_helper_for_frs_allocation,
    incoming_request_helper_for_frs_unallocation,
)


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


def test_create_visit_request_handler():

    mock_request = mock.Mock()
    mock_request.get_json.return_value = (
        incoming_request_helper_for_frs_allocation.get_frs_case_allocation_request()
    )
    mock_update_frs_case_allocation_service = mock.Mock()
    mock_update_frs_case_allocation_service.create_case()

    create_visit_request_handler(mock_request, mock_update_frs_case_allocation_service)

    mock_update_frs_case_allocation_service.create_case.assert_called()


def test_create_visit_request_handler_fails_if_reference_missing_from_payload():

    mock_request = mock.Mock()

    mock_request.get_json.return_value = (
        incoming_request_helper_for_frs_allocation.get_frs_case_allocation_request_without_reference()
    )
    mock_update_frs_case_allocation_service = mock.Mock()
    mock_update_frs_case_allocation_service.create_case()

    with pytest.raises(InvalidTotalmobileFRSRequestException):
        create_visit_request_handler(
            mock_request, mock_update_frs_case_allocation_service
        )


def test_force_recall_visit_request_handler():

    mock_request = mock.Mock()

    mock_request.get_json.return_value = (
        incoming_request_helper_for_frs_unallocation.get_frs_case_unallocation_request()
    )
    mock_update_frs_case_allocation_service = mock.Mock()
    mock_update_frs_case_allocation_service.unallocate_case()

    force_recall_visit_request_handler(
        mock_request, mock_update_frs_case_allocation_service
    )

    mock_update_frs_case_allocation_service.unallocate_case.assert_called()
