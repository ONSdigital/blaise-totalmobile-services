import logging
from typing import List, Sequence

import requests

from client.optimise import GetJobsResponse
from models.common.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from models.create.blaise.blaise_create_case_model import BlaiseCreateCaseModelBase
from models.create.totalmobile.totalmobile_create_job_model import (
    TotalmobileCreateJobModel,
    TotalmobileCreateJobModelRequestJson,
)
from models.delete.totalmobile_get_jobs_response_model import (
    TotalmobileGetJobsResponseModel,
)
from services.totalmobile_service import TotalmobileService


class LoggingTotalmobileService:
    def __init__(self, service: TotalmobileService):
        self._service = service

    def get_world_model(self) -> TotalmobileWorldModel:
        return self._service.get_world_model()

    def create_job(self, job: TotalmobileCreateJobModel) -> requests.Response:
        return self._service.create_job(job)

    def recall_job(
        self, allocated_resource_reference: str, work_type: str, job_reference: str
    ) -> None:
        try:
            self._service.recall_job(
                allocated_resource_reference, work_type, job_reference
            )
            logging.info(
                f"Successfully recalled job {job_reference} from {allocated_resource_reference} on Totalmobile"
            )
        except Exception as error:
            logging.error(
                f"Failed to recall job {job_reference} from {allocated_resource_reference} on Totalmobile",
                extra={"json_fields": {"previous_exception": str(error)}},
            )
            raise error

    def delete_job(
        self, world_id: str, job: str, reason: str = "0"
    ) -> requests.Response:
        try:
            result = self._service.delete_job(world_id, job, reason)
            logging.info(f"Successfully removed job {job} from Totalmobile")
            return result
        except Exception as error:
            logging.error(
                f"Unable to delete job reference '{job}` from Totalmobile",
                extra={"Exception_reason": str(error)},
            )
            raise error

    def get_jobs(self, world_id: str) -> GetJobsResponse:
        return self._service.get_jobs(world_id)

    def get_jobs_model(self, world_id: str) -> TotalmobileGetJobsResponseModel:
        model = self._service.get_jobs_model(world_id)
        logging.info(
            f"Found {model.total_number_of_incomplete_jobs()} incomplete jobs in totalmobile for world {world_id}"
        )
        return model

    def map_totalmobile_create_job_models(
        self, questionnaire_name: str, cases: Sequence[BlaiseCreateCaseModelBase]
    ) -> List[TotalmobileCreateJobModel]:
        return self._service.map_totalmobile_create_job_models(
            questionnaire_name, cases
        )

    def map_totalmobile_create_job_from_json(
        self, request_json: TotalmobileCreateJobModelRequestJson
    ):
        return self._service.map_totalmobile_create_job_from_json(request_json)
