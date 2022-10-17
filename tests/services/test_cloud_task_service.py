from unittest.mock import Mock

import pytest
from google.cloud import tasks_v2

from appconfig import Config
from services.cloud_task_service import CloudTaskService
from models.cloud_tasks.task_request_model import TaskRequestModel
from tests.helpers import config_helper


@pytest.fixture()
def config() -> Config:
    return config_helper.get_default_config()


@pytest.fixture()
def service(config) -> CloudTaskService:
    return CloudTaskService(
        config=config,
        task_queue_id="create_totalmobile_jobs_task_queue_id"
    )


def test_create_task_requests_returns_expected_task_requests_when_given_a_list_of_task_request_models(
    service: CloudTaskService
):
    # arrange
    task_request_models = [TaskRequestModel("task1", b"task1body"), TaskRequestModel("task2", b"task2body")]

    # act
    result = service.create_task_requests(
        task_request_models=task_request_models,
        queue_id="create_totalmobile_jobs_task_queue_id",
        cloud_function_name="cloud_function",
    )

    # assert
    assert result[0].parent == "create_totalmobile_jobs_task_queue_id"
    assert result[0].task.name == "create_totalmobile_jobs_task_queue_id/tasks/task1"
    assert (
        result[0].task.http_request.url
        == "https://region-gcloud_project.cloudfunctions.net/cloud_function"
    )
    assert result[0].task.http_request.body == b"task1body"
    assert (
        result[0].task.http_request.oidc_token.service_account_email
        == "cloud_function_sa"
    )

    assert result[1].parent == "create_totalmobile_jobs_task_queue_id"
    assert result[1].task.name == "create_totalmobile_jobs_task_queue_id/tasks/task2"
    assert (
        result[1].task.http_request.url
        == "https://region-gcloud_project.cloudfunctions.net/cloud_function"
    )
    assert result[1].task.http_request.body == b"task2body"
    assert (
        result[1].task.http_request.oidc_token.service_account_email
        == "cloud_function_sa"
    )


def test_create_tasks_gets_called_once_for_each_task_given_to_it(
        service: CloudTaskService
):
    # arrange
    task_requests = [
        tasks_v2.CreateTaskRequest(parent="qid1", task=tasks_v2.Task()),
        tasks_v2.CreateTaskRequest(parent="qid2", task=tasks_v2.Task()),
    ]
    task_client = Mock()
    task_client.create_task.side_effect = lambda task: f"created {task.parent}"

    # act
    tasks = service.create_tasks(task_requests, task_client)

    # # assert
    assert tasks == ["created qid1", "created qid2"]
