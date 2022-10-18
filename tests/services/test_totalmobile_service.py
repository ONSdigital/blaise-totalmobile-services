from unittest.mock import create_autospec

import pytest
import requests

from client import AuthException
from client.messaging import MessagingClient
from client.optimise import OptimiseClient
from models.cloud_tasks.totalmobile_create_job_model import TotalmobileCreateJobModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.totalmobile_service import RecallJobError, TotalmobileService
from tests.helpers import optimise_client_helper


def mock_response(status_code: int) -> requests.Response:
    response = requests.Response()
    response.status_code = status_code
    return response


@pytest.fixture()
def optimise_client_mock():
    return create_autospec(OptimiseClient)


@pytest.fixture()
def messaging_client_mock():
    mock = create_autospec(MessagingClient)

    mock.force_recall_visit.return_value = mock_response(status_code=201)

    return mock


@pytest.fixture()
def totalmobile_service(optimise_client_mock, messaging_client_mock):
    return TotalmobileService(optimise_client_mock, messaging_client_mock)


class TestGetWorldModel:
    def test_returns_a_world_model(self, totalmobile_service, optimise_client_mock):
        # arrange
        optimise_client_mock.get_worlds.return_value = (
            optimise_client_helper.get_worlds_response()
        )

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


class TestCreateJob:
    def test_create_job_calls_the_client_with_the_correct_parameters(
        self, totalmobile_service, optimise_client_mock
    ):
        # arrange
        totalmobile_job_model = TotalmobileCreateJobModel(
            questionnaire="LMS2101_AA1",
            case_id="900001",
            world_id="3fa85f64-5717-4562-b3fc-2c963f66afa7",
            payload={},
        )

        # act
        totalmobile_service.create_job(totalmobile_job_model)

        # assert
        optimise_client_mock.create_job.assert_called_with(
            "3fa85f64-5717-4562-b3fc-2c963f66afa7", {}
        )

    def test_create_job_auth_error(self, totalmobile_service, optimise_client_mock):
        # arrange
        optimise_client_mock.create_job.side_effect = AuthException()

        totalmobile_job_model = TotalmobileCreateJobModel(
            questionnaire="LMS2101_AA1",
            case_id="900001",
            world_id="3fa85f64-5717-4562-b3fc-2c963f66afa7",
            payload={},
        )

        # act & assert
        with pytest.raises(AuthException):
            totalmobile_service.create_job(totalmobile_job_model)


class TestGetJob:
    def test_calls_the_client_with_the_correct_parameters(
        self, totalmobile_service, optimise_client_mock
    ):
        # arrange
        optimise_client_mock.get_jobs.return_value = {}
        world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"

        # act
        totalmobile_service.get_jobs(world_id)

        # assert
        optimise_client_mock.get_jobs.assert_called_with(world_id)


class TestGetJobsModel:
    def test_returns_a_jobs_model(self, totalmobile_service, optimise_client_mock):
        # arrange
        optimise_client_mock.get_jobs.return_value = (
            optimise_client_helper.get_jobs_response()
        )
        world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"

        # act
        result = totalmobile_service.get_jobs_model(world_id)

        # assert
        assert len(result.questionnaire_jobs) == 2

        assert len(result.questionnaire_jobs["LMS1111_AA1"]) == 2
        assert result.questionnaire_jobs["LMS1111_AA1"][0].case_id == "12345"
        assert (
            result.questionnaire_jobs["LMS1111_AA1"][0].reference == "LMS1111-AA1.12345"
        )
        assert result.questionnaire_jobs["LMS1111_AA1"][0].visit_complete is True
        assert result.questionnaire_jobs["LMS1111_AA1"][1].case_id == "67890"
        assert (
            result.questionnaire_jobs["LMS1111_AA1"][1].reference == "LMS1111-AA1.67890"
        )
        assert result.questionnaire_jobs["LMS1111_AA1"][1].visit_complete is False

        assert len(result.questionnaire_jobs["LMS2222_BB2"]) == 1
        assert result.questionnaire_jobs["LMS2222_BB2"][0].case_id == "22222"
        assert (
            result.questionnaire_jobs["LMS2222_BB2"][0].reference == "LMS2222-BB2.22222"
        )
        assert result.questionnaire_jobs["LMS2222_BB2"][0].visit_complete is False

    def test_calls_the_client_with_the_correct_parameters(
        self, totalmobile_service, optimise_client_mock
    ):
        # arrange
        optimise_client_mock.get_jobs.return_value = {}
        world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"

        # act
        totalmobile_service.get_jobs_model(world_id)

        # assert
        optimise_client_mock.get_jobs.assert_called_with(world_id)


class TestDeleteJobs:
    def test_calls_the_client_with_the_correct_parameters_when_no_reason_json_passed(
        self, totalmobile_service, optimise_client_mock
    ):
        # arrange
        world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        job = "1234"

        # act
        totalmobile_service.delete_job(world_id, job)

        # assert
        optimise_client_mock.delete_job.assert_called_with(world_id, job, "0")

    def test_calls_the_client_with_the_correct_parameters_when_reason_json_passed(
        self, totalmobile_service, optimise_client_mock
    ):
        # arrange
        world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        job = "1234"

        # act
        totalmobile_service.delete_job(world_id, job, "110")

        # assert
        optimise_client_mock.delete_job.assert_called_with(world_id, job, "110")


class TestRecallJob:
    def test_calls_client_with_the_correct_parameters(
        self, totalmobile_service, messaging_client_mock
    ):
        # arrange
        response = requests.Response()
        response.status_code = 201
        messaging_client_mock.force_recall_visit.return_value = response

        # arrange
        totalmobile_service.recall_job("bob.minion", "LMS", "LMS1111_AA1.12345")

        # assert
        messaging_client_mock.force_recall_visit.assert_called_with(
            "bob.minion", "LMS", "LMS1111_AA1.12345"
        )

    @pytest.mark.parametrize("incorrect_response", [200, 202, 301, 400, 500])
    def test_raises_when_response_is_not_201(
        self, incorrect_response, totalmobile_service, messaging_client_mock
    ):
        # arrange
        response = requests.Response()
        response.status_code = incorrect_response
        messaging_client_mock.force_recall_visit.return_value = response

        # act & assert
        with pytest.raises(
            RecallJobError,
            match=f"Expected response status of 201, got {incorrect_response}",
        ):
            totalmobile_service.recall_job("bob.minion", "LMS", "LMS1111_AA1.12345")

    def test_raises_an_exception_when_the_client_raises_an_exception(
        self, totalmobile_service, messaging_client_mock
    ):
        # arrange
        client_error = RuntimeError("Random error")
        messaging_client_mock.force_recall_visit.side_effect = client_error

        # act & assert
        with pytest.raises(
            RecallJobError, match="The messaging client raise an error"
        ) as error:
            totalmobile_service.recall_job("bob.minion", "LMS", "LMS1111_AA1.12345")

        assert error.value.args[1] == client_error
