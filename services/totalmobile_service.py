from typing import List, Protocol, Sequence

import requests

from client.messaging import MessagingClient
from client.optimise import GetJobsResponse, OptimiseClient
from models.blaise.blaise_case_information_base_model import (
    BlaiseCaseInformationBaseModel,
)
from models.cloud_tasks.totalmobile_create_job_model import (
    TotalmobileCreateJobModel,
    TotalmobileCreateJobModelJson,
)
from models.totalmobile.totalmobile_get_jobs_response_model import (
    TotalmobileGetJobsResponseModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from services.mappers.totalmobile_create_job_mapper_service import (
    TotalmobileCreateJobMapperService,
)


class RecallJobError(Exception):
    pass


class DeleteJobError(Exception):
    pass


class TotalmobileService(Protocol):
    def get_world_model(self) -> TotalmobileWorldModel:
        pass

    def create_job(self, job: TotalmobileCreateJobModel) -> requests.Response:
        pass

    def recall_job(
        self, allocated_resource_reference: str, work_type: str, job_reference: str
    ) -> None:
        pass

    def delete_job(
        self, world_id: str, job: str, reason: str = "0"
    ) -> requests.Response:
        pass

    def get_jobs(self, world_id: str) -> GetJobsResponse:
        pass

    def get_jobs_model(self, world_id: str) -> TotalmobileGetJobsResponseModel:
        pass

    def map_totalmobile_create_job_models(
        self, questionnaire_name: str, cases: Sequence[BlaiseCaseInformationBaseModel]
    ) -> List[TotalmobileCreateJobModel]:
        pass

    def map_totalmobile_create_job_from_json(
        self, request_json: TotalmobileCreateJobModelJson
    ):
        pass


class RealTotalmobileService:
    def __init__(
        self,
        optimise_client: OptimiseClient,
        messaging_client: MessagingClient,
        mapper_service: TotalmobileCreateJobMapperService,
    ):
        self._optimise_client = optimise_client
        self._messaging_client = messaging_client
        self._mapper = mapper_service

    def get_world_model(self) -> TotalmobileWorldModel:
        worlds = self._optimise_client.get_worlds()
        return TotalmobileWorldModel.import_worlds(worlds)

    def create_job(self, job: TotalmobileCreateJobModel) -> requests.Response:
        return self._optimise_client.create_job(job.world_id, job.payload)

    def recall_job(
        self, allocated_resource_reference: str, work_type: str, job_reference: str
    ) -> None:
        try:
            response = self._messaging_client.force_recall_visit(
                allocated_resource_reference, work_type, job_reference
            )
        except Exception as error:
            raise RecallJobError("The messaging client raise an error", error)

        if response.status_code != 201:
            raise RecallJobError(
                f"Expected response status of 201, got {response.status_code}"
            )

    def delete_job(
        self, world_id: str, job: str, reason: str = "0"
    ) -> requests.Response:
        try:
            return self._optimise_client.delete_job(world_id, job, reason)
        except Exception as error:
            raise DeleteJobError("The optimise client raise an error", error)

    def get_jobs(self, world_id: str) -> GetJobsResponse:
        return self._optimise_client.get_jobs(world_id)

    def get_jobs_model(self, world_id: str) -> TotalmobileGetJobsResponseModel:
        jobs_response = self.get_jobs(world_id)
        return TotalmobileGetJobsResponseModel.from_get_jobs_response(jobs_response)

    def map_totalmobile_create_job_models(
        self, questionnaire_name: str, cases: Sequence[BlaiseCaseInformationBaseModel]
    ) -> List[TotalmobileCreateJobModel]:
        world_model = self.get_world_model()
        return self._mapper.map_totalmobile_create_job_models(
            questionnaire_name=questionnaire_name, cases=cases, world_model=world_model
        )

    def map_totalmobile_create_job_from_json(
        self, request_json: TotalmobileCreateJobModelJson
    ):
        return self._mapper.map_totalmobile_create_job_model_from_json(request_json)
