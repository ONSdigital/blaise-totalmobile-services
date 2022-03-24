from datetime import timedelta
from typing import Any
from google.cloud import tasks_v2
from google.protobuf.duration_pb2 import Duration
from appconfig import Config
from uuid import uuid4

import json
import asyncio

task_client = tasks_v2.CloudTasksAsyncClient()


def create_task_name(case: Any) -> str:
    return f"{case['instrument']}-{case['case']['qiD.Serial_Number']}-{str(uuid4())}"


async def create_tasks_for_cases(*cases: Any) -> None:
    duration = Duration()
    duration.FromTimedelta(timedelta(minutes=30))

    tasks = []
    for case in cases:
        request = tasks_v2.CreateTaskRequest(
            parent=Config.totalmobile_jobs_queue_id,
            task=tasks_v2.Task(
                name=f"{Config.totalmobile_jobs_queue_id}/tasks/{create_task_name(case)}",
                http_request=tasks_v2.HttpRequest(
                    http_method="POST",
                    url=f"https://{Config.region}-{Config.gcloud_project}.cloudfunctions.net/{Config.totalmobile_job_cloud_function}",
                    body=json.dumps(case).encode(),
                    headers={
                        "Content-Type": "application/json",
                    },
                ),
                dispatch_deadline=duration,
            ),
        )
        task = task_client.create_task(request)
        tasks.append(task)

    await asyncio.gather(*tasks, return_exceptions=True)
