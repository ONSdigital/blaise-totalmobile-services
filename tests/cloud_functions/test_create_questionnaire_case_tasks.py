from appconfig import Config
from cloud_functions.create_questionnaire_case_tasks import create_task_name, prepare_tasks
from models.totalmobile_job_model import TotalmobileJobModel
from unittest.mock import patch
import json


def test_create_task_name_returns_correct_name_when_called():
    # arrange
    case_data_dict = {"qiD.Serial_Number": "90001"}
    model = TotalmobileJobModel(case_data_dict, "OPN2101A", "world")

    # act
    result = create_task_name(model)

    # assert
    assert result.startswith("OPN2101A-90001-")


def test_create_task_name_returns_unique_name_each_time_when_passed_the_same_model():
    # arrange
    case_data_dict = {"qiD.Serial_Number": "90001"}
    model = TotalmobileJobModel(case_data_dict, "OPN2101A", "world")

    # act
    result1 = create_task_name(model)
    result2 = create_task_name(model)

    # assert
    assert result1 != result2


@patch.object(Config, "from_env")
def test_prepare_tasks_returns_an_expected_number_of_tasks_when_given_a_list_of_job_models(_mock_config_from_env):
    # arrange
    _mock_config_from_env.return_value = Config("", "", "", "", "", "", " ", "", "", "")

    model1 = TotalmobileJobModel({"qiD.Serial_Number": "90001"}, "OPN2101A", "world")
    model2 = TotalmobileJobModel({"qiD.Serial_Number": "90002"}, "OPN2101A", "world")

    # act
    result = prepare_tasks(model1, model2)

    # assert
    assert len(result) == 2
    assert result[0] != result[1]


@patch.object(Config, "from_env")
def test_prepare_tasks_returns_expected_tasks_when_given_a_list_of_job_models(_mock_config_from_env):
    # arrange
    _mock_config_from_env.return_value = Config("", "", "", "", "totalmobile_jobs_queue_id", "cloud_function", "project", "region", "rest_api_url", "gusty")

    model1 = TotalmobileJobModel({"qiD.Serial_Number": "90001"}, "OPN2101A", "world")
    model2 = TotalmobileJobModel({"qiD.Serial_Number": "90002"}, "OPN2101A", "world")

    # act
    result = prepare_tasks(model1, model2)

    # assert
    assert result[0].parent == "totalmobile_jobs_queue_id"
    assert result[0].task.name.startswith("totalmobile_jobs_queue_id/tasks/OPN2101A-90001-")
    assert result[0].task.http_request.url == "https://region-project.cloudfunctions.net/cloud_function"
    assert result[0].task.http_request.body == json.dumps(model1.case_data).encode()

    assert result[1].parent == "totalmobile_jobs_queue_id"
    assert result[1].task.name.startswith("totalmobile_jobs_queue_id/tasks/OPN2101A-90002-")
    assert result[1].task.http_request.url == "https://region-project.cloudfunctions.net/cloud_function"
    assert result[1].task.http_request.body == json.dumps(model2.case_data).encode()

