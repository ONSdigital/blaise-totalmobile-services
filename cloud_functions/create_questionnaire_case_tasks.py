from datetime import timedelta
from typing import List
from google.protobuf.duration_pb2 import Duration
from appconfig import Config
from uuid import uuid4
from models.totalmobile_job_model import TotalmobileJobModel
from google.cloud import tasks_v2

import json


def create_task_name(job_model: TotalmobileJobModel) -> str:
    return f"{job_model.questionnaire_name}-{job_model.case_data['qiD.Serial_Number']}-{str(uuid4())}"


def prepare_tasks(*job_models: TotalmobileJobModel) -> List[tasks_v2.CreateTaskRequest]:
    config = Config.from_env()

    duration = Duration()
    duration.FromTimedelta(timedelta(minutes=30))

    task_requests = []
    for job_model in job_models:
        request = tasks_v2.CreateTaskRequest(
            parent=config.totalmobile_jobs_queue_id,
            task=tasks_v2.Task(
                name=f"{config.totalmobile_jobs_queue_id}/tasks/{create_task_name(job_model)}",
                http_request=tasks_v2.HttpRequest(
                    http_method="POST",
                    url=f"https://{config.region}-{config.gcloud_project}.cloudfunctions.net/{config.totalmobile_job_cloud_function}",
                    body=json.dumps(job_model.case_data).encode(),
                    headers={
                        "Content-Type": "application/json",
                    },
                ),
                dispatch_deadline=duration,
            ),
        )
        task_requests.append(request)
    return task_requests

