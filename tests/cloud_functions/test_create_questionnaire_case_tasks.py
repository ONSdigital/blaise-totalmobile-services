from appconfig import Config
from cloud_functions.create_questionnaire_case_tasks import create_task_name, prepare_tasks, retrieve_case_data, \
    retrieve_world_id, map_totalmobile_job_models, create_tasks
from models.totalmobile_job_model import TotalmobileJobModel
from unittest import mock
from client.optimise import OptimiseClient
from google.cloud import tasks_v2

import json
import blaise_restapi


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


@mock.patch.object(Config, "from_env")
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


@mock.patch.object(Config, "from_env")
def test_prepare_tasks_returns_expected_tasks_when_given_a_list_of_job_models(_mock_config_from_env):
    # arrange
    _mock_config_from_env.return_value = Config("", "", "", "", "totalmobile_jobs_queue_id", "cloud_function",
                                                "project", "region", "rest_api_url", "gusty")

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


@mock.patch.object(blaise_restapi.Client, "get_instrument_data")
def test_retrieve_case_data_calls_the_rest_api_client_with_the_correct_parameters(_mock_rest_api_client):
    # arrange
    config = Config("", "", "", "", "", "", "", "", "rest_api_url", "gusty")
    _mock_rest_api_client.return_value = {"instrumentName": "DST2106Z",
                                          "instrumentId": "12345-12345-12345-12345-12345",
                                          "reportingData": ""}

    blaise_server_park = "gusty"
    instrument_name = "OPN2101A"

    fields = [
        "qDataBag.UPRN_Latitude",
        "qDataBag.UPRN_Longitude",
        "qDataBag.Prem1",
        "qDataBag.Prem2",
        "qDataBag.Prem3",
        "qDataBag.PostTown",
        "qDataBag.PostCode",
        "qDataBag.TelNo",
        "qDataBag.TelNo2",
        "hOut",
        "srvStat",
        "qiD.Serial_Number",
    ]

    # act
    retrieve_case_data(instrument_name, config)

    # assert
    _mock_rest_api_client.assert_called_with(blaise_server_park, instrument_name, fields)


@mock.patch.object(blaise_restapi.Client, "get_instrument_data")
def test_retrieve_case_data_returns_the_case_data_supplied_by_the_rest_api_client(_mock_rest_api_client):
    # arrange
    config = Config("", "", "", "", "", "", "", "", "rest_api_url", "gusty")
    _mock_rest_api_client.return_value = {"instrumentName": "DST2106Z",
                                          "instrumentId": "12345-12345-12345-12345-12345",
                                          "reportingData": [{"qiD.Serial_Number": "10010", "qhAdmin.HOut": "110"},
                                                            {"qiD.Serial_Number": "10020", "qhAdmin.HOut": "110"},
                                                            {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "110"}
                                                            ]}
    instrument_name = "OPN2101A"

    # act
    result = retrieve_case_data(instrument_name, config)

    # assert
    assert result == [{"qiD.Serial_Number": "10010", "qhAdmin.HOut": "110"},
                      {"qiD.Serial_Number": "10020", "qhAdmin.HOut": "110"},
                      {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "110"}]


@mock.patch.object(OptimiseClient, "get_world")
def test_retrieve_world_id_returns_a_world_id(_mock_optimise_client):
    # arrange
    config = Config(
        "totalmobile_url",
        "totalmobile_instance",
        "totalmobile_client_id",
        "totalmobile_client_secret",
        "",
        "",
        "",
        "",
        "rest_api_url",
        "gusty"
    )

    _mock_optimise_client.return_value = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "identity": {
            "reference": "test"
        },
        "type": "foo"
    }

    # act
    result = retrieve_world_id(config)

    # assert
    assert result == "3fa85f64-5717-4562-b3fc-2c963f66afa6"


def test_map_totalmobile_job_models_maps_the_correct_list_of_models():
    # arrange
    instrument_name = "OPN2101A"
    world_id = "Earth"

    case_data = [
        {"qiD.Serial_Number": "10010", "qhAdmin.HOut": "110"},
        {"qiD.Serial_Number": "10020", "qhAdmin.HOut": "120"},
        {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "130"}
    ]
    # act
    result = map_totalmobile_job_models(case_data, world_id, instrument_name)

    # assert
    assert result == [
        TotalmobileJobModel("OPN2101A", "Earth", {"qiD.Serial_Number": "10010", "qhAdmin.HOut": "110"}),
        TotalmobileJobModel("OPN2101A", "Earth", {"qiD.Serial_Number": "10020", "qhAdmin.HOut": "120"}),
        TotalmobileJobModel("OPN2101A", "Earth", {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "130"})
    ]


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
    mock_create_task.assert_has_calls([mock.call(task_request) for task_request in task_requests])


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
