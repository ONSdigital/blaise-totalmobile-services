import pytest

from unittest import mock
from client import AuthException
from client.optimise import OptimiseClient
from models.totalmobile_job_model import TotalmobileJobModel
from tests.helpers import config_helper
from services.totalmobile_service import get_worlds, create_job, get_jobs, delete_job
from models.totalmobile_world_model import TotalmobileWorldModel, World


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_worlds_calls_the_rest_api_client_with_the_correct_parameters(_mock_get_worlds):
    # arrange
    config = config_helper.get_default_config()

    # act
    get_worlds(config)

    # assert
    _mock_get_worlds.assert_called_with()


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_worlds_calls_returns_a_world_model(_mock_get_worlds):
    # arrange
    config = config_helper.get_default_config()
    _mock_get_worlds.return_value = [
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

    # act
    result = get_worlds(config)

    # assert
    print(result)
    assert result == TotalmobileWorldModel(
        worlds=[
            World(
                region="Region 1",
                id="3fa85f64-5717-4562-b3fc-2c963f66afa6"
            ),
            World(
                region="Region 2",
                id="3fa85f64-5717-4562-b3fc-2c963f66afa7"
            ),
            World(
                region="Region 3",
                id="3fa85f64-5717-4562-b3fc-2c963f66afa8"
            ),
            World(
                region="Region 4",
                id="3fa85f64-5717-4562-b3fc-2c963f66afa9"
            )
        ])


@mock.patch.object(OptimiseClient, "create_job")
def test_create_job_calls_the_rest_api_client_with_the_correct_parameters(_mock_create_job):
    # arrange
    config = config_helper.get_default_config()
    totalmobile_job_model = TotalmobileJobModel(
        questionnaire="LMS2101_AA1",
        case_id="900001",
        world_id="3fa85f64-5717-4562-b3fc-2c963f66afa7",
        payload="{}"
    )

    # act
    create_job(config, totalmobile_job_model)

    # assert
    _mock_create_job.assert_called_with(
        "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "{}"
    )


@mock.patch.object(OptimiseClient, "create_job")
def test_create_job_auth_error(_mock_create_job):
    # arrange
    config = config_helper.get_default_config()
    totalmobile_job_model = TotalmobileJobModel(
        questionnaire="LMS2101_AA1",
        case_id="900001",
        world_id="3fa85f64-5717-4562-b3fc-2c963f66afa7",
        payload="{}"
    )
    _mock_create_job.side_effect = AuthException()

    with pytest.raises(AuthException):
        create_job(config, totalmobile_job_model)


@mock.patch.object(OptimiseClient, "get_jobs")
def test_get_jobs_calls_the_rest_api_client_with_the_correct_parameters(_mock_get_jobs):
    # arrange
    config = config_helper.get_default_config()
    world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"

    # act
    get_jobs(config, world_id)

    # assert
    _mock_get_jobs.assert_called_with(world_id)


@mock.patch.object(OptimiseClient, "delete_job")
def test_delete_jobs_calls_the_rest_api_client_with_the_correct_parameters(_mock_delete_job):
    # arrange
    config = config_helper.get_default_config()
    world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    job = "1234"

    # act
    delete_job(config, world_id, job)

    # assert
    _mock_delete_job.assert_called_with(world_id, job)
