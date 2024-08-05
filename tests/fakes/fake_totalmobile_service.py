from collections import defaultdict
from typing import Dict, Optional, Sequence, List

import requests

from client.optimise import GetJobResponse, GetJobsResponse
from models.blaise.blaise_case_information_base_model import BlaiseCaseInformationBaseModel
from models.cloud_tasks.totalmobile_create_job_model import TotalmobileCreateJobModel
from models.totalmobile.totalmobile_get_jobs_response_model import (
    TotalmobileGetJobsResponseModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.totalmobile_service import DeleteJobError


class FakeTotalmobileService:
    REGIONS = {
        "Region 0": "world-id-0",
        "Region 1": "world-id-1",
        "Region 2": "world-id-2",
        "Region 3": "world-id-3",
        "Region 4": "world-id-4",
        "Region 5": "world-id-5",
        "Region 6": "world-id-6",
        "Region 7": "world-id-7",
        "Region 8": "world-id-8",
        "Region 9": "world-id-9",
    }

    def __init__(self):
        self._jobs: Dict[str, Dict[str, GetJobResponse]] = defaultdict(dict)
        self._delete_jobs_reason = {}
        self._errors_when_method_is_called = []
        self._recalled_jobs = {}

    def method_throws_exception(self, method_name: str):
        self._errors_when_method_is_called.append(method_name)

    def add_job(
        self,
        reference: str,
        region: str,
        visit_complete: bool = False,
        due_date: Optional[str] = None,
        allocated_resource_reference: Optional[str] = None,
    ) -> None:
        world_id = self.REGIONS[region]
        if self.job_exists(reference):
            raise Exception(f"Job with reference {reference} already exists")

        self._jobs[world_id][reference] = {
            "visitComplete": visit_complete,
            "identity": {"reference": reference},
            "dueDate": {"end": due_date},
            "allocatedResource": (
                {"reference": allocated_resource_reference}
                if allocated_resource_reference
                else None
            ),
            "workType": "LMS",
        }

    def update_due_date(self, reference: str, region: str, due_date: str) -> None:
        world_id = self.REGIONS[region]
        job = self._jobs[world_id][reference]
        job["dueDate"] = {"end": due_date}

    def job_exists(self, job: str) -> bool:
        for jobs_in_world in self._jobs.values():
            if job in jobs_in_world:
                return True
        return False

    def job_has_been_recalled(
        self, allocated_resource_reference: str, job_reference: str
    ) -> bool:
        result = self._recalled_jobs.get(
            f"{job_reference}::{allocated_resource_reference}", False
        )
        return result

    def recall_job(
        self, allocated_resource_reference: str, _work_type: str, job_reference: str
    ) -> None:
        self._recalled_jobs[f"{job_reference}::{allocated_resource_reference}"] = True

    def delete_job(
        self, world_id: str, reference: str, reason: str = "0"
    ) -> requests.Response:
        if "delete_job" in self._errors_when_method_is_called:
            raise DeleteJobError("get_jobs_model has errored")

        self._delete_jobs_reason[reference] = reason
        del self._jobs[world_id][reference]

        return requests.Response()

    def deleted_with_reason(self, reference: str, reason: str = "0") -> bool:
        if reference not in self._delete_jobs_reason.keys():
            return False

        return self._delete_jobs_reason[reference] == reason

    def get_world_model(self) -> TotalmobileWorldModel:
        if "get_world_model" in self._errors_when_method_is_called:
            raise Exception("get_jobs_model has errored")

        return TotalmobileWorldModel(
            worlds=[
                World(region=region, id=id)
                for region, id in self.REGIONS.items()
                if region in TotalmobileWorldModel.get_available_regions()
            ]
        )

    def get_jobs_model(self, world_id: str) -> TotalmobileGetJobsResponseModel:
        if "get_jobs_model" in self._errors_when_method_is_called:
            raise Exception("get_jobs_model has errored")

        if not self._jobs:
            raise Exception("get_jobs_models was called when no jobs were present")

        return TotalmobileGetJobsResponseModel.from_get_jobs_response(
            list(self._jobs[world_id].values())
        )

    def create_job(self, job: TotalmobileCreateJobModel) -> requests.Response:
        raise NotImplementedError("Currently not implemented in this mock")

    def get_jobs(self, world_id: str) -> GetJobsResponse:
        raise NotImplementedError("Currently not implemented in this mock")

    def map_totalmobile_create_job_models(
            self,
            questionnaire_name: str,
            cases: Sequence[BlaiseCaseInformationBaseModel]
    ) -> List[TotalmobileCreateJobModel]:
        raise NotImplementedError("Currently not implemented in this mock")
