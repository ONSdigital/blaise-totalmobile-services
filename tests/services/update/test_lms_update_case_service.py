import logging
from unittest.mock import MagicMock, Mock, PropertyMock, patch

import pytest

from enums.blaise_fields import BlaiseFields
from models.update.lms_blaise_update_case_model import LMSBlaiseUpdateCase
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


@pytest.fixture()
def mock_questionnaire_and_case_data():
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.call_history: False,
    }
    return questionnaire_name, case_id, case_data


@pytest.fixture()
def mock_blaise_case_data(mock_questionnaire_and_case_data):
    questionnaire_name, _, case_data = mock_questionnaire_and_case_data
    return LMSBlaiseUpdateCase(questionnaire_name, case_data)


@pytest.fixture()
def mock_totalmobile_request(mock_questionnaire_and_case_data):
    questionnaire_name, case_id, _ = mock_questionnaire_and_case_data
    return lms_totalmobile_incoming_update_request_helper(questionnaire_name, case_id)


@pytest.fixture()
def mock_blaise_case_object():
    return MagicMock(spec=LMSBlaiseUpdateCase)


@patch.object(LMSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
def test_lms_update_case_calls_validate_questionnaire_exists_once_with_correct_parameters(
    _mock_get_existing_blaise_case,
    mock_validate,
    mock_case_update_service,
    mock_totalmobile_request,
):
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
    mock_totalmobile_request,
):
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
    mock_totalmobile_request,
    mock_blaise_case_data,
):
    # arrange
    mock_totalmobile_request.outcome_code = 300
    mock_get_existing_blaise_case.return_value = mock_blaise_case_data

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_update_case_contact_information.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case_data
    )


@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
@patch.object(LMSUpdateCaseService, "update_case_outcome_code")
def test_lms_update_case_calls_update_case_outcome_code_once_with_correct_parameter(
    mock_update_case_outcome_code,
    mock_get_existing_blaise_case,
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_data,
):
    # arrange
    mock_totalmobile_request.outcome_code = 460
    mock_get_existing_blaise_case.return_value = mock_blaise_case_data

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_update_case_outcome_code.assert_called_once_with(
        mock_totalmobile_request, mock_blaise_case_data
    )


