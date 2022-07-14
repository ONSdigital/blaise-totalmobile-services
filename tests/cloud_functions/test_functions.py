from unittest import mock

from appconfig import Config
from cloud_functions.create_questionnaire_case_tasks import create_task_name
from cloud_functions.functions import prepare_tasks
from models.totalmobile_job_model import TotalmobileJobModel


@mock.patch.object(Config, "from_env")
def test_prepare_tasks_returns_an_expected_number_of_tasks_when_given_a_list_of_job_models(
    _mock_config_from_env,
):
    # arrange
    _mock_config_from_env.return_value = Config(
        "", "", "", "", "", "", "", "", "", "", ""
    )

    models = [
        TotalmobileJobModel("OPN2101A", "world", {"qiD.Serial_Number": "90001"}),
        TotalmobileJobModel("OPN2101A", "world", {"qiD.Serial_Number": "90002"})
    ]

    tasks = [
        (create_task_name(job_model), job_model.json().encode())
        for job_model in models
    ]

    # act
    result = prepare_tasks(
        tasks=tasks,
        queue_id="foo",
        cloud_function_name="bar"
    )

    # assert
    assert len(result) == 2
    assert result[0] != result[1]


@mock.patch.object(Config, "from_env")
def test_prepare_tasks_returns_expected_tasks_when_given_a_list_of_job_models(
    _mock_config_from_env,
):
    # arrange
    _mock_config_from_env.return_value = Config(
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

    model1 = TotalmobileJobModel("OPN2101A", "world", {"qiD.Serial_Number": "90001"})
    model2 = TotalmobileJobModel("OPN2101A", "world", {"qiD.Serial_Number": "90002"})

    tasks = [
        (create_task_name(job_model), job_model.json().encode())
        for job_model in [model1, model2]
    ]

    # act
    result = prepare_tasks(
        tasks=tasks,
        queue_id="totalmobile_jobs_queue_id",
        cloud_function_name="cloud_function"
    )

    # assert
    assert result[0].parent == "totalmobile_jobs_queue_id"
    assert result[0].task.name.startswith(
        "totalmobile_jobs_queue_id/tasks/OPN2101A-90001-"
    )
    assert (
        result[0].task.http_request.url
        == "https://region-project.cloudfunctions.net/cloud_function"
    )
    assert result[0].task.http_request.body == model1.json().encode()
    assert (
        result[0].task.http_request.oidc_token.service_account_email
        == "cloud_function_sa"
    )

    assert result[1].parent == "totalmobile_jobs_queue_id"
    assert result[1].task.name.startswith(
        "totalmobile_jobs_queue_id/tasks/OPN2101A-90002-"
    )
    assert (
        result[1].task.http_request.url
        == "https://region-project.cloudfunctions.net/cloud_function"
    )
    assert result[1].task.http_request.body == model2.json().encode()
    assert (
        result[1].task.http_request.oidc_token.service_account_email
        == "cloud_function_sa"
    )

