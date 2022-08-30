import asyncio
from datetime import timedelta
from typing import Any, Coroutine, List, Tuple

from google.cloud import tasks_v2
from google.protobuf.duration_pb2 import Duration

from appconfig import Config


def prepare_tasks(
        tasks: List[Tuple[str, str]],
        queue_id,
        cloud_function_name
) -> List[tasks_v2.CreateTaskRequest]:

    config = Config.from_env()

    duration = Duration()
    duration.FromTimedelta(timedelta(minutes=30))

    task_requests = []
    for task_name, task_body in tasks:
        request = tasks_v2.CreateTaskRequest(
            parent=queue_id,
            task=tasks_v2.Task(
                name=f"{queue_id}/tasks/{task_name}",
                http_request=tasks_v2.HttpRequest(
                    http_method="POST",
                    url=f"https://{config.region}-{config.gcloud_project}.cloudfunctions.net/{cloud_function_name}",
                    body=task_body,
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


def create_tasks(
    task_requests: List[tasks_v2.CreateTaskRequest], task_client
) -> List[Coroutine[Any, Any, tasks_v2.Task]]:
    return [task_client.create_task(request) for request in task_requests]


async def run(task_requests: List[tasks_v2.CreateTaskRequest]) -> None:
    task_client = tasks_v2.CloudTasksAsyncClient()
    await asyncio.gather(*create_tasks(task_requests, task_client))