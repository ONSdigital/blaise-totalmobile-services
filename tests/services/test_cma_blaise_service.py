from typing import List
from unittest import mock

import blaise_restapi
import pytest
from urllib3.exceptions import HTTPError

from app.exceptions.custom_exceptions import (CaseAllocationException)

from appconfig import Config
from services.cma_blaise_service import CMABlaiseService
from tests.helpers import config_helper


@pytest.fixture()
def config() -> Config:
    return config_helper.get_default_config()


@pytest.fixture()
def cma_blaise_service(config) -> CMABlaiseService:
    return CMABlaiseService(config=config)


# @pytest.fixture()
# def required_fields() -> List:
#     return [
#         "MainSurveyID",
#         "SurveyDisplayName",
#         "ID",
#     ]


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_for_server_park")
def test_questionnaire_exists_calls_the_rest_api_client_with_the_correct_parameters( _mock_rest_api_client, cma_blaise_service, config):
    
    # arrange
    blaise_server_park = config.blaise_server_park
    questionnaire_name = "FRS2405A"

    # act
    cma_blaise_service.questionnaire_exists(questionnaire_name)

    # assert
    _mock_rest_api_client.assert_called_with(
        blaise_server_park, questionnaire_name
    )


@mock.patch.object(blaise_restapi.Client, "get_multikey_case")
def test_case_exists_returns_the_expected_case_if_exists(_mock_rest_api_client_get_multikey_case, cma_blaise_service, config):
    
    # arrange
    questionnaire_guid = "a0e2f264-14e4-4151-b12d-bb3331674624"
    case_id = "100100"
    case = {
                "primaryKeyValues": {
                    "mainSurveyID": "a0e2f264-14e4-4151-b12d-bb3331674624",
                    "id": "100100"
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
                    "lastChangedNote.User": ""
                }
            }

    _mock_rest_api_client_get_multikey_case.return_value = case

    # act
    result = cma_blaise_service.case_exists(questionnaire_guid, case_id)

    # assert
    _mock_rest_api_client_get_multikey_case.assert_called_with(
        config.cma_server_park,
        "CMA_Launcher",
        ["MainSurveyID", "ID"],
        [questionnaire_guid, case_id]
    )
    
    assert result == case

@mock.patch.object(blaise_restapi.Client, "get_multikey_case")
def test_case_exists_returns_false_if_case_doesnot_exist(_mock_rest_api_client_get_multikey_case, cma_blaise_service, config):
    
    # arrange
    questionnaire_guid = "a0e2f264-14e4-4151-b12d-bb3331674624"
    case_id = "100100"

    _mock_rest_api_client_get_multikey_case.side_effect = ValueError("Some error occured in blaise rest API while getting multikey case!")

    # act
    result = cma_blaise_service.case_exists(questionnaire_guid, case_id)

    # assert
    _mock_rest_api_client_get_multikey_case.assert_called_once()
    _mock_rest_api_client_get_multikey_case.assert_called_with(
        config.cma_server_park,
        "CMA_Launcher",
        ["MainSurveyID", "ID"],
        [questionnaire_guid, case_id]
    )
    assert result == False

# @mock.patch.object(blaise_restapi.Client, "get_case")
# @mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
# def test_get_case_calls_the_correct_services(
#     _mock_rest_api_client1, _mock_rest_api_client2, blaise_service
# ):
#     # arrange
#     blaise_server_park = "gusty"
#     questionnaire_name = "LMS2101_AA1"
#     case_id = "10010"

#     _mock_rest_api_client1.return_value = True

#     _mock_rest_api_client2.return_value = {
#         "caseId": "10010",
#         "fieldData": {
#             BlaiseFields.case_id: "10010",
#             BlaiseFields.outcome_code: "110",
#             BlaiseFields.wave_com_dte: "31-01-2023",
#         },
#     }

#     # act
#     blaise_service.get_case(questionnaire_name, case_id)

#     # assert
#     _mock_rest_api_client1.assert_called_with(
#         blaise_server_park, questionnaire_name, case_id
#     )


# @mock.patch.object(blaise_restapi.Client, "get_case")
# @mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
# def test_get_case_returns_the_expected_case_data(
#     _mock_rest_api_client1, _mock_rest_api_client2, blaise_service
# ):
#     # arrange
#     questionnaire_name = "LMS2101_AA1"
#     case_id = "10010"

#     _mock_rest_api_client1.return_value = True

