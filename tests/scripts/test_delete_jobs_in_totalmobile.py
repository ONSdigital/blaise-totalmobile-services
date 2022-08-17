from scripts.delete_totalmobile_jobs import delete_all_totalmobile_jobs_in_active_worlds, get_list_of_world_ids
from unittest import mock
from models.totalmobile_world_model import TotalmobileWorldModel, World
from tests.helpers import config_helper


@mock.patch("services.totalmobile_service.get_worlds")
def test_get_list_of_world_ids_returns_a_list_of_world_ids(mock_get_worlds):
    mock_get_worlds.return_value = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="3fa85f64-5717-4562-b3fc-2c963f66afa6")
        ],
    )
    config = config_helper.get_default_config()
    assert get_list_of_world_ids(config) == [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ]
