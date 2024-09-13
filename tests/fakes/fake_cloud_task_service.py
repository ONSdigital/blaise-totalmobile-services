from typing import List

from models.common.cloud_tasks.task_request_model import TaskRequestModel


class FakeCloudTaskService:
    def __init__(self):
        self._task_request_models: List[TaskRequestModel] = []
        self._cloud_function = None

    def get_task_request_models(self):
        return self._task_request_models

    def create_and_run_tasks(
        self, task_request_models: List[TaskRequestModel], cloud_function: str
    ) -> None:
        self._task_request_models = task_request_models
        self._cloud_function = cloud_function
