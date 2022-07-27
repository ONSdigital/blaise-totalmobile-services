from unittest import mock

from google.cloud import tasks_v2

from appconfig import Config
from cloud_functions.functions import create_tasks, prepare_tasks


@mock.patch.object(Config, "from_env")
def test_prepare_tasks_returns_expected_tasks_when_given_a_list_of_job_models(
    mock_config_from_env,
):
    # arrange
    mock_config_from_env.return_value = Config(
        "",
        "",
        "",
        "",
        "totalmobile_jobs_queue_id",
        "cloud_function",
        "project",
        "region",
        "rest_api_url",
        "gusty",
        "cloud_function_sa",
        "",
        ""
    )

    tasks = [("task1", b"task1body"),("task2",b"task2body")]

    # act
    result = prepare_tasks(
        tasks=tasks,
        queue_id="totalmobile_jobs_queue_id",
        cloud_function_name="cloud_function"
    )

    # assert
    assert result[0].parent == "totalmobile_jobs_queue_id"
    assert result[0].task.name == "totalmobile_jobs_queue_id/tasks/task1"
    assert (
        result[0].task.http_request.url
        == "https://region-project.cloudfunctions.net/cloud_function"
    )
    assert result[0].task.http_request.body == b"task1body"
    assert (
        result[0].task.http_request.oidc_token.service_account_email
        == "cloud_function_sa"
    )

    assert result[1].parent == "totalmobile_jobs_queue_id"
    assert result[1].task.name == "totalmobile_jobs_queue_id/tasks/task2"
    assert (
        result[1].task.http_request.url
        == "https://region-project.cloudfunctions.net/cloud_function"
    )
    assert result[1].task.http_request.body == b"task2body"
    assert (
        result[1].task.http_request.oidc_token.service_account_email
        == "cloud_function_sa"
    )


@mock.patch.object(tasks_v2.CloudTasksAsyncClient, "create_task")
def test_create_tasks_gets_called_once_for_each_task_given_to_it(mock_create_task):
    # arrange
    task_client = tasks_v2.CloudTasksAsyncClient()
    mock_create_task.return_value = {}
    task_requests = [
        tasks_v2.CreateTaskRequest(parent="qid1", task=tasks_v2.Task()),
        tasks_v2.CreateTaskRequest(parent="qid2", task=tasks_v2.Task()),
    ]

    # act
    create_tasks(task_requests, task_client)

    # assert
    mock_create_task.assert_has_calls(
        [mock.call(task_request) for task_request in task_requests]
    )


@mock.patch.object(tasks_v2.CloudTasksAsyncClient, "create_task")
def test_create_tasks_returns_the_correct_number_of_tasks(mock_create_task):
    # arrange
    task_client = tasks_v2.CloudTasksAsyncClient()
    mock_create_task.return_value = {}
    task_requests = [
        tasks_v2.CreateTaskRequest(parent="qid1", task=tasks_v2.Task()),
        tasks_v2.CreateTaskRequest(parent="qid2", task=tasks_v2.Task()),
    ]

    # act
    result = create_tasks(task_requests, task_client)

    # assert
    assert len(result) == 2
