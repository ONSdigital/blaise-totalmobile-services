from client import bus
from unittest import mock
from services.uac_restapi_service import get_questionnaire_uacs
from tests.helpers import config_helper


@mock.patch.object(bus.BusClient, "get_uacs_by_case_id")
def test_get_questionnaire_uacs_calls_the_rest_api_client_with_the_correct_parameters(_mock_rest_api_client):
    # arrange
    config = config_helper.get_default_config()
    questionnaire_name = "DST2106Z"

    # act
    get_questionnaire_uacs(questionnaire_name, config)

    # assert
    _mock_rest_api_client.assert_called_with(questionnaire_name)


@mock.patch.object(bus.BusClient, "get_uacs_by_case_id")
def test_get_questionnaire_uacs_returns_the_case_data_supplied_by_the_rest_api_client(_mock_rest_api_client):
    # arrange
    config = config_helper.get_default_config()
    _mock_rest_api_client.return_value = {
        "10010": {
            "instrument_name": "LMS2101_AA1",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "8176",
                "uac2": "4726",
                "uac3": "3991"
            },
            "full_uac": "817647263991"
        }
    }

    questionnaire_name = "OPN2101A"

    # act
    result = get_questionnaire_uacs(questionnaire_name, config)
    print(result)

    # assert
    assert result["10010"]["uac_chunks"]["uac1"] == "8176"
    assert result["10010"]["uac_chunks"]["uac2"] == "4726"
    assert result["10010"]["uac_chunks"]["uac3"] == "3991"
