import asyncio
import logging
from datetime import datetime
from typing import List
from uuid import uuid4

from google.cloud import datastore

from appconfig import Config
from cloud_functions.functions import prepare_tasks, run
from cloud_functions.logging import setup_logger
from models.cloud_tasks.questionnaire_case_cloud_task_model import (
    QuestionnaireCaseTaskModel,
)

setup_logger()


def create_questionnaire_case_task_name(job_model: QuestionnaireCaseTaskModel) -> str:
    return (f"{job_model.questionnaire}-{str(uuid4())}")


def map_questionnaire_case_task_models(questionnaires: List[str]) -> List[QuestionnaireCaseTaskModel]:
    return [QuestionnaireCaseTaskModel(questionnaire_name) for questionnaire_name in questionnaires]


def get_questionnaires_with_release_date_of_today() -> list:
    records = get_datastore_records()
    today = datetime.today().strftime("%d/%m/%Y")
    return [record["questionnaire"] for record in records if record["tmreleasedate"].strftime("%d/%m/%Y") == today]


def get_datastore_records() -> list:
    datastore_client = datastore.Client()
    query = datastore_client.query(kind="TmReleaseDate")
    return list(query.fetch())


def check_questionnaire_release_date() -> str:

    logging.info("Checking for questionnaire release dates")

    questionnaires_with_release_date_of_today = get_questionnaires_with_release_date_of_today()

    if questionnaires_with_release_date_of_today == []:
        logging.info("There are no questionnaires with a release date of today")
        return "There are no questionnaires with a release date of today"

    for questionnaire in questionnaires_with_release_date_of_today:
        logging.info(f"Questionnaire {questionnaire} has a release date of today")

    questionnaire_case_task_models = map_questionnaire_case_task_models(
        questionnaires_with_release_date_of_today)

    tasks = [
        (create_questionnaire_case_task_name(job_model), job_model.json().encode())
        for job_model in questionnaire_case_task_models
    ]

    config = Config.from_env()

    questionnaire_task_requests = prepare_tasks(
        tasks=tasks,
        queue_id=config.totalmobile_jobs_queue_id,
        cloud_function_name=config.totalmobile_job_cloud_function
    )

    asyncio.run(run(questionnaire_task_requests))

    return "Done"
