from datetime import datetime
from unittest import mock

import blaise_restapi
import pytest
from urllib3.exceptions import HTTPError

from app.exceptions.custom_exceptions import QuestionnaireCaseDoesNotExistError
from appconfig import Config
from services.blaise_service import BlaiseService
from tests.helpers import config_helper


@pytest.fixture()
def config() -> Config:
    return config_helper.get_default_config()


@pytest.fixture()
def blaise_service(config) -> BlaiseService:
    return BlaiseService(config)


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_cases_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client, blaise_service
):
    blaise_server_park = "gusty"
    questionnaire_name = "DST2106Z"
    fields = blaise_service.required_fields_from_blaise

    # act
    blaise_service.get_cases(questionnaire_name)

    # assert
    _mock_rest_api_client.assert_called_with(
        blaise_server_park, questionnaire_name, fields
    )


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_cases_returns_a_list_of_case_models(
    _mock_rest_api_client_get_questionnaire, blaise_service
):
    # arrange
    _mock_rest_api_client_get_questionnaire.return_value = {
        "questionnaireName": "LMS2101_AA1",
        "questionnaireId": "12345-12345-12345-12345-12345",
        "reportingData": [
            {
                "qiD.Serial_Number": "10010",
                "hOut": "110",
                "qDataBag.WaveComDTE": "31-01-2023",
            },
            {"qiD.Serial_Number": "10020", "hOut": "210", "qDataBag.WaveComDTE": ""},
            {"qiD.Serial_Number": "10030", "hOut": "310", "qDataBag.WaveComDTE": ""},
        ],
    }
    questionnaire_name = "LMS2101_AA1"

    # act
    result = blaise_service.get_cases(questionnaire_name)

    # assert
    assert len(result) == 3

    assert result[0].case_id == "10010"
    assert result[0].outcome_code == 110
    assert result[0].wave_com_dte == datetime(2023, 1, 31)

    assert result[1].case_id == "10020"
    assert result[1].outcome_code == 210
    assert result[1].wave_com_dte is None

    assert result[2].case_id == "10030"
    assert result[2].outcome_code == 310
    assert result[2].wave_com_dte is None


@mock.patch.object(blaise_restapi.Client, "get_case")
def test_get_case_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client, blaise_service
):
    blaise_server_park = "gusty"
    questionnaire_name = "LMS2101_AA1"
    case_id = "9001"

    _mock_rest_api_client.return_value = {
        "caseId": "2000000001",
        "fieldData": {
            "qiD.Serial_Number": "10010",
            "hOut": "110",
            "qDataBag.WaveComDTE": "31-01-2023",
        },
    }

    # act
    blaise_service.get_case(questionnaire_name, case_id)

    # assert
    _mock_rest_api_client.assert_called_with(
        blaise_server_park, questionnaire_name, case_id
    )


@mock.patch.object(blaise_restapi.Client, "get_case")
def test_get_case_returns_a_case_model(_mock_rest_api_client, blaise_service):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "9001"
    _mock_rest_api_client.return_value = {
        "caseId": "2000000001",
        "fieldData": {
            "qiD.Serial_Number": "10010",
            "hOut": "110",
            "qDataBag.WaveComDTE": "31-01-2023",
        },
    }

    # act
    result = blaise_service.get_case(questionnaire_name, case_id)

    # assert
    assert result.case_id == "10010"
    assert result.outcome_code == 110


@mock.patch.object(blaise_restapi.Client, "get_case")
def test_get_case_throws_a_case_does_not_exist_error_if_the_case_does_not_exist(
    _mock_rest_api_client, blaise_service
):
    # arrange
    _mock_rest_api_client.side_effect = HTTPError()

    questionnaire_name = "LMS2101_AA1"
    case_id = "9001"

    # assert
    with pytest.raises(QuestionnaireCaseDoesNotExistError):
        blaise_service.get_case(questionnaire_name, case_id)


@mock.patch.object(blaise_restapi.Client, "questionnaire_exists_on_server_park")
def test_questionnaire_exists_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client, blaise_service
):
    blaise_server_park = "gusty"
    questionnaire_name = "LMS2101_AA1"

    # act
    blaise_service.questionnaire_exists(questionnaire_name)

    # assert
    _mock_rest_api_client.assert_called_with(blaise_server_park, questionnaire_name)


@pytest.mark.parametrize(
    "api_response, expected_response", [(False, False), (True, True)]
)
@mock.patch.object(blaise_restapi.Client, "questionnaire_exists_on_server_park")
def test_questionnaire_exists_returns_correct_response(
    _mock_rest_api_client, api_response, expected_response, blaise_service
):
    questionnaire_name = "LMS2101_AA1"
    _mock_rest_api_client.return_value = api_response

    # act
    result = blaise_service.questionnaire_exists(questionnaire_name)

    # assert
    assert result == expected_response


@mock.patch.object(blaise_restapi.Client, "patch_case_data")
def test_update_case_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client, blaise_service
):
    blaise_server_park = "gusty"
    questionnaire_name = "LMS2101_AA1"
    case_id = "900001"
    data_fields = [
        {"hOut": "110"},
        {"dMktnName": "John Smith"},
        {"qDataBag.TelNo": "01234 567890"},
        {"qDataBag.TelNo2": "07734 567890"},
    ]

    # act
    blaise_service.update_case(questionnaire_name, case_id, data_fields)

    # assert
    _mock_rest_api_client.assert_called_with(
        blaise_server_park, questionnaire_name, case_id, data_fields
    )


@mock.patch.object(blaise_restapi.Client, "get_case_status")
def test_get_cases_status_returns_a_list_dictionary_of_stuff_and_or_things(
        _mock_rest_api_client_get_case_status, blaise_service
):
    # arrange
    case_status_list = [
        {
            "primaryKey": "12345",
            "outcome": 110
        },
        {
            "primaryKey": "67890",
            "outcome": 310
        }
    ]
    _mock_rest_api_client_get_case_status.return_value = case_status_list

    questionnaire_name = "LMS2101_AA1"

    # act
    result = blaise_service.get_case_status_information(questionnaire_name)

    # assert
    assert result == case_status_list


@mock.patch.object(blaise_restapi.Client, "get_case_status")
def test_get_case_status_information_calls_the_rest_api_client_with_the_correct_parameters(
        _mock_rest_api_client, blaise_service
):
    blaise_server_park = "gusty"
    questionnaire_name = "LMS2101_AA1"

    _mock_rest_api_client.return_value = []

    # act
    blaise_service.get_case_status_information(questionnaire_name)

    # assert
    _mock_rest_api_client.assert_called_with(
        blaise_server_park, questionnaire_name
    )
