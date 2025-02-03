from unittest.mock import Mock, patch

import pytest

from enums.blaise_fields import BlaiseFields
from models.update.blaise_update_case_model import BlaiseUpdateCase
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
def test_update_case_calls_validate_questionnaire_exists_once_with_correct_parameters(
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
    mock_get_existing_blaise_case.return_value = BlaiseUpdateCase(
        questionnaire_name, case_data
    )
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id
    )

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_validate.assert_called_once_with(mock_totalmobile_request.questionnaire_name)


def test_update_case_calls_get_existing_blaise_case_once_with_correct_parameters(
    mock_case_update_service,
):
    # arrange
    mock_case_update_service.get_existing_blaise_case = Mock()
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper()

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service.get_existing_blaise_case.assert_called_once_with(
        mock_totalmobile_request.questionnaire_name, mock_totalmobile_request.case_id
    )


@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
def test_update_case_calls_should_update_case_contact_information_once_with_correct_parameters(
    mock_get_existing_blaise_case, mock_case_update_service
):
    # arrange
    mock_case_update_service._should_update_case_contact_information = Mock()
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper()
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_blaise_case = BlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service._should_update_case_contact_information.assert_called_once_with(
        mock_blaise_case, mock_totalmobile_request
    )


@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
@patch.object(LMSUpdateCaseService, "_should_update_case_contact_information")
def test_update_case_calls_update_case_contact_information_once_with_correct_parameters(
    mock_should_update_case_contact_information,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    mock_case_update_service._update_case_contact_information = Mock()
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper()
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_blaise_case = BlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case
    mock_should_update_case_contact_information.return_value = True

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service._update_case_contact_information.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case
    )


@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
@patch.object(LMSUpdateCaseService, "_should_update_case_contact_information")
def test_update_case_calls_should_update_case_outcome_code_once_with_correct_parameters(
    mock_should_update_case_contact_information,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    mock_case_update_service._should_update_case_outcome_code = Mock()
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper()
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_blaise_case = BlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case
    mock_should_update_case_contact_information.return_value = False

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service._should_update_case_outcome_code.assert_called_once_with(
        mock_totalmobile_request
    )


@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
@patch.object(LMSUpdateCaseService, "_should_update_case_contact_information")
@patch.object(LMSUpdateCaseService, "_should_update_case_outcome_code")
def test_update_case_calls_update_case_outcome_code_once_with_correct_parameters(
    mock_should_update_case_outcome_code,
    mock_should_update_case_contact_information,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    mock_case_update_service._update_case_outcome_code = Mock()
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper()
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_blaise_case = BlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case
    mock_should_update_case_contact_information.return_value = False
    mock_should_update_case_outcome_code.return_value = True

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service._update_case_outcome_code.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case
    )