@patch.object(LMSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
def test_lms_update_case_logs_information_when_case_has_not_been_updated(
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
        f"Case 90001 for questionnaire LMS2101_AA1 "
        f"has not been updated in Blaise (Blaise hOut=0, "
        f"TM hOut=999)"
    ) in caplog.messages


def test_lms_update_case_contact_information_calls_get_contact_details_fields_once_with_correct_parameters(
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
):
    # arrange
    mock_blaise_case_object.case_id = 90001
    mock_blaise_case_object.outcome_code = 0
    mock_blaise_case_object.get_contact_details_fields.return_value = {
        BlaiseFields.knock_to_nudge_contact_name: "Joe Bloggs",
        BlaiseFields.telephone_number_1: "01234567890",
        BlaiseFields.telephone_number_2: "07123123123",
    }

    # act
    mock_case_update_service._update_case_contact_information(
        mock_totalmobile_request, mock_blaise_case_object
    )

    # assert
    mock_blaise_case_object.get_contact_details_fields.assert_called_once_with(
        mock_totalmobile_request
    )


def test_lms_update_case_contact_information_logs_contact_information_has_not_been_updated(
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
    caplog,
):
    # arrange
    mock_totalmobile_request.outcome_code = 999
    mock_blaise_case_object.case_id = 90001
    mock_blaise_case_object.outcome_code = 0

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service._update_case_contact_information(
            mock_totalmobile_request, mock_blaise_case_object
        )

    # assert
    assert (
        f"Contact information has not been updated as no contact information was provided (Questionnaire=LMS2101_AA1, "
        f"Case Id=90001, Blaise hOut=0, "
        f"TM hOut=999)"
    ) in caplog.messages


def test_lms_update_case_contact_information_calls_get_knock_to_nudge_indicator_flag_field_once(
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
):
    # arrange
    mock_blaise_case_object.get_contact_details_fields.return_value = {
        BlaiseFields.knock_to_nudge_contact_name: "Joe Bloggs",
        BlaiseFields.telephone_number_1: "01234567890",
        BlaiseFields.telephone_number_2: "07123123123",
    }

    # act
    mock_case_update_service._update_case_contact_information(
        mock_totalmobile_request, mock_blaise_case_object
    )

    # assert
    mock_blaise_case_object.get_knock_to_nudge_indicator_flag_field.assert_called_once()


def test_lms_update_case_contact_information_calls_update_case_once_with_correct_parameters(
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
):
    # arrange
    mock_case_update_service._blaise_service = MagicMock()
    mock_contact_details = {
        BlaiseFields.knock_to_nudge_contact_name: "Joe Bloggs",
        BlaiseFields.telephone_number_1: "01234567890",
        BlaiseFields.telephone_number_2: "07123123123",
    }
    mock_blaise_case_object.get_contact_details_fields.return_value = (
        mock_contact_details
    )
    mock_knock_to_nudge_indicator = {BlaiseFields.knock_to_nudge_indicator: "1"}
    mock_blaise_case_object.get_knock_to_nudge_indicator_flag_field.return_value = (
        mock_knock_to_nudge_indicator
    )
    expected_fields = mock_contact_details | mock_knock_to_nudge_indicator

    # act
    mock_case_update_service._update_case_contact_information(
        mock_totalmobile_request, mock_blaise_case_object
    )

    # assert
    mock_case_update_service._blaise_service.update_case.assert_called_once_with(
        "LMS2101_AA1", "90001", expected_fields
    )


def test_lms_update_case_contact_information_logs_contact_information_updated(
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
    caplog,
):
    # arrange
    mock_totalmobile_request.outcome_code = 999
    mock_blaise_case_object.outcome_code = 0
    mock_blaise_case_object.get_contact_details_fields.return_value = {
        BlaiseFields.knock_to_nudge_contact_name: "Joe Bloggs",
        BlaiseFields.telephone_number_1: "01234567890",
        BlaiseFields.telephone_number_2: "07123123123",
    }

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service._update_case_contact_information(
            mock_totalmobile_request, mock_blaise_case_object
        )

    # assert
    assert (
        f"Contact information updated (Questionnaire=LMS2101_AA1, "
        f"Case Id=90001, Blaise hOut=0, "
        f"TM hOut=999)"
    ) in caplog.messages


def test_lms_update_case_outcome_code_calls_get_outcome_code_fields_once_with_correct_parameters(
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
):
    # act
    mock_case_update_service.update_case_outcome_code(
        mock_totalmobile_request, mock_blaise_case_object
    )

    # assert
    mock_blaise_case_object.get_outcome_code_fields.assert_called_once_with(
        mock_totalmobile_request
    )


def test_lms_update_case_outcome_code_calls_update_case_once_with_correct_parameters_without_call_history(
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
):
    # arrange
    mock_case_update_service._blaise_service = MagicMock()

    mock_outcome_fields = {
        BlaiseFields.outcome_code: "300",
        BlaiseFields.admin_outcome_code: "300",
    }
    mock_blaise_case_object.get_outcome_code_fields.return_value = mock_outcome_fields

    mock_knock_to_nudge_indicator = {BlaiseFields.knock_to_nudge_indicator: "1"}
    mock_blaise_case_object.get_knock_to_nudge_indicator_flag_field.return_value = (
        mock_knock_to_nudge_indicator
    )

    mock_call_history_record_1 = {
        f"catiMana.CatiCall.RegsCalls[1].WhoMade": "KTN",
        f"catiMana.CatiCall.RegsCalls[1].DialResult": "5",
    }
    type(mock_blaise_case_object).has_call_history = PropertyMock(return_value=False)
    mock_call_history_record_5 = {
        f"catiMana.CatiCall.RegsCalls[5].WhoMade": "KTN",
        f"catiMana.CatiCall.RegsCalls[5].DialResult": "5",
    }
    mock_blaise_case_object.get_call_history_record_field.side_effect = [
        mock_call_history_record_1,
        mock_call_history_record_5,
    ]

    expected_fields = (
        mock_outcome_fields
        | mock_knock_to_nudge_indicator
        | mock_call_history_record_1
        | mock_call_history_record_5
    )

    # act
    mock_case_update_service.update_case_outcome_code(
        mock_totalmobile_request, mock_blaise_case_object
    )

    # assert
    mock_case_update_service._blaise_service.update_case.assert_called_once_with(
        mock_totalmobile_request.questionnaire_name,
        mock_totalmobile_request.case_id,
        expected_fields,
    )


def test_lms_update_case_outcome_code_calls_update_case_once_with_correct_parameters_with_call_history(
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
):
    # arrange
    mock_case_update_service._blaise_service = MagicMock()

    mock_outcome_fields = {
        BlaiseFields.outcome_code: "300",
        BlaiseFields.admin_outcome_code: "300",
    }
    mock_blaise_case_object.get_outcome_code_fields.return_value = mock_outcome_fields

    mock_knock_to_nudge_indicator = {BlaiseFields.knock_to_nudge_indicator: "1"}
    mock_blaise_case_object.get_knock_to_nudge_indicator_flag_field.return_value = (
        mock_knock_to_nudge_indicator
    )

    mock_call_history_record_1 = {
        f"catiMana.CatiCall.RegsCalls[1].WhoMade": "KTN",
        f"catiMana.CatiCall.RegsCalls[1].DialResult": "5",
    }
    type(mock_blaise_case_object).has_call_history = PropertyMock(return_value=False)

    mock_blaise_case_object.get_call_history_record_field.return_value = (
        mock_call_history_record_1
    )

    expected_fields = (
        mock_outcome_fields | mock_knock_to_nudge_indicator | mock_call_history_record_1
    )

    # act
    mock_case_update_service.update_case_outcome_code(
        mock_totalmobile_request, mock_blaise_case_object
    )

    # assert
    mock_case_update_service._blaise_service.update_case.assert_called_once_with(
        mock_totalmobile_request.questionnaire_name,
        mock_totalmobile_request.case_id,
        expected_fields,
    )


def test_lms_update_case_outcome_logs_outcome_code_and_call_history_updated(
    mock_case_update_service,
    mock_totalmobile_request,
    mock_blaise_case_object,
    caplog,
):
    # arrange
    mock_blaise_case_object.case_id = 90001
    mock_blaise_case_object.outcome_code = 0
    mock_totalmobile_request.outcome_code = 999

    # act
    with caplog.at_level(logging.INFO):
        mock_case_update_service.update_case_outcome_code(
            mock_totalmobile_request, mock_blaise_case_object
        )

    # assert
    assert (
        f"Outcome code and call history updated (Questionnaire=LMS2101_AA1, "
        f"Case Id=90001, Blaise hOut=0, "
        f"TM hOut=999)"
    ) in caplog.messages
