from unittest import mock
from unittest.mock import Mock

from google.cloud import tasks_v2

from appconfig import Config
from cloud_functions.functions import create_tasks, prepare_tasks


@mock.patch.object(Config, "from_env")
def test_prepare_tasks_returns_expected_tasks_when_given_a_list_of_job_models(
    mock_config_from_env,
):
    # arrange
    mock_config_from_env.return_value = Config(
        "totalmobile_url",
        "totalmobile_instance",
        "totalmobile_client_id",
        "totalmobile_client_secret",
        "create_totalmobile_jobs_task_queue_id",
        "gcloud_project",
        "region",
        "rest_api_url",
        "blaise_server_park",
        "cloud_function_sa",
        "bus_api_url",
        "bus_client_id",
    )

    tasks = [("task1", b"task1body"), ("task2", b"task2body")]

    # act
    result = prepare_tasks(
        tasks=tasks,
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


def test_create_tasks_gets_called_once_for_each_task_given_to_it():
    # arrange
    task_requests = [
        tasks_v2.CreateTaskRequest(parent="qid1", task=tasks_v2.Task()),
        tasks_v2.CreateTaskRequest(parent="qid2", task=tasks_v2.Task()),
    ]
    task_client = Mock()
    task_client.create_task.side_effect = lambda task: f"created {task.parent}"

    # act
    tasks = create_tasks(task_requests, task_client)

    # # assert
    assert tasks == ["created qid1", "created qid2"]
