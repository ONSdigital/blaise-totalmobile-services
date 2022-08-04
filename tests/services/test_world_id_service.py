from unittest import mock
from client.optimise import OptimiseClient
from tests.helpers import config_helper
from services.world_id_service import get_world_ids


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_world_ids_returns_a_dictionary_with_region_and_world_id_as_a_key_value_pair(_mock_optimise_client):
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

    assert get_world_ids(config) == {
        "Region 1": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "Region 2": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "Region 3": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
        "Region 4": "3fa85f64-5717-4562-b3fc-2c963f66afa9"
    }