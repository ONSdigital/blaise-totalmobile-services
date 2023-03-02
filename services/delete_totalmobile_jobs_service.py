import logging
from typing import Dict, List

from models.totalmobile.totalmobile_get_jobs_response_model import Job
from services.blaise_case_outcome_service import BlaiseCaseOutcomeService
from services.delete_totalmobile_job_service import DeleteTotalmobileJobService
from services.totalmobile_service import TotalmobileService


class DeleteTotalmobileJobsService:
    CASE_OUTCOMES_WHOSE_JOBS_SHOULD_NOT_BE_DELETED = [0, 120, 310, 320]

    def __init__(
        self,
        totalmobile_service: TotalmobileService,
        blaise_outcome_service: BlaiseCaseOutcomeService,
        delete_totalmobile_job_service: DeleteTotalmobileJobService,
    ):
        self._totalmobile_service = totalmobile_service
        self._blaise_outcome_service = blaise_outcome_service
        self._delete_job_service = delete_totalmobile_job_service

    def delete_jobs_for_completed_cases(self) -> None:
        world_ids = self._get_world_ids()
        for world_id in world_ids:
            for (
                questionnaire_name,
                jobs,
            ) in self._get_incomplete_jobs_from_totalmobile(world_id).items():
                self._delete_jobs_for_completed_cases_by_questionnaire(
                    questionnaire_name, jobs, world_id
                )

    def delete_jobs_past_field_period(self) -> None:
        world_ids = self._get_world_ids()
        for world_id in world_ids:
            for jobs in self._get_incomplete_jobs_from_totalmobile(world_id).values():
                self._delete_jobs_past_field_period(jobs, world_id)

    def _delete_jobs_for_completed_cases_by_questionnaire(
        self, questionnaire_name: str, jobs: List[Job], world_id: str
    ):
        blaise_case_outcomes = (
            self._blaise_outcome_service.get_case_outcomes_for_questionnaire(
                questionnaire_name
            )
        )

        if not blaise_case_outcomes:
            return

        for job in jobs:
            self._delete_job_if_no_longer_required(
                job, questionnaire_name, world_id, blaise_case_outcomes
            )

    def _delete_jobs_past_field_period(self, jobs: List[Job], world_id: str):
        for job in jobs:
            logging.info(
                f"job with case ID {job.case_id} has past field period value of {job.past_field_period}"
            )
            if job.past_field_period:
                self._delete_job_service.delete_job(world_id, job, "past field period")

    def _delete_job_if_no_longer_required(
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

        self._delete_job_service.delete_job(world_id, job, "completed in blaise")

    def _get_world_ids(self):
        world_model = self._totalmobile_service.get_world_model()
        return world_model.get_available_ids()

    def _get_incomplete_jobs_from_totalmobile(
        self, world_id: str
    ) -> Dict[str, List[Job]]:
        try:
            jobs_model = self._totalmobile_service.get_jobs_model(world_id)

            return jobs_model.questionnaires_with_incomplete_jobs()
        except Exception as error:
            logging.error(
                "Unable to retrieve jobs from Totalmobile",
                extra={"json_fields": {"Exception_reason": str(error)}},
            )
            return {}
