from unittest import mock
from client.optimise import OptimiseClient
from tests.helpers import config_helper
from services.totalmobile_restapi_service import get_worlds


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_worlds_calls_the_rest_api_client_with_the_correct_parameters(_mock_rest_api_client):
    # arrange
    config = config_helper.get_default_config()

    # act
    get_worlds(config)

    # assert
    _mock_rest_api_client.assert_called_with()


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_worlds_calls_returns_the_world_data_supplied_by_the_rest_api_client(_mock_rest_api_client):
    # arrange
    config = config_helper.get_default_config()
    _mock_rest_api_client.return_value = [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {
                "reference": "Region 1"
            },
            "type": "foo"
        }
    ]

    # act
    result = get_worlds(config)

    # assert
    assert len(result) == 1
    assert result[0]["id"] == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    assert result[0]["identity"]["reference"] == "Region 1"
    assert result[0]["type"] == "foo"
