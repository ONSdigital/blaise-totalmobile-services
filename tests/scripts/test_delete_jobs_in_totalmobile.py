from scripts.delete_totalmobile_jobs import (
    __delete_job,
    __get_active_world_ids,
    __map_world_id_to_job_reference,
    __remove_default_world_id,
)
from unittest import mock
from models.totalmobile_world_model import TotalmobileWorldModel, World
from tests.helpers import config_helper


@mock.patch("services.totalmobile_service.get_worlds")
def test_get_list_of_active_world_ids_returns_a_list_of_active_world_ids(mock_get_worlds):
    mock_get_worlds.return_value = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="3fa85f64-5717-4562-b3fc-2c963f66afa6")
        ],
    )
    config = config_helper.get_default_config()

    assert __get_active_world_ids(config) == [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ]


def test_remove_default_world_returns_a_list_without_default_world():
    default_world_id = "c0ffee00-c8d0-499f-8693-8be6ad1dc6ea"
    list_of_active_world_ids = [
        default_world_id,
        "c0ffee00-c8d0-499f-8693-8be6ad1dc7ea",
        "c0ffee00-c8d0-499f-8693-8be6ad1dc8ea",
        "c0ffee00-c8d0-499f-8693-8be6ad1dc9ea",
    ]
    assert __remove_default_world_id(list_of_active_world_ids) == [
        "c0ffee00-c8d0-499f-8693-8be6ad1dc7ea",
        "c0ffee00-c8d0-499f-8693-8be6ad1dc8ea",
        "c0ffee00-c8d0-499f-8693-8be6ad1dc9ea",
    ]


@mock.patch("services.totalmobile_service.get_worlds")
def test_get_list_of_active_world_ids_returns_a_list_of_active_world_ids_when_default_world_id_is_returned(
        mock_get_worlds):
    default_world_id = "c0ffee00-c8d0-499f-8693-8be6ad1dc6ea"
    mock_get_worlds.return_value = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 3", id=default_world_id),
        ],
    )
    config = config_helper.get_default_config()

    assert __get_active_world_ids(config) == [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ]


@mock.patch("services.totalmobile_service.get_jobs")
def test_build_dictionary(mock_get_jobs):
    config = config_helper.get_default_config()
    list_of_active_world_ids = ["3fa85f64-5717-4562-b3fc-2c963f66afa6", "3fa85f64-5717-4562-b3fc-2c963f66afa7"]

    mock_get_jobs.return_value = [
        {"identity": {"reference": "Foo"}},
        {"identity": {"reference": "Bar"}},
    ]

    assert __map_world_id_to_job_reference(config, list_of_active_world_ids) == [
        {
            "world_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "reference": "Foo",
        },
        {
            "world_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "reference": "Bar",
        },
        {
            "world_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "reference": "Foo",
        },
        {
            "world_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "reference": "Bar",
        },
    ]
