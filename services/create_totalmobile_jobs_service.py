import logging
from typing import List
from models.cloud_tasks.task_request_model import TaskRequestModel
from models.cloud_tasks.totalmobile_create_job_model import TotalmobileCreateJobModel
from services.cloud_task_service import CloudTaskService
from services.questionnaire_service_base import QuestionnaireServiceBase
from services.totalmobile_service import TotalmobileService

class CreateTotalmobileJobsService:
    def __init__(
        self,
        totalmobile_service: TotalmobileService,
        questionnaire_service: QuestionnaireServiceBase,
        cloud_task_service: CloudTaskService,
    ):
        self._totalmobile_service = totalmobile_service
        self._questionnaire_service = questionnaire_service
        self._cloud_task_service = cloud_task_service

    def create_totalmobile_jobs(self) -> str:
        logging.info("Checking for questionnaire release dates")

        questionnaires_with_release_date_of_today = (
            self._questionnaire_service.get_questionnaires_with_totalmobile_release_date_of_today()
        )

        if not questionnaires_with_release_date_of_today:
            logging.info("There are no questionnaires with a release date of today")
            return "There are no questionnaires with a release date of today"

        for questionnaire_name in questionnaires_with_release_date_of_today:
            logging.info(
                f"Questionnaire {questionnaire_name} has a release date of today"
            )

            self.create_totalmobile_jobs_for_eligible_questionnaire_cases(
                questionnaire_name=questionnaire_name
            )

        return "Done"

    def create_totalmobile_jobs_for_eligible_questionnaire_cases(
        self, questionnaire_name: str
    ) -> str:

        eligible_cases = self._questionnaire_service.get_eligible_cases(
            questionnaire_name
        )

        if len(eligible_cases) == 0:
            logging.info(
                f"Exiting as no eligible cases to send for questionnaire {questionnaire_name}"
            )
            return f"Exiting as no eligible cases to send for questionnaire {questionnaire_name}"

        logging.info(
            f"Found {len(eligible_cases)} eligible cases for questionnaire {questionnaire_name}"
        )

        totalmobile_job_models = self._totalmobile_service.map_totalmobile_Create_job_models(
            cases=eligible_cases,
            questionnaire_name=questionnaire_name
        )

        return self.create_cloud_tasks_for_jobs(
            questionnaire_name=questionnaire_name,
            totalmobile_job_models=totalmobile_job_models,
        )

    def create_cloud_tasks_for_jobs(
        self,
        questionnaire_name: str,
        totalmobile_job_models: List[TotalmobileCreateJobModel],
    ) -> str:
        task_request_models = [
            TaskRequestModel(
                task_name=job_model.create_task_name(),
                task_body=job_model.json().encode(),
            )
            for job_model in totalmobile_job_models
        ]
        logging.info(
            f"Creating {len(task_request_models)} task request models for questionnaire {questionnaire_name}"
        )

        self._cloud_task_service.create_and_run_tasks(
            task_request_models=task_request_models,
            cloud_function="bts-create-totalmobile-jobs-processor",
        )
        logging.info(
            f"Finished creating cloud tasks for questionnaire {questionnaire_name}"
        )

        return "Done"
