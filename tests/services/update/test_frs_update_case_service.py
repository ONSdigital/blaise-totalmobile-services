from unittest.mock import Mock, patch

import pytest

from enums.blaise_fields import BlaiseFields
from models.update.frs_blaise_update_case_model import FRSBlaiseUpdateCase
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
def test_update_case_calls_validate_questionnaire_exists_once_with_correct_parameters(
    mock_get_existing_blaise_case,
    mock_validate,
    mock_case_update_service,
):
    # arrange
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    mock_get_existing_blaise_case.return_value = FRSBlaiseUpdateCase(
        questionnaire_name, case_data
    )
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper(
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
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper()

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service.get_existing_blaise_case.assert_called_once_with(
        mock_totalmobile_request.questionnaire_name, mock_totalmobile_request.case_id
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
def test_update_case_calls_should_update_case_outcome_code_once_with_correct_parameters(
    mock_get_existing_blaise_case, mock_case_update_service
):
    # arrange
    mock_case_update_service._should_update_case_outcome_code = Mock()
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper()
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
    }
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service._should_update_case_outcome_code.assert_called_once_with(
        mock_blaise_case, mock_totalmobile_request
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
@patch.object(FRSUpdateCaseService, "_should_update_case_outcome_code")
def test_update_case_calls_update_case_outcome_code_once_with_correct_parameters(
    mock_should_update_case_outcome_code,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    mock_case_update_service._update_case_outcome_code = Mock()
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper()
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
    }
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case
    mock_should_update_case_outcome_code.return_value = True

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service._update_case_outcome_code.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
@patch.object(FRSUpdateCaseService, "_should_update_case_outcome_code")
def test_update_case_calls_should_update_refusal_reason_once_with_correct_parameters(
    mock_should_update_case_outcome_code,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    mock_case_update_service._should_update_refusal_reason = Mock()
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper()
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
    }
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case
    mock_should_update_case_outcome_code.return_value = False

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service._should_update_refusal_reason.assert_called_once_with(
        mock_blaise_case, mock_totalmobile_request
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
@patch.object(FRSUpdateCaseService, "_should_update_refusal_reason")
@patch.object(FRSUpdateCaseService, "_should_update_case_outcome_code")
def test_update_case_calls_update_refusal_reason_once_with_correct_parameters(
    mock_should_update_refusal_reason,
    mock_should_update_case_outcome_code,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    mock_case_update_service._update_case_outcome_code = Mock()
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper()
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
    }
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case
    mock_should_update_case_outcome_code.return_value = False
    mock_should_update_refusal_reason.return_value = True

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service._update_case_outcome_code.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
@patch.object(FRSUpdateCaseService, "_should_update_case_outcome_code")
def test_update_case_calls_log_no_update_once_with_correct_parameters(
    mock_should_update_case_outcome_code,
    mock_get_existing_blaise_case,
    mock_case_update_service,
):
    # arrange
    mock_case_update_service._log_no_update = Mock()
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper()
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
    }
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case
    mock_should_update_case_outcome_code.return_value = False

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service._log_no_update.assert_called_once_with(
        mock_blaise_case,
        mock_totalmobile_request,
    )


def test_update_case_outcome_code_calls_get_fields_to_update_case_outcome_code_once_with_correct_parameters(
    mock_case_update_service,
):
    # arrange
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper()
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
    }
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_case_update_service._get_fields_to_update_case_outcome_code = Mock()

    # act
    mock_case_update_service._update_case_outcome_code(
        mock_totalmobile_request, mock_blaise_case
    )

    # assert
    mock_case_update_service._get_fields_to_update_case_outcome_code.assert_called_once_with(
        mock_blaise_case, mock_totalmobile_request
    )


def test_update_case_outcome_code_calls_log_attempting_to_update_case_once_with_correct_parameters(
    mock_case_update_service,
):
    # arrange
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper()
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
    }
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_case_update_service._log_attempting_to_update_case = Mock()

    # act
    mock_case_update_service._update_case_outcome_code(
        mock_totalmobile_request, mock_blaise_case
    )

    # assert
    mock_case_update_service._log_attempting_to_update_case.assert_called_once_with(
        mock_totalmobile_request
    )


def test_update_case_outcome_code_calls_blaise_service_update_case_once_with_correct_parameters(
    mock_case_update_service,
):
    # arrange
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper()
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
    }
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)

    mock_fields_to_update = {"hOut": f"{mock_totalmobile_request.outcome_code}"}
    mock_blaise_case._get_fields_to_update_case_outcome_code = Mock(
        return_value=mock_fields_to_update
    )
    mock_case_update_service._blaise_service = Mock()
    mock_case_update_service._blaise_service.update_case = Mock()

    # act
    mock_case_update_service._update_case_outcome_code(
        mock_totalmobile_request, mock_blaise_case
    )

    # assert
    mock_case_update_service._blaise_service.update_case.assert_called_once_with(
        mock_totalmobile_request.questionnaire_name,
        mock_totalmobile_request.case_id,
        mock_fields_to_update,
    )


def test_update_case_outcome_code_calls_log_outcome_code_updated_once_with_correct_parameters(
    mock_case_update_service,
):
    # arrange
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper()
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
    }
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_case_update_service._log_outcome_code_updated = Mock()

    # act
    mock_case_update_service._update_case_outcome_code(
        mock_totalmobile_request, mock_blaise_case
    )

    # assert
    mock_case_update_service._log_outcome_code_updated.assert_called_once_with(
        mock_blaise_case,
        mock_totalmobile_request,
    )


@pytest.mark.parametrize(
    "totalmobile_outcome_code, blaise_outcome_code, expected_boolean",
    [
        (310, 0, True),
        (651, 310, True),
        (999, 310, False),
        (310, 888, False),
    ],
)
def test_should_update_case_outcome_code_returns_expected_boolean(
    totalmobile_outcome_code,
    blaise_outcome_code,
    expected_boolean,
    mock_case_update_service,
):
    # arrange
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper(
        outcome_code=totalmobile_outcome_code
    )
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: blaise_outcome_code,
    }
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)

    # act
    result = mock_case_update_service._should_update_case_outcome_code(
        mock_blaise_case, mock_totalmobile_request
    )

    # assert
    assert result == expected_boolean


def test_get_fields_to_update_case_outcome_code_returns_expected_fields(
    mock_case_update_service,
):
    # arrange
    totalmobile_outcome_code = 310
    mock_totalmobile_request = frs_totalmobile_incoming_update_request_helper(
        outcome_code=totalmobile_outcome_code
    )
    questionnaire_name = "FRS2102"
    case_id = "90002"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
    }
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)

    # act
    result = mock_case_update_service._get_fields_to_update_case_outcome_code(
        mock_blaise_case, mock_totalmobile_request
    )

    # assert
    assert result == {"hOut": str(totalmobile_outcome_code)}
