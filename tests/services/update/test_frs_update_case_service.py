import logging
from unittest.mock import MagicMock, patch

import pytest

from enums.blaise_fields import BlaiseFields
from models.update.frs_blaise_update_case_model import FRSBlaiseUpdateCase
from models.update.lms_blaise_update_case_model import LMSBlaiseUpdateCase
from services.update.frs_update_case_service import FRSUpdateCaseService
from tests.helpers.totalmobile_incoming_update_request_helper import (
    frs_totalmobile_incoming_update_request_helper,
)


@pytest.fixture()
def mock_blaise_service():
    return MagicMock ()


@pytest.fixture()
def mock_case_update_service(mock_blaise_service):
    return FRSUpdateCaseService(mock_blaise_service)


@pytest.fixture()
def setup_data():
    questionnaire_name = "FRS2102"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    return questionnaire_name, case_id, case_data


@pytest.fixture()
def mock_totalmobile_request(setup_data):
    questionnaire_name, case_id, _ = setup_data
    return frs_totalmobile_incoming_update_request_helper(questionnaire_name, case_id)


@patch.object(FRSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
def test_frs_update_case_calls_validate_questionnaire_exists_once_with_correct_parameters(
    _mock_get_existing_blaise_case,
    mock_validate,
    mock_case_update_service,
    mock_totalmobile_request,
):
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
    mock_totalmobile_request,
):
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
    setup_data,
    mock_totalmobile_request,
):
    # arrange
    questionnaire_name, case_id, case_data = setup_data
    mock_totalmobile_request.outcome_code = 522
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
    setup_data,
    mock_totalmobile_request,
):
    # arrange
    questionnaire_name, case_id, case_data = setup_data
    mock_totalmobile_request.outcome_code = 410
    mock_blaise_case = FRSBlaiseUpdateCase(questionnaire_name, case_data)
    mock_get_existing_blaise_case.return_value = mock_blaise_case

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_update_case_outcome_code.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
@patch.object(FRSUpdateCaseService, "update_refusal_reason")
def test_frs_update_case_calls_update_refusal_reason_once_with_correct_parameter_when_outcome_code_in_refusal_reason(
    mock_update_refusal_reason,
    mock_get_existing_blaise_case,
    mock_case_update_service,
    setup_data,
    mock_totalmobile_request,
):
    # arrange
    questionnaire_name, case_id, case_data = setup_data
    mock_totalmobile_request.outcome_code = 410
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
    mock_get_existing_blaise_case,
    _mock_validate,
    mock_case_update_service,
    caplog,
    setup_data,
    mock_totalmobile_request,
):
    # arrange
    questionnaire_name, case_id, case_data = setup_data
    mock_totalmobile_request.outcome_code = 999
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


def test_frs_update_case_outcome_code_calls_get_outcome_code_fields_once_with_correct_parameters(
    mock_case_update_service, setup_data, mock_totalmobile_request
):
    # arrange
    questionnaire_name, case_id, _ = setup_data
    mock_blaise_case = MagicMock(spec=FRSBlaiseUpdateCase)

    # act
    mock_case_update_service.update_case_outcome_code(
        mock_totalmobile_request, mock_blaise_case
    )

    # assert
    mock_blaise_case.get_outcome_code_fields.assert_called_once_with(
        mock_totalmobile_request
    )


def test_frs_update_case_outcome_code_calls_update_case_once_with_correct_parameters(
    mock_case_update_service, setup_data, mock_totalmobile_request
):
    # arrange
    questionnaire_name, case_id, _ = setup_data
    outcome_code = 620
    mock_totalmobile_request.outcome_code = outcome_code
    mock_blaise_case = MagicMock(spec=LMSBlaiseUpdateCase)
    mock_blaise_case.get_outcome_code_fields.return_value = {
        BlaiseFields.outcome_code: outcome_code
    }
    mock_case_update_service._blaise_service = MagicMock()
    expected_fields = {"hOut": outcome_code}

    # act
    mock_case_update_service.update_case_outcome_code(
        mock_totalmobile_request, mock_blaise_case
    )

    # assert
    mock_case_update_service._blaise_service.update_case.assert_called_once_with(
        questionnaire_name, case_id, expected_fields
    )


def test_frs_update_case_outcome_code_logs_information_when_outcome_code_has_been_updated(
    mock_case_update_service, setup_data, mock_totalmobile_request, caplog
):
    # arrange
    questionnaire_name, case_id, _ = setup_data
    mock_totalmobile_request.outcome_code = 620
    mock_blaise_case = MagicMock(spec=FRSBlaiseUpdateCase)
    mock_blaise_case.case_id = case_id
    mock_blaise_case.outcome_code = 0

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service.update_case_outcome_code(
            mock_totalmobile_request, mock_blaise_case
        )

    # assert
    assert (
        f"Outcome code updated (Questionnaire=FRS2102, "
        f"Case Id=90001, Blaise hOut=0, "
        f"TM hOut=620)"
    ) in caplog.messages


def test_frs_update_refusal_reason_calls_get_refusal_reason_fields_once_with_correct_parameters(
    mock_case_update_service, setup_data, mock_totalmobile_request
):
    # arrange
    questionnaire_name, case_id, _ = setup_data
    mock_blaise_case = MagicMock(spec=FRSBlaiseUpdateCase)

    # act
    mock_case_update_service.update_refusal_reason(
        mock_totalmobile_request, mock_blaise_case
    )

    # assert
    mock_blaise_case.get_refusal_reason_fields.assert_called_once_with(
        mock_totalmobile_request
    )


def test_frs_update_refusal_reason_calls_update_case_once_with_correct_parameters(
    mock_case_update_service, setup_data, mock_totalmobile_request
):
    # arrange
    questionnaire_name, case_id, _ = setup_data
    outcome_code = 410
    mock_totalmobile_request.outcome_code = outcome_code
    mock_case_update_service._blaise_service = MagicMock()
    mock_blaise_case = MagicMock(spec=FRSBlaiseUpdateCase)
    mock_blaise_case.get_refusal_reason_fields.return_value = {
        BlaiseFields.outcome_code: outcome_code,
        BlaiseFields.refusal_reason: outcome_code,
    }

    expected_fields = {
        "hOut": outcome_code,
        "qDataBag.RefReas": outcome_code,
    }

    # act
    mock_case_update_service.update_refusal_reason(
        mock_totalmobile_request, mock_blaise_case
    )

    # assert
    mock_case_update_service._blaise_service.update_case.assert_called_once_with(
        questionnaire_name, case_id, expected_fields
    )


def test_frs_update_refusal_reason_logs_information_when_outcome_code_and_refusal_reason_have_been_updated(
    mock_case_update_service, setup_data, mock_totalmobile_request, caplog
):
    # arrange
    questionnaire_name, case_id, _ = setup_data
    mock_totalmobile_request.outcome_code = 410
    mock_blaise_case = MagicMock(spec=FRSBlaiseUpdateCase)
    mock_blaise_case.case_id = case_id
    mock_blaise_case.outcome_code = 0

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service.update_refusal_reason(
            mock_totalmobile_request, mock_blaise_case
        )

    # assert
    assert (
        f"Outcome code and refusal reason updated (Questionnaire=FRS2102, "
        f"Case Id=90001, Blaise hOut=0, "
        f"TM hOut=410)"
    ) in caplog.messages
