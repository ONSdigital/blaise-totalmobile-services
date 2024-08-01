from datetime import datetime
from typing import List
from unittest import mock

import blaise_restapi
import pytest
from urllib3.exceptions import HTTPError

from app.exceptions.custom_exceptions import (
    QuestionnaireCaseDoesNotExistError,
    QuestionnaireCaseError,
)
from appconfig import Config
from models.blaise.blaise_lms_case_information_model import BlaiseLMSCaseInformationModel
from services.blaise_service import RealBlaiseService
from tests.helpers import config_helper


@pytest.fixture()
def config() -> Config:
    return config_helper.get_default_config()


@pytest.fixture()
def blaise_service(config) -> RealBlaiseService:
    return RealBlaiseService(config=config)


@pytest.fixture()
def required_fields() -> List:
    return [
            "qiD.Serial_Number",
            "dataModelName",
            "qDataBag.TLA",
        ]


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_cases_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client, blaise_service, required_fields
):
    # arrange
    blaise_server_park = "gusty"
    questionnaire_name = "DST2106Z"

    # act
    blaise_service.get_cases(questionnaire_name, required_fields)

    # assert
    _mock_rest_api_client.assert_called_with(
        blaise_server_park, questionnaire_name, required_fields
    )


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_cases_returns_the_expected_case_data(
    _mock_rest_api_client_get_questionnaire, blaise_service, required_fields
):
    # arrange
    questionnaire_case_data = {
        "questionnaireName": "LMS2101_AA1",
        "questionnaireId": "12345-12345-12345-12345-12345",
        "reportingData": [
            {"qiD.Serial_Number": "10010","hOut": "110","qDataBag.WaveComDTE": "31-01-2023",},
            {"qiD.Serial_Number": "10020", "hOut": "210", "qDataBag.WaveComDTE": ""},
            {"qiD.Serial_Number": "10030", "hOut": "310", "qDataBag.WaveComDTE": ""},
            {"qiD.Serial_Number": "10040", "hOut": "310", "qDataBag.WaveComDTE": ""},
        ],
    }

    _mock_rest_api_client_get_questionnaire.return_value = questionnaire_case_data

    questionnaire_name = "LMS2101_AA1"

    # act
    result = blaise_service.get_cases(questionnaire_name, required_fields)

    # assert
    assert result == questionnaire_case_data["reportingData"]


@mock.patch.object(blaise_restapi.Client, "get_case")
@mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
def test_get_case_calls_the_correct_services(
    _mock_rest_api_client1, _mock_rest_api_client2, blaise_service
):
    # arrange
    blaise_server_park = "gusty"
    questionnaire_name = "LMS2101_AA1"
    case_id = "10010"

    _mock_rest_api_client1.return_value = True

    _mock_rest_api_client2.return_value = {
        "caseId": "10010",
        "fieldData": {
            "qiD.Serial_Number": "10010",
            "hOut": "110",
            "qDataBag.WaveComDTE": "31-01-2023",
        },
    }

    # act
    blaise_service.get_case(questionnaire_name, case_id)

    # assert
    _mock_rest_api_client1.assert_called_with(
        blaise_server_park, questionnaire_name, case_id
    )


@mock.patch.object(blaise_restapi.Client, "get_case")
@mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
def test_get_case_returns_the_expected_case_data(
    _mock_rest_api_client1, _mock_rest_api_client2, blaise_service
):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "10010"

    _mock_rest_api_client1.return_value = True

    case_data = {
        "caseId": "2000000001",
        "fieldData": {
            "qiD.Serial_Number": "10010",
            "hOut": "110",
            "qDataBag.WaveComDTE": "31-01-2023",
        },
    }
    _mock_rest_api_client2.return_value = case_data

    # act
    result = blaise_service.get_case(questionnaire_name, case_id)

    # assert
    assert result == case_data["fieldData"]


@mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
def test_get_case_throws_a_case_does_not_exist_error_if_the_case_does_not_exist(
    _mock_rest_api_client, blaise_service
):
    # arrange
    _mock_rest_api_client.return_value = False

    questionnaire_name = "LMS2101_AA1"
    case_id = "9001"

    # assert
    with pytest.raises(QuestionnaireCaseDoesNotExistError):
        blaise_service.get_case(questionnaire_name, case_id)


@mock.patch.object(blaise_restapi.Client, "get_case")
@mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
def test_get_case_throws_a_case_error_if_a_httperror_is_thrown(
    _mock_rest_api_client1, _mock_rest_api_client2, blaise_service
):
    # arrange
    _mock_rest_api_client1.return_value = True

    _mock_rest_api_client2.side_effect = HTTPError

    questionnaire_name = "LMS2101_AA1"
    case_id = "9001"

    # assert
    with pytest.raises(QuestionnaireCaseError):
        blaise_service.get_case(questionnaire_name, case_id)


@mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
def test_case_exists_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client, blaise_service
):
    # arrange
    blaise_server_park = "gusty"
    questionnaire_name = "LMS2101_AA1"
    case_id = "10010"

    # act
    blaise_service.case_exists(questionnaire_name, case_id)

    # assert
    _mock_rest_api_client.assert_called_with(
        blaise_server_park, questionnaire_name, case_id
    )


@pytest.mark.parametrize(
    "api_response, expected_response", [(False, False), (True, True)]
)
@mock.patch.object(blaise_restapi.Client, "case_exists_for_questionnaire")
def test_case_exists_returns_correct_response(
    _mock_rest_api_client, api_response, expected_response, blaise_service
):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "10010"
    _mock_rest_api_client.return_value = api_response

    # act
    result = blaise_service.case_exists(questionnaire_name, case_id)

    # assert
    assert result == expected_response


@mock.patch.object(blaise_restapi.Client, "questionnaire_exists_on_server_park")
def test_questionnaire_exists_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client, blaise_service
):
    # arrange
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
    # arrange
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
    # arrange
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
