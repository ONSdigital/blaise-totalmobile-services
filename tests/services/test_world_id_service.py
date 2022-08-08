from unittest import mock
from client.optimise import OptimiseClient
from tests.helpers import config_helper
from services.world_id_service import get_world


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_world_returns_a_world_model(_mock_optimise_client):
    config = config_helper.get_default_config()
    _mock_optimise_client.return_value = [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {
                "reference": "Region 1"
            },
            "type": "foo"
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "identity": {
                "reference": "Region 2"
            },
            "type": "foo"
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
            "identity": {
                "reference": "Region 3"
            },
            "type": "foo"
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
            "identity": {
                "reference": "Region 4"
            },
            "type": "foo"
        },
    ]

    result = get_world(config)

    assert result.worlds[0].region == "Region 1"
    assert result.worlds[0].id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"

    assert result.worlds[1].region == "Region 2"
    assert result.worlds[1].id == "3fa85f64-5717-4562-b3fc-2c963f66afa7"

    assert result.worlds[2].region == "Region 3"
    assert result.worlds[2].id == "3fa85f64-5717-4562-b3fc-2c963f66afa8"

    assert result.worlds[3].region == "Region 4"
    assert result.worlds[3].id == "3fa85f64-5717-4562-b3fc-2c963f66afa9"