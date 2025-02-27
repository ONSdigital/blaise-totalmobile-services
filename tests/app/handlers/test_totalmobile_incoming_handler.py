from unittest import mock
from unittest.mock import MagicMock, patch

import pytest

from app.exceptions.custom_exceptions import (
    BadReferenceError,
    InvalidTotalmobileFRSRequestException,
    MissingReferenceError,
    SurveyDoesNotExistError,
)
from app.handlers.totalmobile_incoming_handler import (
    create_visit_request_handler,
    force_recall_visit_request_handler,
    submit_form_result_request_handler,
    verify_survey_type,
)
from tests.helpers import (
    incoming_request_helper,
    incoming_request_helper_for_frs_allocation,
    incoming_request_helper_for_frs_unallocation,
)


@patch("app.handlers.totalmobile_incoming_handler.ServiceInstanceFactory")
def test_submit_form_result_request_handler_calls_update_case_once(
    mock_service_factory,
):
    # arrange
    mock_service = MagicMock()
    mock_service_factory.return_value.create_update_case_service.return_value = (
        mock_service
    )

    mock_request = MagicMock()
    mock_request.get_json.return_value = (
        incoming_request_helper.get_populated_update_case_refusal_request()
    )

    mock_app = MagicMock()
    mock_app.blaise_service = MagicMock()

    # act
    submit_form_result_request_handler(mock_request, mock_app)

    # assert
    mock_service.update_case.assert_called_once()


def test_submit_form_result_request_handler_raises_an_exception_when_a_malformed_request_is_received():
    # arrange
    mock_request = mock.Mock()
    mock_request.get_json.return_value = (
        incoming_request_helper.get_malformed_update_case_request()
    )
    mock_update_case_service = mock.Mock()
    mock_update_case_service.update_case()

    # act & assert
    with pytest.raises(Exception):
        submit_form_result_request_handler(mock_request, mock_update_case_service)


@patch("app.handlers.totalmobile_incoming_handler.FRSCaseAllocationService")
@patch(
    "app.handlers.totalmobile_incoming_handler.TotalMobileIncomingFRSRequestModel.import_request"
)
def test_create_visit_request_handler_calls_create_case_once(
    mock_import_request, mock_frs_service
):
    # arrange
    mock_frs_instance = MagicMock()
    mock_frs_service.return_value = mock_frs_instance

    mock_totalmobile_case = MagicMock()
    mock_import_request.return_value = mock_totalmobile_case

    mock_request = MagicMock()
    mock_request.get_json.return_value = (
        incoming_request_helper_for_frs_allocation.get_frs_case_allocation_request()
    )

    mock_app = MagicMock()
    mock_app.cma_blaise_service = MagicMock()

    # act
    create_visit_request_handler(mock_request, mock_app)

    # assert
    mock_frs_instance.create_case.assert_called_once_with(mock_totalmobile_case)


def test_create_visit_request_handler_raises_invalid_totalmobile_frs_request_exception_if_reference_missing_from_payload():
    # arrange
    mock_request = mock.Mock()

    mock_request.get_json.return_value = (
        incoming_request_helper_for_frs_allocation.get_frs_case_allocation_request_without_reference()
    )
    mock_update_frs_case_allocation_service = mock.Mock()
    mock_update_frs_case_allocation_service.create_case()

    # act & assert
    with pytest.raises(InvalidTotalmobileFRSRequestException):
        create_visit_request_handler(
            mock_request, mock_update_frs_case_allocation_service
        )


@patch("app.handlers.totalmobile_incoming_handler.FRSCaseAllocationService")
def test_force_recall_visit_request_handler_calls_unallocate_case_once(
    mock_frs_service,
):
    # arrange
    mock_frs_instance = MagicMock()
    mock_frs_service.return_value = mock_frs_instance

    mock_request = MagicMock()
    mock_request.get_json.return_value = (
        incoming_request_helper_for_frs_unallocation.get_frs_case_unallocation_request()
    )

    mock_app = MagicMock()
    mock_app.cma_blaise_service = MagicMock()

    # act
    force_recall_visit_request_handler(mock_request, mock_app)

    # assert
    mock_frs_instance.unallocate_case.assert_called_once()


@pytest.mark.parametrize(
    "valid_survey_type",
    [
        "LMS",
        "FRS",
    ],
)
def test_verify_survey_type_does_not_raise_an_error_with_a_valid_survey_type(
    valid_survey_type,
):
    try:
        verify_survey_type(valid_survey_type)
    except Exception:
        pytest.fail("verify_survey_type() raised an exception unexpectedly.")


def test_verify_survey_type_raises_missing_reference_error():
    with pytest.raises(
        MissingReferenceError, match="Reference field is missing in association block"
    ):
        verify_survey_type(None)


@pytest.mark.parametrize(
    "invalid_survey_type",
    [
        123,
        45.6,
        [],
        {},
        True,
        False,
        "LM",
    ],
)
def test_verify_survey_type_raises_bad_reference_error(invalid_survey_type):
    with pytest.raises(
        BadReferenceError, match="Reference field in association block is invalid"
    ):
        verify_survey_type(invalid_survey_type)


def test_verify_survey_type_is_not_a_valid_survey_tla(caplog):
    with pytest.raises(SurveyDoesNotExistError):
        verify_survey_type("XYZ")
    assert "survey_type of 'XYZ' is invalid" in caplog.messages
