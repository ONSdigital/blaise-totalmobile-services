from unittest import mock

import pytest

from appconfig import Config
from client import bus
from models.blaise.questionnaire_uac_model import UacChunks
from services.uac_service import UacService
from tests.helpers import config_helper


@pytest.fixture()
def config() -> Config:
    return config_helper.get_default_config()


@pytest.fixture()
def uac_service(config) -> UacService:
    return UacService(config)


@mock.patch.object(bus.BusClient, "get_uacs_by_case_id")
def test_get_uacs_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client, uac_service
):
    # arrange
    questionnaire_name = "DST2106Z"

    # act
    uac_service.get_questionnaire_uac_model(questionnaire_name)

    # assert
    _mock_rest_api_client.assert_called_with(questionnaire_name)


@mock.patch.object(bus.BusClient, "get_uacs_by_case_id")
def test_get_questionnaire_uac_model_returns_an_expected_model(
    _mock_rest_api_client, uac_service
):
    # arrange
    _mock_rest_api_client.return_value = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {"uac1": "8176", "uac2": "4726", "uac3": "3991"},
            "full_uac": "817647263991",
        },
        "10020": {
            "instrument_name": "OPN2101A",
            "case_id": "10020",
            "uac_chunks": {"uac1": "8177", "uac2": "4727", "uac3": "3992"},
            "full_uac": "817647263992",
        },
        "10030": {
            "instrument_name": "OPN2101A",
            "case_id": "10030",
            "uac_chunks": {"uac1": "8178", "uac2": "4728", "uac3": "3993"},
            "full_uac": "817647263994",
        },
    }

    questionnaire_name = "OPN2101A"

    # act
    result = uac_service.get_questionnaire_uac_model(questionnaire_name)

    # assert
    assert result.questionnaire_case_uacs["10010"] == UacChunks(
        uac1="8176", uac2="4726", uac3="3991"
    )
    assert result.questionnaire_case_uacs["10020"] == UacChunks(
        uac1="8177", uac2="4727", uac3="3992"
    )
    assert result.questionnaire_case_uacs["10030"] == UacChunks(
        uac1="8178", uac2="4728", uac3="3993"
    )
