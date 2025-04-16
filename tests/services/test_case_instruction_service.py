import logging
from unittest.mock import MagicMock

import pytest
from requests import JSONDecodeError

from services.delete.delete_cma_case_service import DeleteCMACaseService
from services.case_instruction_service import CaseInstructionService


from app.exceptions.custom_exceptions import SpecialInstructionCreationFailedException


@pytest.fixture()
def mock_cma_blaise_service():
    return MagicMock()


@pytest.fixture()
def case_instruction_service(mock_cma_blaise_service):
    return CaseInstructionService(
        mock_cma_blaise_service
    )


@pytest.fixture()
def mock_case_instruction_service():
    return MagicMock()


@pytest.fixture()
def delete_service(mock_cma_blaise_service, mock_case_instruction_service):
    return DeleteCMACaseService(
        mock_cma_blaise_service, mock_case_instruction_service
    )


@pytest.fixture()
def totalmobile_request():
    totalmobile_request = MagicMock()
    totalmobile_request.questionnaire_name = "FRS2504A"
    totalmobile_request.case_id = 1234
    totalmobile_request.outcome_code = 410
    return totalmobile_request


@pytest.fixture()
def cma_case():
    return {
        "primaryKeyValues": {
            "mainSurveyID": "8d02c802-962d-431a-9e8b-715839442480",
            "id": "100100",
        },
        "fieldData": {
            "mainSurveyID": "8d02c802-962d-431a-9e8b-715839442480",
            "surveyDisplayName": "FRS2504A",
            "id": "100100",
            "cmA_Supervisor": "",
            "cmA_ForWhom": "",
            "cmA_InPossession": "",
            "cmA_Location": "SERVER",
            "cmA_Status": "",
            "cmA_CaseClosed": "",
            "cmA_HappeningsStr": "",
            "cmA_HappeningsLbl": "",
            "cmA_HappeningsCod": "",
            "cmA_AllowSpawning": "",
            "cmA_IsDonorCase": "",
            "cmA_GroupType": "",
            "cmA_GroupID": "",
            "cmA_GroupSort": "",
            "cmA_GroupStatus": "",
            "cmA_GroupSummary": "",
            "cmA_SpawnCount": "",
            "cmA_StartDate": "",
            "cmA_EndDate": "31-03-2024",
            "cmA_CmdLineForEdit": "",
            "cmA_PreLoadForEdit": "",
            "cmA_Process.CreatedDT": "",
            "cmA_Process.LastChangedDT": "",
            "cmA_Process.GeoLocation": "",
            "cmA_Process.FirstDownloaded.When": "",
            "cmA_Process.FirstDownloaded.User": "",
            "cmA_Process.FirstUploaded.When": "",
            "cmA_Process.FirstUploaded.User": "",
            "cmA_Process.LastDownloaded.When": "",
            "cmA_Process.LastDownloaded.User": "",
            "cmA_Process.LastUploaded.When": "",
            "cmA_Process.LastUploaded.User": "",
            "cmA_Process.LastAttempt.When": "",
            "cmA_Process.LastAttempt.User": "",
            "cmA_Process.FirstInterviewTime.When": "",
            "cmA_Process.FirstInterviewTime.User": "",
            "cmA_Process.LastInterviewTime.When": "",
            "cmA_Process.LastInterviewTime.User": "",
            "cmA_Process.LastInterviewEndTime": "",
            "cmA_Process.TotalInterviewTimeUsed": "",
            "cmA_Appointment.AppDate": "",
            "cmA_Appointment.AppTime": "",
            "cmA_Appointment.WhenMade.When": "",
            "cmA_Appointment.WhenMade.User": "",
            "cmA_TimeZone": "",
            "cmA_Data.SurveyUploadFailed": "",
            "cmA_Data.Survey": "",
            "cmA_Data.AttemptsCount": "",
            "cmA_Data.Attempts": "",
            "cmA_AttemptsRoute": "",
            "cmA_AttemptsGUID": "",
            "cmA_ContactImage": "",
            "cmA_GeoLocation": "",
            "cmA_ContactInfoGUID": "",
            "cmA_ContactData": "",
            "cmA_DetailsTemplate": "",
            "cmA_CustomUse": "",
            "contactInfoShort": "",
            "lastChangedCI.When": "",
            "lastChangedCI.User": "",
            "caseNote": "",
            "lastChangedNote.When": "",
            "lastChangedNote.User": "",
        },
    }


