import logging
from unittest.mock import Mock, patch, MagicMock

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


def test_lms_update_case_contact_information_calls_get_contact_details_fields_once_with_correct_parameters(
        mock_case_update_service):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id
    )
    mock_blaise_case = MagicMock(spec=BlaiseUpdateCaseBase)
    mock_blaise_case.case_id = case_id
    mock_blaise_case.outcome_code = 0
    mock_blaise_case.get_contact_details_fields.return_value = {
        BlaiseFields.knock_to_nudge_contact_name: "Joe Bloggs",
        BlaiseFields.telephone_number_1: "01234567890",
        BlaiseFields.telephone_number_2: "07123123123",
    }

    # act
    mock_case_update_service._update_case_contact_information(mock_totalmobile_request, mock_blaise_case)

    # assert
    mock_blaise_case.get_contact_details_fields.assert_called_once_with(mock_totalmobile_request)


def test_lms_update_case_contact_information_logs_contact_information_has_not_been_updated(
        mock_case_update_service, caplog):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id, 999
    )
    mock_blaise_case = MagicMock(spec=BlaiseUpdateCaseBase)
    mock_blaise_case.case_id = case_id
    mock_blaise_case.outcome_code = 0
    mock_blaise_case.get_contact_details_fields.return_value = {}

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service._update_case_contact_information(mock_totalmobile_request, mock_blaise_case)

    # assert
    assert (
                f"Contact information has not been updated as no contact information was provided (Questionnaire=LMS2101_AA1, "
                f"Case Id=90001, Blaise hOut=0, "
                f"TM hOut=999)"
            ) in caplog.messages

def test_lms_update_case_contact_information_calls_get_knock_to_nudge_indicator_flag_field_once(mock_case_update_service):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    mock_blaise_case = MagicMock(spec=BlaiseUpdateCaseBase)
    mock_blaise_case.case_id = case_id
    mock_blaise_case.outcome_code = 0
    mock_blaise_case.get_contact_details_fields.return_value = {
        BlaiseFields.knock_to_nudge_contact_name: "Joe Bloggs",
        BlaiseFields.telephone_number_1: "01234567890",
        BlaiseFields.telephone_number_2: "07123123123",
    }
    mock_blaise_case.get_knock_to_nudge_indicator_flag_field.return_value = {BlaiseFields.knock_to_nudge_indicator: "1"}
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id
    )

    # act
    mock_case_update_service._update_case_contact_information(mock_totalmobile_request, mock_blaise_case)

    # assert
    mock_blaise_case.get_knock_to_nudge_indicator_flag_field.assert_called_once()


def test_lms_update_case_contact_information_update_case_once_with_correct_parameters(mock_case_update_service):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    mock_contact_details = {
        BlaiseFields.knock_to_nudge_contact_name: "Joe Bloggs",
        BlaiseFields.telephone_number_1: "01234567890",
        BlaiseFields.telephone_number_2: "07123123123",
    }
    mock_knock_to_nudge_indicator = {BlaiseFields.knock_to_nudge_indicator: "1"}
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id
    )
    mock_case_update_service._blaise_service = MagicMock()
    mock_blaise_case = MagicMock(spec=BlaiseUpdateCaseBase)
    mock_blaise_case.case_id = case_id
    mock_blaise_case.outcome_code = 0

    mock_blaise_case.get_contact_details_fields.return_value = mock_contact_details
    mock_blaise_case.get_knock_to_nudge_indicator_flag_field.return_value = mock_knock_to_nudge_indicator

    expected_fields = mock_contact_details | mock_knock_to_nudge_indicator

    # act
    mock_case_update_service._update_case_contact_information(mock_totalmobile_request, mock_blaise_case)

    # assert
    mock_case_update_service._blaise_service.update_case.assert_called_once_with(
        questionnaire_name, case_id, expected_fields
    )


def test_lms_update_case_contact_information_logs_contact_information_updated(mock_case_update_service, caplog):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(
        questionnaire_name, case_id, 999
    )
    mock_blaise_case = MagicMock(spec=BlaiseUpdateCaseBase)
    mock_blaise_case.case_id = case_id
    mock_blaise_case.outcome_code = 0
    mock_blaise_case.get_contact_details_fields.return_value = {
        BlaiseFields.knock_to_nudge_contact_name: "Joe Bloggs",
        BlaiseFields.telephone_number_1: "01234567890",
        BlaiseFields.telephone_number_2: "07123123123",
    }
    mock_blaise_case.get_knock_to_nudge_indicator_flag_field.return_value = {BlaiseFields.knock_to_nudge_indicator: "1"}

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service._update_case_contact_information(mock_totalmobile_request, mock_blaise_case)

    # assert
    assert (
            f"Contact information updated (Questionnaire=LMS2101_AA1, "
            f"Case Id=90001, Blaise hOut=0, "
            f"TM hOut=999)"
        ) in caplog.messages