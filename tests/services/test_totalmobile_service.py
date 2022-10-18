from unittest.mock import create_autospec

import pytest

from client import AuthException
from client.optimise import OptimiseClient
from models.cloud_tasks.totalmobile_create_job_model import TotalmobileCreateJobModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.totalmobile_service import TotalmobileService
from tests.helpers import optimise_client_helper


@pytest.fixture()
def optimise_client_mock():
    return create_autospec(OptimiseClient)


def test_get_world_model_returns_a_world_model(optimise_client_mock):
    # arrange
    optimise_client_mock.get_worlds.return_value = (
        optimise_client_helper.get_worlds_response()
    )

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


def test_create_job_calls_the_client_with_the_correct_parameters(optimise_client_mock):
    # arrange
    totalmobile_job_model = TotalmobileCreateJobModel(
        questionnaire="LMS2101_AA1",
        case_id="900001",
        world_id="3fa85f64-5717-4562-b3fc-2c963f66afa7",
        payload={},
    )

    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act
    totalmobile_service.create_job(totalmobile_job_model)

    # assert
    optimise_client_mock.create_job.assert_called_with(
        "3fa85f64-5717-4562-b3fc-2c963f66afa7", {}
    )


def test_create_job_auth_error(optimise_client_mock):
    # arrange
    optimise_client_mock.create_job.side_effect = AuthException()

    totalmobile_job_model = TotalmobileCreateJobModel(
        questionnaire="LMS2101_AA1",
        case_id="900001",
        world_id="3fa85f64-5717-4562-b3fc-2c963f66afa7",
        payload={},
    )

    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act & assert
    with pytest.raises(AuthException):
        totalmobile_service.create_job(totalmobile_job_model)


def test_get_jobs_calls_the_client_with_the_correct_parameters(optimise_client_mock):
    # arrange
    optimise_client_mock.get_jobs.return_value = {}
    world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act
    totalmobile_service.get_jobs(world_id)

    # assert
    optimise_client_mock.get_jobs.assert_called_with(world_id)


def test_get_jobs_model_returns_a_jobs_model(optimise_client_mock):
    # arrange
    optimise_client_mock.get_jobs.return_value = (
        optimise_client_helper.get_jobs_response()
    )
    world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act
    result = totalmobile_service.get_jobs_model(world_id)

    # assert
    assert len(result.questionnaire_jobs) == 2

    assert len(result.questionnaire_jobs["LMS1111_AA1"]) == 2
    assert result.questionnaire_jobs["LMS1111_AA1"][0].case_id == "12345"
    assert result.questionnaire_jobs["LMS1111_AA1"][0].reference == "LMS1111-AA1.12345"
    assert result.questionnaire_jobs["LMS1111_AA1"][0].visit_complete is True
    assert result.questionnaire_jobs["LMS1111_AA1"][1].case_id == "67890"
    assert result.questionnaire_jobs["LMS1111_AA1"][1].reference == "LMS1111-AA1.67890"
    assert result.questionnaire_jobs["LMS1111_AA1"][1].visit_complete is False

    assert len(result.questionnaire_jobs["LMS2222_BB2"]) == 1
    assert result.questionnaire_jobs["LMS2222_BB2"][0].case_id == "22222"
    assert result.questionnaire_jobs["LMS2222_BB2"][0].reference == "LMS2222-BB2.22222"
    assert result.questionnaire_jobs["LMS2222_BB2"][0].visit_complete is False


def test_get_jobs_model_calls_the_client_with_the_correct_parameters(optimise_client_mock):
    # arrange
    optimise_client_mock.get_jobs.return_value = {}
    world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act
    totalmobile_service.get_jobs_model(world_id)

    # assert
    optimise_client_mock.get_jobs.assert_called_with(world_id)


def test_delete_jobs_calls_the_client_with_the_correct_parameters_when_no_reason_json_passed(optimise_client_mock):
    # arrange
    world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    job = "1234"
    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act
    totalmobile_service.delete_job(world_id, job)

    # assert
    optimise_client_mock.delete_job.assert_called_with(world_id, job, "0")


def test_delete_jobs_calls_the_client_with_the_correct_parameters_when_reason_json_passed(optimise_client_mock):
    # arrange
    world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    job = "1234"
    totalmobile_service = TotalmobileService(optimise_client_mock)

    # act
    totalmobile_service.delete_job(world_id, job, "110")

    # assert
    optimise_client_mock.delete_job.assert_called_with(world_id, job, "110")
