from unittest.mock import create_autospec

from models.common.totalmobile.totalmobile_world_model import (
    TotalmobileWorldModel,
    World,
)
from scripts.delete_totalmobile_jobs import (
    __get_active_world_ids,
    __map_world_id_to_job_reference,
)
from services.totalmobile_service import RealTotalmobileService


def test_get_list_of_active_world_ids_returns_a_list_of_active_world_ids():
    totalmobile_service_mock = create_autospec(RealTotalmobileService)
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


def test_build_dictionary():
    list_of_active_world_ids = [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "3fa85f64-5717-4562-b3fc-2c963f66afa7",
    ]
    totalmobile_service_mock = create_autospec(RealTotalmobileService)
    totalmobile_service_mock.get_jobs.return_value = [
        {"identity": {"reference": "Foo"}, "visitComplete": False},
        {"identity": {"reference": "Bar"}, "visitComplete": False},
    ]

    assert __map_world_id_to_job_reference(
        totalmobile_service_mock, list_of_active_world_ids
    ) == [
        {
            "world_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "job_reference": "Foo",
        },
        {
            "world_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "job_reference": "Bar",
        },
        {
            "world_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "job_reference": "Foo",
        },
        {
            "world_id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "job_reference": "Bar",
        },
    ]
