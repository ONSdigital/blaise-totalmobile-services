from typing import Dict, List

from client.optimise import GetJobsResponse, OptimiseClient
from models.cloud_tasks.totalmobile_outgoing_job_model import TotalmobileJobModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel


class TotalmobileService:
    def __init__(self, client: OptimiseClient):
        self.client = client

    def get_world_model(self) -> TotalmobileWorldModel:
        worlds = self.client.get_worlds()
        return TotalmobileWorldModel.import_worlds(worlds)

    def create_job(self, job: TotalmobileJobModel):
        return self.client.create_job(job.world_id, job.payload)

    def delete_job(self, world_id: str, job: str, reason: str = "0"):
        reason_json = {"deletionReason": {"reference": reason}}
        return self.client.delete_job(world_id, job, reason_json)

    def get_jobs(self, world_id: str) -> GetJobsResponse:
        return self.client.get_jobs(world_id)
