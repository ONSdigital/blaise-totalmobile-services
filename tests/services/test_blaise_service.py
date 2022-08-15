import blaise_restapi
import pytest

from urllib3.exceptions import HTTPError
from services import blaise_service
from unittest import mock

from services.blaise_service import QuestionnaireCaseDoesNotExistError
from tests.helpers import config_helper


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_cases_calls_the_rest_api_client_with_the_correct_parameters(_mock_rest_api_client):
    config = config_helper.get_default_config()
    blaise_server_park = "gusty"
    questionnaire_name = "DST2106Z"
    fields = blaise_service.required_fields_from_blaise

    # act
    blaise_service.get_cases(questionnaire_name, config)

    # assert
    _mock_rest_api_client.assert_called_with(blaise_server_park, questionnaire_name, fields)


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_cases_returns_a_list_of_case_models(_mock_rest_api_client):
    # arrange
    config = config_helper.get_default_config()
    _mock_rest_api_client.return_value = {
        "questionnaireName": "LMS2101_AA1",
        "questionnaireId": "12345-12345-12345-12345-12345",
        "reportingData": [
            {"qiD.Serial_Number": "10010", "hOut": "110"},
            {"qiD.Serial_Number": "10020", "hOut": "210"},
            {"qiD.Serial_Number": "10030", "hOut": "310"},
        ],
    }
    questionnaire_name = "LMS2101_AA1"

    # act
    result = blaise_service.get_cases(questionnaire_name, config)

    # assert
    assert len(result) == 3

    assert result[0].case_id == "10010"
    assert result[0].outcome_code == "110"

    assert result[1].case_id == "10020"
    assert result[1].outcome_code == "210"

    assert result[2].case_id == "10030"
    assert result[2].outcome_code == "310"


@mock.patch.object(blaise_restapi.Client, "get_case")
def test_get_case_calls_the_rest_api_client_with_the_correct_parameters(_mock_rest_api_client):
    config = config_helper.get_default_config()
    blaise_server_park = "gusty"
    questionnaire_name = "LMS2101_AA1"
    case_id = "9001"

    # act
    blaise_service.get_case(questionnaire_name, case_id, config)

    # assert
    _mock_rest_api_client.assert_called_with(blaise_server_park, questionnaire_name, case_id)


@mock.patch.object(blaise_restapi.Client, "get_case")
def test_get_case_returns_a_case_model(_mock_rest_api_client):
    # arrange
    config = config_helper.get_default_config()
    questionnaire_name = "LMS2101_AA1"
    case_id = "9001"
    _mock_rest_api_client.return_value = {
      "caseId": "2000000001",
      "fieldData": {
          "qiD.Serial_Number": "10010", "hOut": "110"
        }
    }

    # act
    result = blaise_service.get_case(questionnaire_name, case_id, config)

    # assert
    assert result.case_id == "10010"
    assert result.outcome_code == "110"


@mock.patch.object(blaise_restapi.Client, "get_case")
def test_get_case_throws_a_case_does_not_exist_error_if_the_case_does_not_exist(_mock_rest_api_client):
    # arrange
    config = config_helper.get_default_config()
    _mock_rest_api_client.side_effect = HTTPError()

    questionnaire_name = "LMS2101_AA1"
    case_id = "9001"

    # assert
    with pytest.raises(QuestionnaireCaseDoesNotExistError):
        blaise_service.get_case(questionnaire_name, case_id, config)


@mock.patch.object(blaise_restapi.Client, "questionnaire_exists_on_server_park")
def test_questionnaire_exists_calls_the_rest_api_client_with_the_correct_parameters(_mock_rest_api_client):
    config = config_helper.get_default_config()
    blaise_server_park = "gusty"
    questionnaire_name = "LMS2101_AA1"

    # act
    blaise_service.questionnaire_exists(questionnaire_name, config)

    # assert
    _mock_rest_api_client.assert_called_with(blaise_server_park, questionnaire_name)


@pytest.mark.parametrize("api_response, expected_response", [(False, False), (True, True)])
@mock.patch.object(blaise_restapi.Client, "questionnaire_exists_on_server_park")
def test_questionnaire_exists_returns_correct_response(_mock_rest_api_client, api_response, expected_response):
    config = config_helper.get_default_config()
    questionnaire_name = "LMS2101_AA1"
    _mock_rest_api_client.return_value = api_response

    # act
    result = blaise_service.questionnaire_exists(questionnaire_name, config)

    # assert
    assert result == expected_response
