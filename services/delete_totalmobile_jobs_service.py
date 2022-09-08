from client.optimise import OptimiseClient


class DeleteTotalmobileJobsService:
    def __init__(self, client: OptimiseClient):
        self.client = client

    def delete_totalmobile_job(self, world_id: str, job_reference: str, reason: str) -> None:
        self.client.delete_job(world_id, job_reference, reason)

    def delete_totalmobile_jobs_completed_in_blaise(self) -> str:
        return "foo"

    def get_incomplete_totalmobile_jobs(self) -> list[str]:
        return []
