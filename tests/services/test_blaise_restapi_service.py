import blaise_restapi

from services import blaise_restapi_service
from unittest import mock
from tests.helpers import config_helper


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_cases_calls_the_rest_api_client_with_the_correct_parameters(_mock_rest_api_client):
    config = config_helper.get_default_config()
    blaise_server_park = "gusty"
    questionnaire_name = "DST2106Z"
    fields = blaise_restapi_service.required_fields_from_blaise

    # act
    blaise_restapi_service.get_cases(questionnaire_name, config)

    # assert
    _mock_rest_api_client.assert_called_with(blaise_server_park, questionnaire_name, fields)


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_cases_returns_a_list_of_case_models(
        _mock_rest_api_client,
):
    # arrange
    config = config_helper.get_default_config()
    _mock_rest_api_client.return_value = {
        "questionnaireName": "DST2106Z",
        "questionnaireId": "12345-12345-12345-12345-12345",
        "reportingData": [
            {"qiD.Serial_Number": "10010", "hOut": "110"},
            {"qiD.Serial_Number": "10020", "hOut": "210"},
            {"qiD.Serial_Number": "10030", "hOut": "310"},
        ],
    }
    questionnaire_name = "OPN2101A"

    # act
    result = blaise_restapi_service.get_cases(questionnaire_name, config)

    # assert
    assert len(result) == 3

    assert result[0].case_id == "10010"
    assert result[0].outcome_code == "110"

    assert result[1].case_id == "10020"
    assert result[1].outcome_code == "210"

    assert result[2].case_id == "10030"
    assert result[2].outcome_code == "310"