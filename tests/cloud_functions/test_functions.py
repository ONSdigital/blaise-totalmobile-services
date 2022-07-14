from unittest import mock

from appconfig import Config
from cloud_functions.create_questionnaire_case_tasks import create_task_name
from cloud_functions.functions import prepare_tasks
from models.totalmobile_job_model import TotalmobileJobModel


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

