import logging
from typing import Dict, List, Optional

from models.totalmobile.totalmobile_get_jobs_response_model import Job
from services.blaise_service import BlaiseService
from services.totalmobile_service import TotalmobileService


class DeleteTotalmobileJobsService:
    def __init__(
        self,
        totalmobile_service: TotalmobileService,
        blaise_service: BlaiseService,
        incomplete_job_outcomes=[0, 120, 310, 320],
    ):
        self.totalmobile_service = totalmobile_service
        self.blaise_service = blaise_service
        self._delete_reason = "completed in blaise"
        self.incomplete_job_outcomes = incomplete_job_outcomes

    def delete_totalmobile_jobs_completed_in_blaise(self) -> None:
        world_id = self.get_world_id()

        for (
            questionnaire_name,
            jobs,
        ) in self.get_questionnaires_with_incomplete_jobs_by_world(world_id).items():
            self.delete_jobs_for_questionnaire(questionnaire_name, jobs, world_id)

    def delete_jobs_for_questionnaire(self, questionnaire_name, jobs, world_id):
        blaise_cases_with_outcomes_dict = self.get_blaise_case_outcomes(
            questionnaire_name
        )

        for job in jobs:
            self.delete_job_if_completed(
                job, questionnaire_name, world_id, blaise_cases_with_outcomes_dict
            )

    def delete_job_if_completed(
        self, job, questionnaire_name, world_id, blaise_cases_with_outcomes_dict
    ):
        if job.case_id not in blaise_cases_with_outcomes_dict:
            logging.error(
                f"Unable to find case {job.case_id} for questionnaire {questionnaire_name} in Blaise"
            )
            return

        if (
            job.visit_complete
            or blaise_cases_with_outcomes_dict[job.case_id]
            in self.incomplete_job_outcomes
        ):
            return

        self.delete_job(world_id, job.reference)

    def get_blaise_case_outcomes(self, questionnaire_name) -> Dict[Optional[str], int]:
        try:
            cases = self.blaise_service.get_cases(questionnaire_name)
            return {case.case_id: case.outcome_code for case in cases}
        except Exception as error:
            logging.error(
                "Unable to retrieve cases from Blaise",
                extra={"Exception_reason": str(error)},
            )
            return {}

    def get_world_id(self):
        world_model = self.totalmobile_service.get_world_model()
        for world in world_model.worlds:
            if world.region == "Region 1":
                return world.id

    def get_questionnaires_with_incomplete_jobs_by_world(
        self, world_id: str
    ) -> Dict[str, List[Job]]:
        try:
            jobs_model = self.totalmobile_service.get_jobs_model(world_id)
            return jobs_model.questionnaires_with_incomplete_jobs()
        except Exception as error:
            logging.error(
                "Unable to retrieve jobs from Totalmobile",
                extra={"Exception_reason": str(error)},
            )
            return {}

    def delete_job(self, world_id: str, job_reference: str):
        try:
            self.totalmobile_service.delete_job(
                world_id, job_reference, self._delete_reason
            )
            logging.info(f"Successfully removed job {job_reference} from Totalmobile")
        except Exception as error:
            logging.error(
                f"Unable to delete job reference '{job_reference}` from Totalmobile",
                extra={"Exception_reason": str(error)},
            )
