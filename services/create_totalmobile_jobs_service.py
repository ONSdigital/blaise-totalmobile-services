import logging
from typing import List

from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.cloud_tasks.task_request_model import TaskRequestModel
from models.cloud_tasks.totalmobile_create_job_model import TotalmobileCreateJobModel
from models.totalmobile.totalmobile_outgoing_create_job_payload_model import (
    TotalMobileOutgoingCreateJobPayloadModel,
)
from services.cloud_task_service import CloudTaskService
from services.questionnaire_service import QuestionnaireService
from services.totalmobile_service import TotalmobileService
from services.uac_service import UacService


class CreateTotalmobileJobsService:
    def __init__(
        self,
        totalmobile_service: TotalmobileService,
        questionnaire_service: QuestionnaireService,
        uac_service: UacService,
        cloud_task_service: CloudTaskService,
    ):
        self._totalmobile_service = totalmobile_service
        self._questionnaire_service = questionnaire_service
        self._uac_service = uac_service
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

            self.validate_questionnaire_is_in_wave_1(
                questionnaire_name=questionnaire_name
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

        totalmobile_job_models = self.map_totalmobile_job_models(
            cases=eligible_cases,
            questionnaire_name=questionnaire_name,
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

    def map_totalmobile_job_models(
        self,
        questionnaire_name: str,
        cases: List[BlaiseCaseInformationModel],
    ) -> List[TotalmobileCreateJobModel]:
        world_model = self._totalmobile_service.get_world_model()
        questionnaire_uac_model = self._uac_service.get_questionnaire_uac_model(
            questionnaire_name
        )

        job_models = [
            TotalmobileCreateJobModel(
                questionnaire_name,
                world_model.get_world_id(case.field_region),
                case.case_id,
                TotalMobileOutgoingCreateJobPayloadModel.import_case(
                    questionnaire_name,
                    case,
                    questionnaire_uac_model.get_uac_chunks(case.case_id),
                ).to_payload(),
            )
            for case in cases
        ]

        logging.info(
            f"Finished mapping Totalmobile jobs for questionnaire {questionnaire_name}"
        )

        return job_models

    def validate_questionnaire_is_in_wave_1(self, questionnaire_name: str) -> None:
        wave = self._questionnaire_service.get_wave_from_questionnaire_name(
            questionnaire_name
        )
        if wave != "1":
            logging.info(
                f"Questionnaire name {questionnaire_name} does not end with a valid wave, currently only wave 1 is supported"
            )
            raise Exception(
                f"Questionnaire name {questionnaire_name} does not end with a valid wave, currently only wave 1 is supported"
            )
