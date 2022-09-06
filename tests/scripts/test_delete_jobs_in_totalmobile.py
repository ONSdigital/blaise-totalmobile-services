from unittest import mock
from unittest.mock import create_autospec

from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from scripts.delete_totalmobile_jobs import (
    __delete_job,
    __get_active_world_ids,
    __map_world_id_to_job_reference,
    __remove_default_world_id,
)
from services.totalmobile_service import TotalmobileService
from tests.helpers import config_helper


def test_get_list_of_active_world_ids_returns_a_list_of_active_world_ids():
    totalmobile_service_mock = create_autospec(TotalmobileService)
    totalmobile_service_mock.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
        ],
    )

    assert __get_active_world_ids(totalmobile_service_mock) == [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ]


def test_remove_default_world_returns_a_list_without_default_world():
    default_world_id = "c0ffee00-c8d0-499f-8693-8be6ad1dc6ea"
    mod_world_id = "b9268537-c4ee-4ff2-b63c-a8a500cb2f04"
    list_of_active_world_ids = [
        default_world_id,
        mod_world_id,
        "c0ffee00-c8d0-499f-8693-8be6ad1dc7ea",
        "c0ffee00-c8d0-499f-8693-8be6ad1dc8ea",
        "c0ffee00-c8d0-499f-8693-8be6ad1dc9ea",
    ]
    assert __remove_default_world_id(list_of_active_world_ids) == [
        "c0ffee00-c8d0-499f-8693-8be6ad1dc7ea",
        "c0ffee00-c8d0-499f-8693-8be6ad1dc8ea",
        "c0ffee00-c8d0-499f-8693-8be6ad1dc9ea",
    ]


def test_get_list_of_active_world_ids_returns_a_list_of_active_world_ids_when_default_world_id_is_returned():
    default_world_id = "c0ffee00-c8d0-499f-8693-8be6ad1dc6ea"
    mod_world_id = "b9268537-c4ee-4ff2-b63c-a8a500cb2f04"
    totalmobile_service_mock = create_autospec(TotalmobileService)
    totalmobile_service_mock.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 3", id=default_world_id),
            World(region="Region 3", id=mod_world_id),
        ],
    )

    assert __get_active_world_ids(totalmobile_service_mock) == [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    ]


def test_build_dictionary():
    list_of_active_world_ids = [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "3fa85f64-5717-4562-b3fc-2c963f66afa7",
    ]
    totalmobile_service_mock = create_autospec(TotalmobileService)
    totalmobile_service_mock.get_jobs.return_value = [
        {"identity": {"reference": "Foo"}},
        {"identity": {"reference": "Bar"}},
    ]

    assert __map_world_id_to_job_reference(
        totalmobile_service_mock, list_of_active_world_ids
    ) == [
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
