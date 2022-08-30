from unittest import mock

from client import bus
from models.blaise.uac_model import UacChunks, UacModel
from services import uac_service
from tests.helpers import config_helper


@mock.patch.object(bus.BusClient, "get_uacs_by_case_id")
def test_get_uacs_calls_the_rest_api_client_with_the_correct_parameters(_mock_rest_api_client):
    # arrange
    config = config_helper.get_default_config()
    questionnaire_name = "DST2106Z"

    # act
    uac_service.get_uacs(questionnaire_name, config)

    # assert
    _mock_rest_api_client.assert_called_with(questionnaire_name)


@mock.patch.object(bus.BusClient, "get_uacs_by_case_id")
def test_get_uacs_returns_a_list_of_uac_models(_mock_rest_api_client):
    # arrange
    config = config_helper.get_default_config()
    _mock_rest_api_client.return_value = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "8176",
                "uac2": "4726",
                "uac3": "3991"
            },
            "full_uac": "817647263991"
        },
        "10020": {
            "instrument_name": "OPN2101A",
            "case_id": "10020",
            "uac_chunks": {
                "uac1": "8177",
                "uac2": "4727",
                "uac3": "3992"
            },
            "full_uac": "817647263992"
        },
        "10030": {
            "instrument_name": "OPN2101A",
            "case_id": "10030",
            "uac_chunks": {
                "uac1": "8178",
                "uac2": "4728",
                "uac3": "3993"
            },
            "full_uac": "817647263994"
        },
    }

    questionnaire_name = "OPN2101A"

    # act
    result = uac_service.get_uacs(questionnaire_name, config)

    # assert
    assert result == [
        UacModel(
            case_id= "10010",
            uac_chunks=UacChunks(
                uac1="8176",
                uac2="4726",
                uac3="3991"
            )
        ),
        UacModel(
            case_id="10020",
            uac_chunks=UacChunks(
                uac1="8177",
                uac2="4727",
                uac3="3992"
            )
        ),
        UacModel(
            case_id="10030",
            uac_chunks=UacChunks(
                uac1="8178",
                uac2="4728",
                uac3="3993"
            )
        )
    ]

