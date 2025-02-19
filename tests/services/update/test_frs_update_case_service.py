import logging
from unittest.mock import MagicMock, patch

import pytest

from enums.blaise_fields import BlaiseFields
from models.update.frs_blaise_update_case_model import FRSBlaiseUpdateCase
from services.update.frs_update_case_service import FRSUpdateCaseService
from tests.helpers.totalmobile_incoming_update_request_helper import (
    frs_totalmobile_incoming_update_request_helper,
)


@pytest.fixture()
def mock_blaise_service():
    return MagicMock()


@pytest.fixture()
def mock_case_update_service(mock_blaise_service):
    return FRSUpdateCaseService(mock_blaise_service)


@pytest.fixture()
def mock_questionnaire_and_case_data():
    questionnaire_name = "FRS2102"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.refusal_reason: 0,
    }
    return questionnaire_name, case_id, case_data


@pytest.fixture()
def mock_totalmobile_request(mock_questionnaire_and_case_data):
    questionnaire_name, case_id, _ = mock_questionnaire_and_case_data
    return frs_totalmobile_incoming_update_request_helper(questionnaire_name, case_id)


@pytest.fixture()
def mock_blaise_case_data(mock_questionnaire_and_case_data):
    questionnaire_name, _, case_data = mock_questionnaire_and_case_data
    return FRSBlaiseUpdateCase(questionnaire_name, case_data)


@pytest.fixture()
def mock_blaise_case_object():
    return MagicMock(spec=FRSBlaiseUpdateCase)


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
def test_frs_update_case_calls_get_outcome_code_fields_once_with_correct_parameter_when_outcome_code_not_in_refusal_reason(
    mock_get_existing_blaise_case,
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
):
    # arrange
    mock_totalmobile_request.outcome_code = 522
    mock_get_existing_blaise_case.return_value = mock_blaise_case_object

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_blaise_case_object.get_outcome_code_fields.assert_called_once_with(
        mock_totalmobile_request
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
def test_frs_update_case_calls_get_outcome_code_fields_once_with_correct_parameter_when_outcome_code_in_refusal_reason(
    mock_get_existing_blaise_case,
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
):
    # arrange
    mock_totalmobile_request.outcome_code = 410
    mock_get_existing_blaise_case.return_value = mock_blaise_case_object

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_blaise_case_object.get_outcome_code_fields.assert_called_once_with(
        mock_totalmobile_request
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
def test_frs_update_case_calls_get_refusal_reason_fields_once_with_correct_parameter_when_outcome_code_in_refusal_reason(
    mock_get_existing_blaise_case,
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
):
    # arrange
    mock_totalmobile_request.outcome_code = 410
    mock_get_existing_blaise_case.return_value = mock_blaise_case_object

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_blaise_case_object.get_refusal_reason_fields.assert_called_once_with(
        mock_totalmobile_request
    )


@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
def test_frs_update_case_does_not_call_get_refusal_reason_fields_once_with_correct_parameter_when_outcome_code_not_in_refusal_reason(
    mock_get_existing_blaise_case,
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
):
    # arrange
    mock_totalmobile_request.outcome_code = 522
    mock_get_existing_blaise_case.return_value = mock_blaise_case_object

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_blaise_case_object.get_refusal_reason_fields.assert_not_called()


@patch.object(FRSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
def test_frs_update_case_logs_expected_message_when_totalmobile_outcome_code_is_invalid(
    mock_get_existing_blaise_case,
    _mock_validate,
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_data,
    caplog,
):
    # arrange
    mock_totalmobile_request.outcome_code = 999
    mock_get_existing_blaise_case.return_value = mock_blaise_case_data

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    assert (
        f"Case 90001 for questionnaire FRS2102 "
        f"has not been updated in Blaise (Blaise hOut=0, "
        f"TM hOut=999)"
    ) in caplog.messages


@pytest.mark.parametrize(
    "outcome_code, expected_fields",
    [
        (310, {BlaiseFields.outcome_code: "310"}),
        (512, {BlaiseFields.outcome_code: "512"}),
        (620, {BlaiseFields.outcome_code: "620"}),
        (410, {BlaiseFields.outcome_code: "410", BlaiseFields.refusal_reason: "410"}),
        (432, {BlaiseFields.outcome_code: "432", BlaiseFields.refusal_reason: "432"}),
        (450, {BlaiseFields.outcome_code: "450", BlaiseFields.refusal_reason: "450"}),
    ],
)
def test_frs_update_case_calls_blaise_service_update_case_once_with_correct_parameters(
    mock_case_update_service,
    mock_questionnaire_and_case_data,
    mock_totalmobile_request,
    outcome_code,
    expected_fields,
):
    # arrange
    mock_case_update_service._blaise_service = MagicMock()
    questionnaire_name, case_id, _ = mock_questionnaire_and_case_data
    mock_totalmobile_request.outcome_code = outcome_code

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service._blaise_service.update_case.assert_called_once_with(
        questionnaire_name, case_id, expected_fields
    )


@patch.object(FRSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
def test_frs_update_case_logs_expected_message_when_outcome_code_received_was_within_400_range(
    mock_get_existing_blaise_case,
    _mock_validate_questionnaire_exists,
    mock_totalmobile_request,
    mock_case_update_service,
    mock_blaise_case_object,
    caplog,
):
    # arrange
    outcome_code = 410
    mock_totalmobile_request.outcome_code = outcome_code
    mock_get_existing_blaise_case.return_value = mock_blaise_case_object
    mock_blaise_case_object.get_refusal_reason_fields.return_value = {
        BlaiseFields.outcome_code: outcome_code,
        BlaiseFields.refusal_reason: outcome_code,
    }

    mock_blaise_case_object.case_id = 90001
    mock_blaise_case_object.outcome_code = 0
    mock_blaise_case_object.refusal_reason = 0

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    assert (
        f"Outcome code and refusal reason updated (Questionnaire=FRS2102, "
        f"Case Id=90001, Blaise hOut=0, Blaise RefReas=0, "
        f"TM hOut=410)"
    ) in caplog.messages


@patch.object(FRSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(FRSUpdateCaseService, "get_existing_blaise_case")
def test_frs_update_case_logs_expected_message_when_outcome_code_received_was_not_within_400_range_and_valid(
    mock_get_existing_blaise_case,
    _mock_validate_questionnaire_exists,
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
    caplog,
):
    # arrange
    outcome_code = 620
    mock_totalmobile_request.outcome_code = outcome_code
    mock_get_existing_blaise_case.return_value = mock_blaise_case_object
    mock_blaise_case_object.get_outcome_code_fields.return_value = {
        BlaiseFields.outcome_code: outcome_code,
    }
    mock_blaise_case_object.case_id = 90001
    mock_blaise_case_object.outcome_code = 0

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    assert (
        f"Outcome code updated (Questionnaire=FRS2102, "
        f"Case Id=90001, Blaise hOut=0, "
        f"TM hOut=620)"
    ) in caplog.messages


def test_frs_update_case_implements_frs_blaise_update_case_type(
    mock_case_update_service,
    mock_blaise_case_object,
    mock_totalmobile_request,
    mock_questionnaire_and_case_data,
):
    # arrange
    mock_case_update_service.get_existing_blaise_case = MagicMock(
        return_value=mock_blaise_case_object
    )

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    assert isinstance(
        mock_case_update_service.get_existing_blaise_case.return_value,
        FRSBlaiseUpdateCase,
    )
