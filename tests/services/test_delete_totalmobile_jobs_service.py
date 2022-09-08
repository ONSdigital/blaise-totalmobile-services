from client import OptimiseClient
from client.optimise import GetJobResponse
from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService
from unittest.mock import create_autospec


def test_delete_totalmobile_job_calls_correct_service():
    # arrange
    mock_optimise_client = create_autospec(OptimiseClient)
    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(mock_optimise_client)

    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"
    job_reference = "LMS1111-AA1.12345"
    reason = "110"

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_job(world_id, job_reference, reason)

    # assert
    mock_optimise_client.delete_job.assert_called_with(world_id, job_reference, reason)


def test_get_incomplete_totalmobile_jobs_returns_an_expected_list_of_jobs():
    # arrange
    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    mock_optimise_client = create_autospec(OptimiseClient)
    mock_optimise_client.get_jobs.return_value =

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(mock_optimise_client)

    # act
    result = delete_totalmobile_jobs_service.get_incomplete_totalmobile_jobs()

    # assert
    assert result == []
