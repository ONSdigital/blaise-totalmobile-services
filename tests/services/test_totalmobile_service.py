from unittest.mock import create_autospec

import pytest

from client import AuthException
from client.optimise import OptimiseClient
from models.cloud_tasks.totalmobile_outgoing_job_model import TotalmobileJobModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.totalmobile_service import TotalmobileService


def test_get_world_model_returns_a_world_model():
    # arrange
    optimise_client_mock = create_autospec(OptimiseClient)
    optimise_client_mock.get_worlds.return_value = [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {"reference": "Region 1"},
            "type": "foo",
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "identity": {"reference": "Region 2"},
            "type": "foo",
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
            "identity": {"reference": "Region 3"},
            "type": "foo",
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
            "identity": {"reference": "Region 4"},
            "type": "foo",
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa2",
            "identity": {"reference": "Region 5"},
            "type": "foo",
        },
    ]

    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act
    result = totalmobile_service.get_world_model()

    # assert
    print(result)
    assert result == TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="3fa85f64-5717-4562-b3fc-2c963f66afa7"),
            World(region="Region 3", id="3fa85f64-5717-4562-b3fc-2c963f66afa8"),
            World(region="Region 4", id="3fa85f64-5717-4562-b3fc-2c963f66afa9"),
            World(region="Region 5", id="3fa85f64-5717-4562-b3fc-2c963f66afa2"),
        ]
    )


def test_create_job_calls_the_client_with_the_correct_parameters():
    # arrange
    optimise_client_mock = create_autospec(OptimiseClient)
    totalmobile_job_model = TotalmobileJobModel(
        questionnaire="LMS2101_AA1",
        case_id="900001",
        world_id="3fa85f64-5717-4562-b3fc-2c963f66afa7",
        payload="{}",
    )

    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act
    totalmobile_service.create_job(totalmobile_job_model)

    # assert
    optimise_client_mock.create_job.assert_called_with(
        "3fa85f64-5717-4562-b3fc-2c963f66afa7", "{}"
    )


def test_create_job_auth_error():
    # arrange
    optimise_client_mock = create_autospec(OptimiseClient)
    optimise_client_mock.create_job.side_effect = AuthException()

    totalmobile_job_model = TotalmobileJobModel(
        questionnaire="LMS2101_AA1",
        case_id="900001",
        world_id="3fa85f64-5717-4562-b3fc-2c963f66afa7",
        payload="{}",
    )

    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act & assert
    with pytest.raises(AuthException):
        totalmobile_service.create_job(totalmobile_job_model)


def test_get_jobs_calls_the_rest_api_client_with_the_correct_parameters():
    # arrange
    optimise_client_mock = create_autospec(OptimiseClient)
    optimise_client_mock.get_jobs.return_value = {}
    world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act
    totalmobile_service.get_jobs(world_id)

    # assert
    optimise_client_mock.get_jobs.assert_called_with(world_id)


def test_delete_jobs_calls_the_rest_api_client_with_the_correct_parameters():
    # arrange
    optimise_client_mock = create_autospec(OptimiseClient)
    optimise_client_mock.get_jobs.return_value = {}
    world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    job = "1234"
    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act
    totalmobile_service.delete_job(world_id, job)

    # assert
    optimise_client_mock.delete_job.assert_called_with(world_id, job, "0")
