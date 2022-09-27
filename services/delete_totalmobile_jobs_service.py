import logging
from typing import Dict, List

from models.totalmobile.totalmobile_get_jobs_response_model import Job
from services.blaise_service import BlaiseService
from services.totalmobile_service import TotalmobileService


class DeleteTotalmobileJobsService:
    CASE_OUTCOMES_WHOSE_JOBS_SHOULD_NOT_BE_DELETED = [0, 120, 310, 320]

    def __init__(
        self,
        totalmobile_service: TotalmobileService,
        blaise_service: BlaiseService,
    ):
        self._totalmobile_service = totalmobile_service
        self._blaise_service = blaise_service
        self._delete_reason = "completed in blaise"

    def delete_totalmobile_jobs_completed_in_blaise(self) -> None:
        world_ids = self._get_world_ids()
        for world_id in world_ids:
            for (
                questionnaire_name,
                jobs,
            ) in self._get_questionnaires_with_incomplete_jobs(world_id).items():
                self._delete_jobs_for_questionnaire(questionnaire_name, jobs, world_id)

    def _delete_jobs_for_questionnaire(
        self, questionnaire_name: str, jobs: List[Job], world_id: str
    ):
        blaise_case_outcomes = self._get_blaise_case_outcomes(questionnaire_name)

        for job in jobs:
            self._delete_job_if_completed(
                job, questionnaire_name, world_id, blaise_case_outcomes
            )

    def _delete_job_if_completed(
        self,
        job: Job,
        questionnaire_name: str,
        world_id: str,
        blaise_case_outcomes: Dict[str, int],
    ):
        if job.case_id not in blaise_case_outcomes:
            logging.error(
                f"Unable to find case {job.case_id} for "
                f"questionnaire {questionnaire_name} in Blaise"
            )
            return

        blaise_cases_to_remain = (
            blaise_case_outcomes[job.case_id]
            in self.CASE_OUTCOMES_WHOSE_JOBS_SHOULD_NOT_BE_DELETED
        )

        if job.visit_complete or blaise_cases_to_remain:
            return

        self._delete_job(world_id, job.reference)

    def _get_blaise_case_outcomes(self, questionnaire_name: str) -> Dict[str, int]:
        try:
            cases = self._blaise_service.get_cases(questionnaire_name)
            return {str(case.case_id): case.outcome_code for case in cases}
        except Exception as error:
            logging.error(
                "Unable to retrieve cases from Blaise",
                extra={"Exception_reason": str(error)},
            )
            return {}

    def _get_world_ids(self):
        world_model = self._totalmobile_service.get_world_model()
        return world_model.get_available_ids()

    def _get_questionnaires_with_incomplete_jobs(
        self, world_id: str
    ) -> Dict[str, List[Job]]:
        try:
            jobs_model = self._totalmobile_service.get_jobs_model(world_id)
            return jobs_model.questionnaires_with_incomplete_jobs()
        except Exception as error:
            logging.error(
                "Unable to retrieve jobs from Totalmobile",
                extra={"Exception_reason": str(error)},
            )
            return {}

    def _delete_job(self, world_id: str, job_reference: str):
        try:
            self._totalmobile_service.delete_job(
                world_id, job_reference, self._delete_reason
            )
            logging.info(f"Successfully removed job {job_reference} from Totalmobile")
        except Exception as error:
            logging.error(
                f"Unable to delete job reference '{job_reference}` from Totalmobile",
                extra={"Exception_reason": str(error)},
            )
