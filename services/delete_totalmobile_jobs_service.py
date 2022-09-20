import logging
from typing import List, Optional

from models.totalmobile.totalmobile_get_jobs_response_model import (
    TotalmobileGetJobsResponseModel,
)
from services.blaise_service import BlaiseService
from services.totalmobile_service import TotalmobileService


class DeleteTotalmobileJobsService:
    def __init__(
        self, totalmobile_service: TotalmobileService, blaise_service: BlaiseService
    ):
        self.totalmobile_service = totalmobile_service
        self.blaise_service = blaise_service
        self._delete_reason = "completed in blaise"

    def delete_totalmobile_jobs_completed_in_blaise(self) -> None:
        world_id = self.get_world_id()
        totalmobile_jobs_model = self.get_jobs_model(world_id)
        if not totalmobile_jobs_model:
            return

        for questionnaire_name in totalmobile_jobs_model.questionnaire_jobs.keys():
            if self.questionnaire_has_incomplete_cases(
                questionnaire_name, totalmobile_jobs_model
            ):
                continue

            completed_case_ids = self.get_completed_blaise_cases(questionnaire_name)
            if not completed_case_ids:
                continue

            for job in totalmobile_jobs_model.questionnaire_jobs[questionnaire_name]:
                if job.visit_complete:
                    continue

                if job.case_id not in completed_case_ids:
                    logging.error(
                        f"Unable to find case {job.case_id} for questionnaire {questionnaire_name} in Blaise"
                    )
                    continue

                self.delete_job(world_id, job.reference)

    def get_completed_blaise_cases(self, questionnaire_name) -> List[Optional[str]]:
        try:
            cases = self.blaise_service.get_cases(questionnaire_name)
            return [case.case_id for case in cases if case.outcome_code == 110]
        except:
            logging.error("Unable to retrieve cases from Blaise")
            return []

    @staticmethod
    def questionnaire_has_incomplete_cases(
        questionnaire_name: str, totalmobile_jobs_model: TotalmobileGetJobsResponseModel
    ) -> bool:
        return all(
            job.visit_complete
            for job in totalmobile_jobs_model.questionnaire_jobs[questionnaire_name]
        )

    def get_world_id(self):
        world_model = self.totalmobile_service.get_world_model()
        for world in world_model.worlds:
            if world.region == "Region 1":
                return world.id

    def get_jobs_model(
        self, world_id: str
    ) -> Optional[TotalmobileGetJobsResponseModel]:
        try:
            return self.totalmobile_service.get_jobs_model(world_id)
        except:
            logging.error("Unable to retrieve jobs from Totalmobile")
            return None

    def delete_job(self, world_id: str, job_reference: str):
        try:
            self.totalmobile_service.delete_job(
                world_id, job_reference, self._delete_reason
            )
            logging.info(f"Successfully removed job {job_reference} from Totalmobile")
        except:
            logging.error(
                f"Unable to delete job reference '{job_reference}` from Totalmobile"
            )
