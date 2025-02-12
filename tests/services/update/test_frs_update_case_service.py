import logging
from unittest.mock import Mock, patch

import pytest

from enums.blaise_fields import BlaiseFields
from models.update.lms_blaise_update_case_model import LMSBlaiseUpdateCase
from services.update.frs_update_case_service import FRSUpdateCaseService
from tests.helpers.totalmobile_incoming_update_request_helper import (
    frs_totalmobile_incoming_update_request_helper,
)


@pytest.fixture()
def mock_blaise_service():
    return Mock()


@pytest.fixture()
def mock_case_update_service(mock_blaise_service):
    return FRSUpdateCaseService(mock_blaise_service)


@patch.object(FRSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
def test_frs_update_case_calls_validate_questionnaire_exists_once_with_correct_parameters(
    mock_get_existing_blaise_case,
    mock_validate,
    mock_case_update_service,
):
    # arrange
    questionnaire_name = "FRS2102"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_get_existing_blaise_case.return_value = LMSBlaiseUpdateCase(
        questionnaire_name, case_data
    )
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id
    )

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_validate.assert_called_once_with(mock_totalmobile_request.questionnaire_name)


@patch.object(FRSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
def test_frs_update_case_calls_get_existing_blaise_case_once_with_correct_parameters(
    mock_get_existing_blaise_case,
    _mock_validate,
    mock_case_update_service,
):
    # arrange
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper(
        "FRS2102", "90001"
    )

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_get_existing_blaise_case.assert_called_once_with(
        mock_totalmobile_request.questionnaire_name, mock_totalmobile_request.case_id
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
@patch.object(FRSUpdateCaseService, "update_case_outcome_code")
def test_frs_update_case_calls_update_case_outcome_code_once_with_correct_parameter_when_outcome_code_not_in_refusal_reason(
    mock_update_case_outcome_code,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    questionnaire_name = "FRS2102"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id, 522
    )
    mock_blaise_case = LMSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_update_case_outcome_code.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
@patch.object(FRSUpdateCaseService, "update_case_outcome_code")
def test_frs_update_case_calls_update_case_outcome_code_once_with_correct_parameter_when_outcome_code_in_refusal_reason(
    mock_update_case_outcome_code,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    questionnaire_name = "FRS2102"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id, 410
    )
    mock_blaise_case = LMSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_update_case_outcome_code.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
@patch.object(FRSUpdateCaseService, "update_case_outcome_code")
@patch.object(FRSUpdateCaseService, "update_refusal_reason")
def test_frs_update_case_calls_update_refusal_reason_once_with_correct_parameter_when_outcome_code_in_refusal_reason(
    mock_update_refusal_reason,
    _mock_update_case_outcome_code,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    questionnaire_name = "FRS2102"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id, 410
    )
    mock_blaise_case = LMSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_update_refusal_reason.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case
    )


@patch.object(FRSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
def test_frs_update_case_logs_information_when_case_has_not_been_updated(
    mock_get_existing_blaise_case, _mock_validate, mock_case_update_service, caplog
):
    # arrange
    questionnaire_name = "FRS2102"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }

    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id, 999
    )
    mock_blaise_case = LMSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    assert (
        f"Case 90001 for questionnaire FRS2102 "
        f"has not been updated in Blaise (Blaise hOut=0, "
        f"TM hOut=999)"
    ) in caplog.messages
