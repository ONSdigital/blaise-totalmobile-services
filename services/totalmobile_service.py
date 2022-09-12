from client.optimise import GetJobsResponse, OptimiseClient
from models.cloud_tasks.totalmobile_job_request_model import TotalmobileJobRequestModel
from models.totalmobile.totalmobile_jobs_response_model import (
    TotalmobileJobsResponseModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel


class TotalmobileService:
    def __init__(self, client: OptimiseClient):
        self.client = client

    def get_world_model(self) -> TotalmobileWorldModel:
        worlds = self.client.get_worlds()
        return TotalmobileWorldModel.import_worlds(worlds)

    def create_job(self, job: TotalmobileJobRequestModel):
        return self.client.create_job(job.world_id, job.payload)

    def delete_job(self, world_id: str, job: str, reason: str = "0"):
        return self.client.delete_job(world_id, job, reason)

    def get_jobs(self, world_id: str) -> GetJobsResponse:
        return self.client.get_jobs(world_id)

    def get_jobs_model(self, world_id: str) -> TotalmobileJobsResponseModel:
        jobs_response = self.get_jobs(world_id)
        return TotalmobileJobsResponseModel(jobs_response)
