from unittest.mock import create_autospec

from cloud_functions.delete_totalmobile_jobs_completed_in_blaise import (
    delete_totalmobile_jobs_completed_in_blaise,
)
from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService


def test_delete_totalmobile_jobs_completed_in_blaise_returns_done():
    # arrange
    mock_delete_totalmobile_jobs_service = create_autospec(DeleteTotalmobileJobsService)

    # act and assert
    assert (
        delete_totalmobile_jobs_completed_in_blaise(
            mock_delete_totalmobile_jobs_service
        )
        == "Done"
    )


def test_delete_totalmobile_jobs_completed_in_blaise_calls_the_correct_service():
    # arrange
    mock_delete_totalmobile_jobs_service = create_autospec(DeleteTotalmobileJobsService)

    # act
    delete_totalmobile_jobs_completed_in_blaise(mock_delete_totalmobile_jobs_service)

    # assert
    mock_delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise.assert_called()
