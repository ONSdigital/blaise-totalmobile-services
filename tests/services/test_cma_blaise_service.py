import logging
from typing import List
from unittest import mock

import blaise_restapi
import pytest

from app.exceptions.custom_exceptions import CaseAllocationException
from appconfig import Config
from models.create.cma.blaise_cma_frs_create_case_model import FRSCaseModel
from services.cma_blaise_service import CMABlaiseService
from tests.helpers import config_helper


@pytest.fixture()
def config() -> Config:
    return config_helper.get_default_config()


@pytest.fixture()
def cma_blaise_service(config) -> CMABlaiseService:
    return CMABlaiseService(config=config)


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_for_server_park")
def test_questionnaire_exists_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client, cma_blaise_service, config
):

    # arrange
    blaise_server_park = config.blaise_server_park
    questionnaire_name = "FRS2405A"

    # act
    cma_blaise_service.questionnaire_exists(questionnaire_name)

    # assert
    _mock_rest_api_client.assert_called_with(blaise_server_park, questionnaire_name)


@mock.patch.object(blaise_restapi.Client, "get_multikey_case")
def test_case_exists_returns_the_expected_case_if_exists(
    _mock_rest_api_client, cma_blaise_service, config
):

    # arrange
    questionnaire_guid = "a0e2f264-14e4-4151-b12d-bb3331674624"
    case_id = "100100"
    case = {
        "primaryKeyValues": {
            "mainSurveyID": "a0e2f264-14e4-4151-b12d-bb3331674624",
            "id": "100100",
        },
        "fieldData": {
            "mainSurveyID": "a0e2f264-14e4-4151-b12d-bb3331674624",
            "surveyDisplayName": "FRS2405A",
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
            "cmA_EndDate": "11-11-2024",
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

    _mock_rest_api_client.return_value = case

    # act
    result = cma_blaise_service.case_exists(questionnaire_guid, case_id)

    # assert
    _mock_rest_api_client.assert_called_with(
        config.cma_server_park,
        "CMA_Launcher",
        ["MainSurveyID", "ID"],
        [questionnaire_guid, case_id],
    )

    assert result == case


@mock.patch.object(blaise_restapi.Client, "get_multikey_case")
def test_case_exists_returns_false_if_case_doesnot_exist(
    _mock_rest_api_client, cma_blaise_service, config
):

    # arrange
    questionnaire_guid = "a0e2f264-14e4-4151-b12d-bb3331674624"
    case_id = "100100"

    _mock_rest_api_client.side_effect = ValueError(
        "Some error occured in blaise rest API while getting multikey case!"
    )

    # act
    result = cma_blaise_service.case_exists(questionnaire_guid, case_id)

    # assert
    _mock_rest_api_client.assert_called_once()
    _mock_rest_api_client.assert_called_with(
        config.cma_server_park,
        "CMA_Launcher",
        ["MainSurveyID", "ID"],
        [questionnaire_guid, case_id],
    )
    assert result == False


@mock.patch.object(blaise_restapi.Client, "create_multikey_case")
def test_create_frs_case_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client, cma_blaise_service, config
):
    # arrange
    frs_case_model = FRSCaseModel(
        user="Interviewer1",
        questionnaire_name="FRS2405A",
        guid="a0e2f264-14e4-4151-b12d-bb3331674624",
        case_id="100100",
        custom_use="",
        location="",
        inPosession="",
    )
    # act
    cma_blaise_service.create_frs_case(frs_case_model)

    # assert
    _mock_rest_api_client.assert_called_with(
        config.cma_server_park,
        "CMA_Launcher",
        frs_case_model.key_names,
        frs_case_model.key_values,
        frs_case_model.data_fields,
    )


@mock.patch.object(blaise_restapi.Client, "create_multikey_case")
def test_create_frs_case_raises_exception_if_rest_api_fails_creating_case(
    _mock_rest_api_client, cma_blaise_service, caplog
):
    # arrange
    frs_case_model = FRSCaseModel(
        user="Interviewer1",
        questionnaire_name="FRS2405A",
        guid="a0e2f264-14e4-4151-b12d-bb3331674624",
        case_id="100100",
        custom_use="",
        location="",
        inPosession="",
    )
    _mock_rest_api_client.side_effect = ValueError(
        "Some error occured in blaise rest API while creating multikey case!"
    )

    # act
    with caplog.at_level(logging.ERROR) and pytest.raises(CaseAllocationException):
        cma_blaise_service.create_frs_case(frs_case_model)

    # assert
    assert (
        "root",
        logging.ERROR,
        f"Could not create a case for User Interviewer1 "
        f"within Questionnaire FRS2405A with case_id 100100 in CMA_Launcher...",
    ) in caplog.record_tuples


@mock.patch.object(blaise_restapi.Client, "patch_multikey_case_data")
def test_update_frs_case_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client, cma_blaise_service, config
):

    # arrange
    frs_case_model = FRSCaseModel(
        user="Interviewer2",
        questionnaire_name="FRS2405A",
        guid="a0e2f264-14e4-4151-b12d-bb3331674624",
        case_id="100100",
        custom_use="",
        location="",
        inPosession="",
    )
    # act
    cma_blaise_service.update_frs_case(frs_case_model)

    # assert
    _mock_rest_api_client.assert_called_with(
        config.cma_server_park,
        "CMA_Launcher",
        frs_case_model.key_names,
        frs_case_model.key_values,
        frs_case_model.data_fields,
    )


@mock.patch.object(blaise_restapi.Client, "patch_multikey_case_data")
def test_update_frs_case_raises_exception_if_rest_api_fails_updating_case(
    _mock_rest_api_client, cma_blaise_service, caplog
):
    # arrange
    frs_case_model = FRSCaseModel(
        user="Interviewer2",
        questionnaire_name="FRS2405A",
        guid="a0e2f264-14e4-4151-b12d-bb3331674624",
        case_id="100100",
        custom_use="",
        location="",
        inPosession="",
    )
    _mock_rest_api_client.side_effect = ValueError(
        "Some error occured in blaise rest API while updating multikey case!"
    )

    # act
    with pytest.raises(CaseAllocationException):
        cma_blaise_service.update_frs_case(frs_case_model)

    # assert
    assert (
        "root",
        logging.ERROR,
        f"Reallocation failed. Failed in allocating Case {frs_case_model.case_id} to User: {frs_case_model.user}",
    ) in caplog.record_tuples
