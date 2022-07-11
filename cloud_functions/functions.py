from google.cloud import tasks_v2
from google.protobuf.duration_pb2 import Duration
from datetime import timedelta
from uuid import uuid4
from typing import List

from appconfig import Config
from models.questionnaire_case_task_model import QuestionnaireCaseTaskModel


def create_questionnaire_task_name(job_model: QuestionnaireCaseTaskModel) -> str:
    return (
        f"{job_model.questionnaire}-{str(uuid4())}"
    )


def prepare_questionnaire_tasks(
        job_models: List[QuestionnaireCaseTaskModel],
        queue_id,
        cloud_function_name
) -> List[tasks_v2.CreateTaskRequest]:

    config = Config.from_env()

    duration = Duration()
    duration.FromTimedelta(timedelta(minutes=30))

    task_requests = []
    for job_model in job_models:
        request = tasks_v2.CreateTaskRequest(
            parent=queue_id,
            task=tasks_v2.Task(
                name=f"{queue_id}/tasks/{create_questionnaire_task_name(job_model)}",
                http_request=tasks_v2.HttpRequest(
                    http_method="POST",
                    url=f"https://{config.region}-{config.gcloud_project}.cloudfunctions.net/{cloud_function_name}",
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
