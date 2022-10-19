import logging
from typing import Dict, List

from models.totalmobile.totalmobile_get_jobs_response_model import Job
from services.blaise_service import BlaiseService
from services.logging_totalmobile_service import LoggingTotalmobileService
from services.totalmobile_service import ITotalmobileService, RecallJobError


class DeleteTotalmobileJobsService:
    CASE_OUTCOMES_WHOSE_JOBS_SHOULD_NOT_BE_DELETED = [0, 120, 310, 320]

    def __init__(
        self,
        totalmobile_service: ITotalmobileService,
        blaise_service: BlaiseService,
    ):
        self._totalmobile_service = LoggingTotalmobileService(totalmobile_service)
        self._blaise_service = blaise_service

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
        blaise_case_outcomes = self._get_blaise_case_outcomes_for_questionnaire(
            questionnaire_name
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
                self._recall_job(job)
                self._delete_job(world_id, job.reference, "past field period")

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

        self._recall_and_delete_job(job, world_id)

    def _get_blaise_case_outcomes_for_questionnaire(
        self, questionnaire_name: str
    ) -> Dict[str, int]:
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

    def _get_incomplete_jobs_from_totalmobile(
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

    def _recall_and_delete_job(self, job, world_id):
        self._recall_job(job)
        self._delete_job(world_id, job.reference, "completed in blaise")

    def _recall_job(self, job: Job):
        if not job.allocated_resource_reference:
            return

        try:
            self._totalmobile_service.recall_job(
                job.allocated_resource_reference, job.work_type, job.reference
            )
            logging.info(
                f"Successfully recalled job {job.reference} from {job.allocated_resource_reference} on Totalmobile"
            )
        except RecallJobError:
            pass  # Swallow the exception and continue to the next job

    def _delete_job(self, world_id: str, job_reference: str, reason: str):
        try:
            self._totalmobile_service.delete_job(world_id, job_reference, reason)
        except Exception:
            pass  # Swallow the exception and continue to the next job
