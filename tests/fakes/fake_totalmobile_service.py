from collections import defaultdict
from typing import Callable, List

from models.totalmobile.totalmobile_get_jobs_response_model import (
    TotalmobileGetJobsResponseModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World


class FakeTotalmobileService:
    REGIONS = {
        "Region 1": "world-id-1",
        "Region 2": "world-id-2",
        "Region 3": "world-id-3",
        "Region 4": "world-id-4",
        "Region 5": "world-id-5",
        "Region 6": "world-id-6",
        "Region 7": "world-id-7",
        "Region 8": "world-id-8",
    }

    def __init__(self):
        self._jobs = defaultdict(dict)
        self._delete_jobs = defaultdict(lambda: 0)
        self._errors_when_method_is_called = []

    def method_throws_exception(self, method_name: str):
        self._errors_when_method_is_called.append(method_name)

    def add_job(
        self, reference: str, region: str, visit_complete: bool = False
    ) -> None:
        world_id = self.REGIONS[region]
        self._jobs[world_id][reference] = {
            "visitComplete": visit_complete,
            "identity": {"reference": reference},
        }

    def job_exists(self, job: str, world_id: str) -> bool:
        return job in self._jobs[world_id]

    def delete_job(self, world_id: str, job: str, reason: str = "0") -> None:
        if "delete_job" in self._errors_when_method_is_called:
            raise Exception("get_jobs_model has errored")

        del self._jobs[world_id][job]

    def get_world_model(self) -> TotalmobileWorldModel:
        if "get_world_model" in self._errors_when_method_is_called:
            raise Exception("get_jobs_model has errored")

        return TotalmobileWorldModel(
            worlds=[World(region=region, id=id) for region, id in self.REGIONS.items()]
        )

    def get_jobs_model(self, world_id: str) -> TotalmobileGetJobsResponseModel:
        if "get_jobs_model" in self._errors_when_method_is_called:
            raise Exception("get_jobs_model has errored")

        if not self._jobs:
            raise Exception

        return TotalmobileGetJobsResponseModel.from_get_jobs_response(
            self._jobs[world_id].values()
        )
