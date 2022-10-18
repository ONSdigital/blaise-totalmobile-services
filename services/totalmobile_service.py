import requests

from client.optimise import GetJobsResponse, OptimiseClient
from models.cloud_tasks.totalmobile_create_job_model import TotalmobileCreateJobModel
from models.totalmobile.totalmobile_get_jobs_response_model import (
    TotalmobileGetJobsResponseModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel


class TotalmobileService:
    def __init__(self, optimise_client: OptimiseClient):
        self._optimise_client = optimise_client

    def get_world_model(self) -> TotalmobileWorldModel:
        worlds = self._optimise_client.get_worlds()
        return TotalmobileWorldModel.import_worlds(worlds)

    def create_job(self, job: TotalmobileCreateJobModel) -> requests.Response:
        return self._optimise_client.create_job(job.world_id, job.payload)

    def recall_job(self, reference: str) -> None:
        raise NotImplementedError("TODO")

    def delete_job(self, world_id: str, job: str, reason: str = "0") -> requests.Response:
        return self._optimise_client.delete_job(world_id, job, reason)

    def get_jobs(self, world_id: str) -> GetJobsResponse:
        return self._optimise_client.get_jobs(world_id)

    def get_jobs_model(self, world_id: str) -> TotalmobileGetJobsResponseModel:
        jobs_response = self.get_jobs(world_id)
        return TotalmobileGetJobsResponseModel.from_get_jobs_response(jobs_response)
