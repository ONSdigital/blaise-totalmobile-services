from unittest.mock import create_autospec

from cloud_functions.create_totalmobile_jobs_trigger import (
    create_totalmobile_jobs_trigger,
)
from services.create.create_totalmobile_jobs_service import CreateTotalmobileJobsService


def test_create_totalmobile_jobs_completed_in_blaise_returns_value_from_service():
    # arrange
    mock_create_totalmobile_jobs_service = create_autospec(CreateTotalmobileJobsService)

    mock_create_totalmobile_jobs_service.create_totalmobile_jobs.return_value = "Done"
    # act and assert
    assert (
        create_totalmobile_jobs_trigger(mock_create_totalmobile_jobs_service) == "Done"
    )


def test_delete_totalmobile_jobs_completed_in_blaise_calls_the_correct_service():
    # arrange
    mock_create_totalmobile_jobs_service = create_autospec(CreateTotalmobileJobsService)

    # act
    create_totalmobile_jobs_trigger(mock_create_totalmobile_jobs_service)

    # assert
    mock_create_totalmobile_jobs_service.create_totalmobile_jobs.assert_called()
