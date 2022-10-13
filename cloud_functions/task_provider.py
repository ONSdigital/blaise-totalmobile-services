import asyncio
from datetime import timedelta
from typing import Any, Coroutine, List

from google.cloud import tasks_v2
from google.protobuf.duration_pb2 import Duration

from appconfig import Config
from models.cloud_tasks.task_request_model import TaskRequestModel


class TaskProvider:
    def __init__(self, config: Config):
        self.config = config

    def create_and_run_tasks(self, task_request_models: List[TaskRequestModel], queue_id: str, cloud_function: str):
        task_requests = self._create_task_requests(
            task_request_models=task_request_models, queue_id=queue_id, cloud_function_name=cloud_function
        )

        asyncio.run(self._run_tasks(task_requests))

    def _create_task_requests(self, task_request_models: List[TaskRequestModel], queue_id, cloud_function_name
                              ) -> List[tasks_v2.CreateTaskRequest]:
        duration = Duration()
        duration.FromTimedelta(timedelta(minutes=30))

        task_requests = []
        for task_request_model in task_request_models:
            request = tasks_v2.CreateTaskRequest(
                parent=queue_id,
                task=tasks_v2.Task(
                    name=f"{queue_id}/tasks/{task_request_model.task_name}",
                    http_request=tasks_v2.HttpRequest(
                        http_method="POST",
                        url=f"https://{self.config.region}-{self.config.gcloud_project}.cloudfunctions.net/{cloud_function_name}",
                        body=task_request_model.task_body,
                        headers={
                            "Content-Type": "application/json",
                        },
                        oidc_token={"service_account_email": self.config.cloud_function_sa},
                    ),
                    dispatch_deadline=duration,
                ),
            )
            task_requests.append(request)
        return task_requests

    @staticmethod
    def _create_tasks(task_requests: List[tasks_v2.CreateTaskRequest], task_client
                      ) -> List[Coroutine[Any, Any, tasks_v2.Task]]:
        return [task_client.create_task(request) for request in task_requests]

    async def _run_tasks(self, task_requests: List[tasks_v2.CreateTaskRequest]) -> None:
        task_client = tasks_v2.CloudTasksAsyncClient()
        await asyncio.gather(*self._create_tasks(task_requests, task_client))