@pytest.fixture()
def questionnaire_object():
    return {
        "name": "FRS2504A",
        "id": "8d02c802-962d-431a-9e8b-715839442480",
        "serverParkName": "gusty",
        "installDate": "2025-02-27T11:47:28.1314856+00:00",
        "status": "Active",
        "dataRecordCount": 0,
        "hasData": False,
        "blaiseVersion": "5.14.6.3686",
        "fieldPeriod": "2025-02-01T00:00:00",
        "surveyTla": "FRS",
        "nodes": [{"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Active"}],
    }


def test_remove_case_from_cma_does_not_remove_case_from_cma_when_outcome_code_is_not_in_remove_from_cma_set_and_logs_information(
    delete_service, totalmobile_request, mock_case_instruction_service, caplog
):
    # arrange
    totalmobile_request.outcome_code = 310

    # act
    with caplog.at_level(logging.INFO):
        delete_service.remove_case_from_cma(totalmobile_request)

    # assert
    assert (
        "Totalmobile case has an outcome code of 310 and should not to be removed from CMA."
    ) in caplog.messages
    mock_case_instruction_service.create_new_entry_for_special_instructions.assert_not_called()


def test_remove_case_from_cma_calls_create_new_entry_for_special_instructions_when_outcome_code_is_in_remove_from_cma_set(
    delete_service,
    totalmobile_request,
    mock_case_instruction_service,
    mock_cma_blaise_service,
    cma_case,
    questionnaire_object,
):
    # arrange
    mock_cma_blaise_service.questionnaire_exists.return_value = questionnaire_object
    mock_cma_blaise_service.case_exists.return_value = cma_case

    # act
    delete_service.remove_case_from_cma(totalmobile_request)

    # assert
    mock_case_instruction_service.create_new_entry_for_special_instructions.assert_called_once_with(
        cma_case, totalmobile_request.questionnaire_name
    )


def test_create_new_entry_for_special_instructions_is_run_successfully(
    case_instruction_service,
    mock_cma_blaise_service,
    cma_case,
    questionnaire_object,
    caplog
):
    # arrange
    mock_cma_blaise_service.questionnaire_exists.return_value = questionnaire_object
    mock_cma_blaise_service.case_exists.return_value = cma_case
    questionnaire_name = "FRS2405A"
    unique_case_id = 100100

    # act
    with caplog.at_level(logging.INFO):
        case_instruction_service.create_new_entry_for_special_instructions(cma_case, questionnaire_name)

    # assert
    mock_cma_blaise_service.create_frs_case.assert_called_once()
    assert (
        f"Special Instructions entry created for Case {unique_case_id} for Questionnaire {questionnaire_name}"
    ) in caplog.messages

def test_create_new_entry_for_special_instructions_throws_exception(
    case_instruction_service,
    mock_cma_blaise_service,
    cma_case,
    questionnaire_object,
    caplog
):
    # arrange
    mock_cma_blaise_service.questionnaire_exists.return_value = questionnaire_object
    mock_cma_blaise_service.case_exists.return_value = cma_case
    mock_cma_blaise_service.create_frs_case.side_effect = Exception("Boom!")
    questionnaire_name = "FRS2405A"
    unique_case_id = 100100

    # act
    with pytest.raises(SpecialInstructionCreationFailedException):
        case_instruction_service.create_new_entry_for_special_instructions(cma_case, questionnaire_name)

    # assert
    mock_cma_blaise_service.create_frs_case.assert_called_once()
    assert (
        f"Special Instructions entry creation for Case {unique_case_id} for Questionnaire {questionnaire_name} failed"
    ) in caplog.messages