#     case_data = {
#         "caseId": "2000000001",
#         "fieldData": {
#             BlaiseFields.case_id: "10010",
#             BlaiseFields.outcome_code: "110",
#             BlaiseFields.wave_com_dte: "31-01-2023",
#         },
#     }
#     _mock_rest_api_client2.return_value = case_data

#     # act
#     result = blaise_service.get_case(questionnaire_name, case_id)

#     # assert
#     assert result == case_data["fieldData"]


# @mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
# def test_get_case_throws_a_case_does_not_exist_error_if_the_case_does_not_exist(
#     _mock_rest_api_client, blaise_service
# ):
#     # arrange
#     _mock_rest_api_client.return_value = False

#     questionnaire_name = "LMS2101_AA1"
#     case_id = "9001"

#     # assert
#     with pytest.raises(QuestionnaireCaseDoesNotExistError):
#         blaise_service.get_case(questionnaire_name, case_id)


# @mock.patch.object(blaise_restapi.Client, "get_case")
# @mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
# def test_get_case_throws_a_case_error_if_a_httperror_is_thrown(
#     _mock_rest_api_client1, _mock_rest_api_client2, blaise_service
# ):
#     # arrange
#     _mock_rest_api_client1.return_value = True

#     _mock_rest_api_client2.side_effect = HTTPError

#     questionnaire_name = "LMS2101_AA1"
#     case_id = "9001"

#     # assert
#     with pytest.raises(QuestionnaireCaseError):
#         blaise_service.get_case(questionnaire_name, case_id)


# @mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
# def test_case_exists_calls_the_rest_api_client_with_the_correct_parameters(
#     _mock_rest_api_client, blaise_service
# ):
#     # arrange
#     blaise_server_park = "gusty"
#     questionnaire_name = "LMS2101_AA1"
#     case_id = "10010"

#     # act
#     blaise_service.case_exists(questionnaire_name, case_id)

#     # assert
#     _mock_rest_api_client.assert_called_with(
#         blaise_server_park, questionnaire_name, case_id
#     )


# @pytest.mark.parametrize(
#     "api_response, expected_response", [(False, False), (True, True)]
# )
# @mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
# def test_case_exists_returns_correct_response(
#     _mock_rest_api_client, api_response, expected_response, blaise_service
# ):
#     # arrange
#     questionnaire_name = "LMS2101_AA1"
#     case_id = "10010"
#     _mock_rest_api_client.return_value = api_response

#     # act
#     result = blaise_service.case_exists(questionnaire_name, case_id)

#     # assert
#     assert result == expected_response


# @mock.patch.object(blaise_restapi.Client, "questionnaire_exists_on_server_park")
# def test_questionnaire_exists_calls_the_rest_api_client_with_the_correct_parameters(
#     _mock_rest_api_client, blaise_service
# ):
#     # arrange
#     blaise_server_park = "gusty"
#     questionnaire_name = "LMS2101_AA1"

#     # act
#     blaise_service.questionnaire_exists(questionnaire_name)

#     # assert
#     _mock_rest_api_client.assert_called_with(blaise_server_park, questionnaire_name)


# @pytest.mark.parametrize(
#     "api_response, expected_response", [(False, False), (True, True)]
# )
# @mock.patch.object(blaise_restapi.Client, "questionnaire_exists_on_server_park")
# def test_questionnaire_exists_returns_correct_response(
#     _mock_rest_api_client, api_response, expected_response, blaise_service
# ):
#     # arrange
#     questionnaire_name = "LMS2101_AA1"
#     _mock_rest_api_client.return_value = api_response

#     # act
#     result = blaise_service.questionnaire_exists(questionnaire_name)

#     # assert
#     assert result == expected_response


# @mock.patch.object(blaise_restapi.Client, "patch_case_data")
# def test_update_case_calls_the_rest_api_client_with_the_correct_parameters(
#     _mock_rest_api_client, blaise_service
# ):
#     # arrange
#     blaise_server_park = "gusty"
#     questionnaire_name = "LMS2101_AA1"
#     case_id = "900001"
#     data_fields = [
#         {BlaiseFields.outcome_code: "110"},
#         {BlaiseFields.knock_to_nudge_contact_name: "John Smith"},
#         {BlaiseFields.telephone_number_1: "01234 567890"},
#         {BlaiseFields.telephone_number_2: "07734 567890"},
#     ]

#     # act
#     blaise_service.update_case(questionnaire_name, case_id, data_fields)

#     # assert
#     _mock_rest_api_client.assert_called_with(
#         blaise_server_park, questionnaire_name, case_id, data_fields
#     )
