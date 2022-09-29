import asyncio
import logging
from datetime import datetime
from typing import List, Tuple

from google.cloud import datastore

from appconfig import Config
from cloud_functions.functions import prepare_tasks, run
from cloud_functions.logging import setup_logger
from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.cloud_tasks.totalmobile_create_job_model import TotalmobileCreateJobModel
from models.totalmobile.totalmobile_outgoing_create_job_payload_model import (
    TotalMobileOutgoingCreateJobPayloadModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from services.questionnaire_service import QuestionnaireService
from services.totalmobile_service import TotalmobileService

setup_logger()


def map_totalmobile_job_models(
    cases: List[BlaiseCaseInformationModel],
    world_model: TotalmobileWorldModel,
    questionnaire_name: str,
) -> List[TotalmobileCreateJobModel]:
    return [
        TotalmobileCreateJobModel(
            questionnaire_name,
            world_model.get_world_id(case.field_region),
            case.case_id,
            TotalMobileOutgoingCreateJobPayloadModel.import_case(
                questionnaire_name, case
            ).to_payload(),
        )
        for case in cases
    ]


def run_async_tasks(tasks: List[Tuple[str, bytes]], queue_id: str, cloud_function: str):
    task_requests = prepare_tasks(
        tasks=tasks, queue_id=queue_id, cloud_function_name=cloud_function
    )

    asyncio.run(run(task_requests))


def create_cloud_tasks(
    questionnaire_name: str,
    config: Config,
    totalmobile_service: TotalmobileService,
    questionnaire_service: QuestionnaireService,
) -> str:
    wave = questionnaire_service.get_wave_from_questionnaire_name(questionnaire_name)
    if wave != "1":
        logging.info(
            f"Questionnaire name {questionnaire_name} does not end with a valid wave, currently only wave 1 is supported"
        )
        raise Exception(
            f"Questionnaire name {questionnaire_name} does not end with a valid wave, currently only wave 1 is supported"
        )

    logging.info(f"Creating case tasks for questionnaire {questionnaire_name}")

    eligible_cases = questionnaire_service.get_eligible_cases(questionnaire_name)

    if len(eligible_cases) == 0:
        logging.info(
            f"Exiting as no eligible cases to send for questionnaire {questionnaire_name}"
        )
        return f"Exiting as no eligible cases to send for questionnaire {questionnaire_name}"

    logging.info(
        f"Found {len(eligible_cases)} eligible cases for questionnaire {questionnaire_name}"
    )

    world_model = totalmobile_service.get_world_model()

    totalmobile_job_models = map_totalmobile_job_models(
        eligible_cases, world_model, questionnaire_name
    )
    logging.info(
        f"Finished mapping Totalmobile jobs for questionnaire {questionnaire_name}"
    )

    tasks = [
        (job_model.create_task_name(), job_model.json().encode())
        for job_model in totalmobile_job_models
    ]
    logging.info(
        f"Creating {len(tasks)} cloud tasks for questionnaire {questionnaire_name}"
    )

    run_async_tasks(
        tasks=tasks,
        queue_id=config.create_totalmobile_jobs_task_queue_id,
        cloud_function="bts-create-totalmobile-jobs-processor",
    )
    logging.info(
        f"Finished creating cloud tasks for questionnaire {questionnaire_name}"
    )
    return "Done"


def create_totalmobile_jobs_trigger(
    config: Config,
    totalmobile_service: TotalmobileService,
    questionnaire_service: QuestionnaireService,
) -> str:
    logging.info("Checking for questionnaire release dates")

    questionnaires_with_release_date_of_today = (
        questionnaire_service.get_questionnaires_with_totalmobile_release_date_of_today()
    )

    if not questionnaires_with_release_date_of_today:
        logging.info("There are no questionnaires with a release date of today")
        return "There are no questionnaires with a release date of today"

    for questionnaire_name in questionnaires_with_release_date_of_today:
        logging.info(f"Questionnaire {questionnaire_name} has a release date of today")
        create_cloud_tasks(
            questionnaire_name, config, totalmobile_service, questionnaire_service
        )

    return "Done"
