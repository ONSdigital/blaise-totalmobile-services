from unittest.mock import create_autospec

import pytest

from models.delete.totalmobile_get_jobs_response_model import Job
from services.common.totalmobile_service import (
    DeleteJobError,
    RecallJobError,
    TotalmobileService,
)
from services.delete.delete_totalmobile_job_service import DeleteTotalmobileJobService


@pytest.fixture()
def totalmobile_service():
    return create_autospec(TotalmobileService)


@pytest.fixture()
def delete_job_service(totalmobile_service) -> DeleteTotalmobileJobService:
    return DeleteTotalmobileJobService(totalmobile_service)


def test_deletes_the_job(delete_job_service, totalmobile_service):
    world_id = "b8368839-be8b-4a95-90e7-6a1e7c7c3f37"
    job_reference = "LMS2209-AA1.12345"
    job = Job(job_reference, "12345", False, False, "stuart.minion", "LMS")
    reason = "completed"

    delete_job_service.delete_job(world_id, job, reason)

    totalmobile_service.delete_job.assert_called_with(world_id, job_reference, reason)


def test_does_not_raise_when_delete_job_raises(delete_job_service, totalmobile_service):
    totalmobile_service.delete_job.side_effect = DeleteJobError("Kaboom")

    world_id = "b8368839-be8b-4a95-90e7-6a1e7c7c3f37"
    job_reference = "LMS2209-AA1.12345"
    job = Job(job_reference, "12345", False, False, "stuart.minion", "LMS")
    reason = "completed"

    delete_job_service.delete_job(world_id, job, reason)


def test_raise_when_delete_fails_with_unknown_exception(
    delete_job_service, totalmobile_service
):
    totalmobile_service.delete_job.side_effect = Exception("Kaboom")

    world_id = "b8368839-be8b-4a95-90e7-6a1e7c7c3f37"
    job = Job("LMS2209-AA1.12345", "12345", False, False, "kevin.minion", "LMS")
    reason = "completed"

    with pytest.raises(Exception, match="Kaboom"):
        delete_job_service.delete_job(world_id, job, reason)


def test_recalls_the_job(delete_job_service, totalmobile_service):
    world_id = "b8368839-be8b-4a95-90e7-6a1e7c7c3f37"
    job = Job("LMS2209-AA1.12345", "12345", False, False, "stuart.minion", "LMS")
    reason = "completed"

    delete_job_service.delete_job(world_id, job, reason)

    totalmobile_service.recall_job.assert_called_with(
        "stuart.minion", "LMS", "LMS2209-AA1.12345"
    )


def test_does_not_recalls_the_job_when_not_allocated(
    delete_job_service, totalmobile_service
):
    world_id = "b8368839-be8b-4a95-90e7-6a1e7c7c3f37"
    job = Job("LMS2209-AA1.12345", "12345", False, False, None, "LMS")
    reason = "completed"

    delete_job_service.delete_job(world_id, job, reason)

    totalmobile_service.recall_job.assert_not_called()


def test_does_delete_the_job_when_not_allocated(
    delete_job_service, totalmobile_service
):
    world_id = "b8368839-be8b-4a95-90e7-6a1e7c7c3f37"
    job = Job("LMS2209-AA1.12345", "12345", False, False, None, "LMS")
    reason = "completed"

    delete_job_service.delete_job(world_id, job, reason)

    totalmobile_service.delete_job.assert_called()


def test_still_deletes_job_when_recall_fails(delete_job_service, totalmobile_service):
    totalmobile_service.recall_job.side_effect = RecallJobError("Recall failed")

    world_id = "b8368839-be8b-4a95-90e7-6a1e7c7c3f37"
    job = Job("LMS2209-AA1.12345", "12345", False, False, "kevin.minion", "LMS")
    reason = "completed"

    delete_job_service.delete_job(world_id, job, reason)

    totalmobile_service.delete_job.assert_called()


def test_raise_when_recall_fails_with_unknown_exception(
    delete_job_service, totalmobile_service
):
    totalmobile_service.recall_job.side_effect = Exception("Kaboom")

    world_id = "b8368839-be8b-4a95-90e7-6a1e7c7c3f37"
    job = Job("LMS2209-AA1.12345", "12345", False, False, "kevin.minion", "LMS")
    reason = "completed"

    with pytest.raises(Exception, match="Kaboom"):
        delete_job_service.delete_job(world_id, job, reason)
