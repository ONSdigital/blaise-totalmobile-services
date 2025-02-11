import logging
from unittest.mock import Mock, patch

import pytest

from enums.blaise_fields import BlaiseFields
from models.update.blaise_update_case_model import BlaiseUpdateCaseBase
from services.update.lms_update_case_service import LMSUpdateCaseService
from tests.helpers.totalmobile_incoming_update_request_helper import (
    lms_totalmobile_incoming_update_request_helper,
)


@pytest.fixture()
def mock_blaise_service():
    return Mock()


@pytest.fixture()
def mock_case_update_service(mock_blaise_service):
    return LMSUpdateCaseService(mock_blaise_service)


@patch.object(LMSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
def test_lms_update_case_calls_validate_questionnaire_exists_once_with_correct_parameters(
    mock_get_existing_blaise_case,
    mock_validate,
    mock_case_update_service,
):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_get_existing_blaise_case.return_value = BlaiseUpdateCaseBase(
        questionnaire_name, case_data
    )
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id
    )

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_validate.assert_called_once_with(mock_totalmobile_request.questionnaire_name)


@patch.object(LMSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
def test_lms_update_case_calls_get_existing_blaise_case_once_with_correct_parameters(
    mock_get_existing_blaise_case,
    _mock_validate,
    mock_case_update_service,
):
    # arrange
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(
        "LMS2101_AA1", "90001"
    )

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_get_existing_blaise_case.assert_called_once_with(
        mock_totalmobile_request.questionnaire_name, mock_totalmobile_request.case_id
    )


@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
@patch.object(LMSUpdateCaseService, "_update_case_contact_information")
def test_lms_update_case_calls_update_case_contact_information_once_with_correct_parameter(
    mock_update_case_contact_information,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id, 300
    )
    mock_blaise_case = BlaiseUpdateCaseBase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_update_case_contact_information.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case
    )


@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
@patch.object(LMSUpdateCaseService, "update_case_outcome_code")
def test_lms_update_case_calls_update_case_outcome_code_once_with_correct_parameter(
    mock_update_case_outcome_code,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id, 460
    )
    mock_blaise_case = BlaiseUpdateCaseBase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_update_case_outcome_code.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case
    )


@patch.object(LMSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
def test_lms_update_case_logs_information_when_case_has_not_been_updated(
    mock_get_existing_blaise_case, _mockvalidate, mock_case_update_service, caplog
):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }

    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id, 999
    )
    mock_blaise_case = BlaiseUpdateCaseBase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    assert (
        f"Case 90001 for questionnaire LMS2101_AA1 "
        f"has not been updated in Blaise (Blaise hOut=0, "
        f"TM hOut=999)"
    ) in caplog.messages
