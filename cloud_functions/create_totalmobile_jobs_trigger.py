import logging
from typing import List

from appconfig import Config
from cloud_functions.logging import setup_logger
from cloud_functions.task_provider import TaskProvider
from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.blaise.questionnaire_uac_model import QuestionnaireUacModel
from models.cloud_tasks.task_request_model import TaskRequestModel
from models.cloud_tasks.totalmobile_create_job_model import TotalmobileCreateJobModel
from models.totalmobile.totalmobile_outgoing_create_job_payload_model import (
    TotalMobileOutgoingCreateJobPayloadModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from services.questionnaire_service import QuestionnaireService
from services.totalmobile_service import TotalmobileService
from services.uac_service import UacService

setup_logger()


def map_totalmobile_job_models(
    cases: List[BlaiseCaseInformationModel],
    world_model: TotalmobileWorldModel,
    questionnaire_name: str,
    questionnaire_uac_model: QuestionnaireUacModel,
) -> List[TotalmobileCreateJobModel]:
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


def validate_questionnaire_is_in_wave_1(
    questionnaire_name: str,
    questionnaire_service: QuestionnaireService,
) -> None:
    wave = questionnaire_service.get_wave_from_questionnaire_name(questionnaire_name)
    if wave != "1":
        logging.info(
            f"Questionnaire name {questionnaire_name} does not end with a valid wave, currently only wave 1 is supported"
        )
        raise Exception(
            f"Questionnaire name {questionnaire_name} does not end with a valid wave, currently only wave 1 is supported"
        )


def create_cloud_tasks_for_jobs(
    questionnaire_name: str,
    config: Config,
    totalmobile_job_models: List[TotalmobileCreateJobModel],
    task_provider: TaskProvider
) -> str:
    task_request_models = [
        TaskRequestModel(task_name=job_model.create_task_name(), task_body=job_model.json().encode())
        for job_model in totalmobile_job_models
    ]
    logging.info(
        f"Creating {len(task_request_models)} task request models for questionnaire {questionnaire_name}"
    )

    task_provider.create_and_run_tasks(
        task_request_models=task_request_models,
        queue_id=config.create_totalmobile_jobs_task_queue_id,
        cloud_function="bts-create-totalmobile-jobs-processor",
    )
    logging.info(
        f"Finished creating cloud tasks for questionnaire {questionnaire_name}"
    )

    return "Done"


def create_totalmobile_jobs_for_eligible_questionnaire_cases(
    questionnaire_name: str,
    config: Config,
    world_model: TotalmobileWorldModel,
    questionnaire_service: QuestionnaireService,
    uac_service: UacService,
    task_provider: TaskProvider
) -> str:

    eligible_cases = questionnaire_service.get_eligible_cases(questionnaire_name)

    if len(eligible_cases) == 0:
        logging.info(
            f"Exiting as no eligible cases to send for questionnaire {questionnaire_name}"
        )
        return f"Exiting as no eligible cases to send for questionnaire {questionnaire_name}"

    logging.info(
        f"Found {len(eligible_cases)} eligible cases for questionnaire {questionnaire_name}"
    )

    questionnaire_uac_model = uac_service.get_questionnaire_uac_model(
        questionnaire_name
    )

    totalmobile_job_models = map_totalmobile_job_models(
        cases=eligible_cases,
        world_model=world_model,
        questionnaire_name=questionnaire_name,
        questionnaire_uac_model=questionnaire_uac_model,
    )

    return create_cloud_tasks_for_jobs(
        questionnaire_name=questionnaire_name,
        config=config,
        totalmobile_job_models=totalmobile_job_models,
        task_provider=task_provider
    )


def create_totalmobile_jobs_trigger(
    config: Config,
    totalmobile_service: TotalmobileService,
    questionnaire_service: QuestionnaireService,
    uac_service: UacService,
    task_provider: TaskProvider
) -> str:
    logging.info("Checking for questionnaire release dates")

    questionnaires_with_release_date_of_today = (
        questionnaire_service.get_questionnaires_with_totalmobile_release_date_of_today()
    )

    if not questionnaires_with_release_date_of_today:
        logging.info("There are no questionnaires with a release date of today")
        return "There are no questionnaires with a release date of today"

    world_model = totalmobile_service.get_world_model()

    for questionnaire_name in questionnaires_with_release_date_of_today:
        logging.info(f"Questionnaire {questionnaire_name} has a release date of today")

        validate_questionnaire_is_in_wave_1(
            questionnaire_name=questionnaire_name,
            questionnaire_service=questionnaire_service,
        )

        create_totalmobile_jobs_for_eligible_questionnaire_cases(
            questionnaire_name=questionnaire_name,
            config=config,
            world_model=world_model,
            questionnaire_service=questionnaire_service,
            uac_service=uac_service,
            task_provider=task_provider
        )

    return "Done"
