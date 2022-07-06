import flask
import json
import asyncio

from google.cloud import datastore, tasks_v2
from datetime import datetime
from dataclasses import asdict, dataclass
from typing import Dict, List, Coroutine, Any
from google.protobuf.duration_pb2 import Duration
from datetime import timedelta
from uuid import uuid4

from appconfig import Config


@dataclass
class QuestionnaireCaseTaskModel:
    questionnaire: str

    def as_dict(self) -> Dict:
        return asdict(self)

    def json(self) -> str:
        return json.dumps(self.as_dict())


def create_tasks(
        task_requests: List[tasks_v2.CreateTaskRequest], task_client
) -> List[Coroutine[Any, Any, tasks_v2.Task]]:
    return [task_client.create_task(request) for request in task_requests]


async def run(task_requests: List[tasks_v2.CreateTaskRequest]) -> None:
    task_client = tasks_v2.CloudTasksAsyncClient()
    await asyncio.gather(*create_tasks(task_requests, task_client))


def create_questionnaire_task_name(job_model: QuestionnaireCaseTaskModel) -> str:
    return (
        f"{job_model.questionnaire}-{str(uuid4())}"
    )


def prepare_questionnaire_tasks(
        job_models: List[QuestionnaireCaseTaskModel],
) -> List[tasks_v2.CreateTaskRequest]:

    config = Config.from_env()

    duration = Duration()
    duration.FromTimedelta(timedelta(minutes=30))

    task_requests = []
    for job_model in job_models:
        request = tasks_v2.CreateTaskRequest(
            parent=config.totalmobile_jobs_queue_id,
            task=tasks_v2.Task(
                name=f"{config.totalmobile_jobs_queue_id}/tasks/{create_questionnaire_task_name(job_model)}",
                http_request=tasks_v2.HttpRequest(
                    http_method="POST",
                    url=f"https://{config.region}-{config.gcloud_project}.cloudfunctions.net/{config.totalmobile_job_cloud_function}",
                    body=job_model.json().encode(),
                    headers={
                        "Content-Type": "application/json",
                    },
                    oidc_token={"service_account_email": config.cloud_function_sa},
                ),
                dispatch_deadline=duration,
            ),
        )
        task_requests.append(request)
    return task_requests


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
    todays_questionnaires_for_release = get_questionnaires_with_todays_release_date()
    if todays_questionnaires_for_release == []:
        return "There are no questionnaires for release today"

    questionnaire_case_task_models = map_questionnaire_case_task_models(
        todays_questionnaires_for_release)

    questionnaire_task_requests = prepare_questionnaire_tasks(questionnaire_case_task_models)

    asyncio.run(run(questionnaire_task_requests))
    return "Done"
