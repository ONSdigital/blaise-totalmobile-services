import asyncio
import logging

from google.cloud import datastore, tasks_v2
from datetime import datetime
from typing import List, Coroutine, Any
from cloud_functions.logging import setup_logger
from cloud_functions.functions import prepare_tasks
from models.questionnaire_case_task_model import QuestionnaireCaseTaskModel
from appconfig import Config
from uuid import uuid4


setup_logger()


def create_questionnaire_task_name(job_model: QuestionnaireCaseTaskModel) -> str:
    return (
        f"{job_model.questionnaire}-{str(uuid4())}"
    )


def create_tasks(
        task_requests: List[tasks_v2.CreateTaskRequest], task_client
) -> List[Coroutine[Any, Any, tasks_v2.Task]]:
    return [task_client.create_task(request) for request in task_requests]


async def run(task_requests: List[tasks_v2.CreateTaskRequest]) -> None:
    task_client = tasks_v2.CloudTasksAsyncClient()
    await asyncio.gather(*create_tasks(task_requests, task_client))


def map_questionnaire_case_task_models(questionnaires: List[str]) -> List[QuestionnaireCaseTaskModel]:
    return [QuestionnaireCaseTaskModel(questionnaire_name) for questionnaire_name in questionnaires]


def get_questionnaires_with_todays_release_date() -> list:
    records = get_datastore_records()
    today = datetime.today().strftime("%d/%m/%Y")
    return [record["questionnaire"] for record in records if record["tmreleasedate"].strftime("%d/%m/%Y") == today]


def get_datastore_records() -> list:
    datastore_client = datastore.Client()
    query = datastore_client.query(kind="TmReleaseDate")
    return list(query.fetch())


def check_questionnaire_release_date() -> str:
    logging.info("Started checking questionnaire release dates")

    todays_questionnaires_for_release = get_questionnaires_with_todays_release_date()
    if todays_questionnaires_for_release == []:
        logging.info("There are no questionnaires for release today")
        return "There are no questionnaires for release today"

    questionnaire_case_task_models = map_questionnaire_case_task_models(
        todays_questionnaires_for_release)

    tasks = [
        (create_questionnaire_task_name(job_model), job_model.json().encode())
        for job_model in questionnaire_case_task_models
    ]

    config = Config.from_env()
    questionnaire_task_requests = prepare_tasks(
        tasks=tasks,
        queue_id=config.totalmobile_jobs_queue_id,
        cloud_function_name=config.totalmobile_job_cloud_function
    )

    asyncio.run(run(questionnaire_task_requests))
    logging.info("Finished checking questionnaire release dates")
    return "Done"
