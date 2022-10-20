from models.totalmobile.totalmobile_get_jobs_response_model import Job
from services.totalmobile_service import ITotalmobileService, RecallJobError, DeleteJobError


class DeleteTotalmobileJobService:
    def __init__(self, totalmobile_service: ITotalmobileService):
        self._totalmobile_service = totalmobile_service

    def delete_job(self, world_id: str, job: Job, reason: str) -> None:
        if job.allocated_resource_reference:
            self._recall_job(
                job.allocated_resource_reference, job.reference, job.work_type
            )

        self._delete_job(job, reason, world_id)

    def _recall_job(
        self, allocated_resource_reference: str, job_reference: str, work_type: str
    ) -> None:
        try:
            self._totalmobile_service.recall_job(
                allocated_resource_reference, work_type, job_reference
            )
        except RecallJobError:
            pass  # Swallow the exception and continue to the next job

    def _delete_job(self, job: Job, reason: str, world_id: str) -> None:
        try:
            self._totalmobile_service.delete_job(world_id, job.reference, reason)
        except DeleteJobError:
            pass  # Swallow the exception and continue to the next job
