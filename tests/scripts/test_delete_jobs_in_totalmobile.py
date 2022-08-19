from scripts.delete_totalmobile_jobs import (
    get_list_of_active_world_ids,
    remove_default_world_id_from_the_list_of_active_world_ids,
    get_list_of_world_ids_and_job_references,
    delete_job,
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

    assert get_list_of_active_world_ids(config) == [
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
    assert remove_default_world_id_from_the_list_of_active_world_ids(list_of_active_world_ids) == [
        "c0ffee00-c8d0-499f-8693-8be6ad1dc7ea",
        "c0ffee00-c8d0-499f-8693-8be6ad1dc8ea",
        "c0ffee00-c8d0-499f-8693-8be6ad1dc9ea",
    ]


@mock.patch("services.totalmobile_service.get_worlds")
def test_get_list_of_active_world_ids_returns_a_list_of_active_world_ids_when_default_world_id_is_returned(mock_get_worlds):
    default_world_id = "c0ffee00-c8d0-499f-8693-8be6ad1dc6ea"
    mock_get_worlds.return_value = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 3", id=default_world_id),
        ],
    )
    config = config_helper.get_default_config()

    assert get_list_of_active_world_ids(config) == [
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

    assert get_list_of_world_ids_and_job_references(config, list_of_active_world_ids) == [
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

# TODO:
# Test delete job function now that concurrency has been added


# @mock.patch("services.totalmobile_service.delete_job")
# def test_delete_job(mock_delete_job):
#     config = config_helper.get_default_config()
#     list_of_jobs = [
#         {
#             "world_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#             "reference": "Bar",
#         },
#     ]
#
#     result = delete_job(config, list_of_jobs)
#
#     mock_delete_job.assert_called_with(config, "3fa85f64-5717-4562-b3fc-2c963f66afa6", "Bar")
