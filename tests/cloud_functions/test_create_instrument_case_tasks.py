import json
from unittest import mock

import blaise_restapi
import flask
import pytest
from google.cloud import tasks_v2

from appconfig import Config
from client.optimise import OptimiseClient
from cloud_functions.create_instrument_case_tasks import (
    create_case_tasks_for_instrument,
    create_task_name,
    create_tasks,
    filter_cases,
    map_totalmobile_job_models,
    prepare_tasks,
    retrieve_case_data,
    retrieve_world_id,
    validate_request,
)
from models.totalmobile_job_model import TotalmobileJobModel


def test_create_task_name_returns_correct_name_when_called():
    # arrange
    case_data_dict = {"qiD.Serial_Number": "90001"}
    model = TotalmobileJobModel("OPN2101A", "world", case_data_dict)

    # act
    result = create_task_name(model)

    # assert
    assert result.startswith("OPN2101A-90001-")


def test_create_task_name_returns_unique_name_each_time_when_passed_the_same_model():
    # arrange
    case_data_dict = {"qiD.Serial_Number": "90001"}
    model = TotalmobileJobModel("OPN2101A", "world", case_data_dict)

    # act
    result1 = create_task_name(model)
    result2 = create_task_name(model)

    # assert
    assert result1 != result2


@mock.patch.object(Config, "from_env")
def test_prepare_tasks_returns_an_expected_number_of_tasks_when_given_a_list_of_job_models(
    _mock_config_from_env,
):
    # arrange
    _mock_config_from_env.return_value = Config(
        "", "", "", "", "", "", "", "", "", "", ""
    )

    model1 = TotalmobileJobModel("OPN2101A", "world", {"qiD.Serial_Number": "90001"})
    model2 = TotalmobileJobModel("OPN2101A", "world", {"qiD.Serial_Number": "90002"})

    # act
    result = prepare_tasks([model1, model2])

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

    # act
    result = prepare_tasks([model1, model2])

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


@mock.patch.object(blaise_restapi.Client, "get_instrument_data")
def test_retrieve_case_data_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client,
):
    # arrange
    config = Config("", "", "", "", "", "", "", "", "rest_api_url", "gusty", "")
    _mock_rest_api_client.return_value = {
        "instrumentName": "DST2106Z",
        "instrumentId": "12345-12345-12345-12345-12345",
        "reportingData": "",
    }

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
    _mock_rest_api_client.assert_called_with(
        blaise_server_park, instrument_name, fields
    )


@mock.patch.object(blaise_restapi.Client, "get_instrument_data")
def test_retrieve_case_data_returns_the_case_data_supplied_by_the_rest_api_client(
    _mock_rest_api_client,
):
    # arrange
    config = Config("", "", "", "", "", "", "", "", "rest_api_url", "gusty", "")
    _mock_rest_api_client.return_value = {
        "instrumentName": "DST2106Z",
        "instrumentId": "12345-12345-12345-12345-12345",
        "reportingData": [
            {"qiD.Serial_Number": "10010", "qhAdmin.HOut": "110"},
            {"qiD.Serial_Number": "10020", "qhAdmin.HOut": "110"},
            {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "110"},
        ],
    }
    instrument_name = "OPN2101A"

    # act
    result = retrieve_case_data(instrument_name, config)

    # assert
    assert result == [
        {"qiD.Serial_Number": "10010", "qhAdmin.HOut": "110"},
        {"qiD.Serial_Number": "10020", "qhAdmin.HOut": "110"},
        {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "110"},
    ]


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
        "gusty",
        "",
    )

    _mock_optimise_client.return_value = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "identity": {"reference": "test"},
        "type": "foo",
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
        {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "130"},
    ]
    # act
    result = map_totalmobile_job_models(case_data, world_id, instrument_name)

    # assert
    assert result == [
        TotalmobileJobModel(
            "OPN2101A", "Earth", {"qiD.Serial_Number": "10010", "qhAdmin.HOut": "110"}
        ),
        TotalmobileJobModel(
            "OPN2101A", "Earth", {"qiD.Serial_Number": "10020", "qhAdmin.HOut": "120"}
        ),
        TotalmobileJobModel(
            "OPN2101A", "Earth", {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "130"}
        ),
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


def test_filter_cases_returns_cases_where_srv_stat_is_not_3_or_hOut_is_not_360_or_390():
    # arrange
    cases = [
        {
            # should return
            "srvStat": "1",
            "hOut": "210",
        },
        {
            # should return
            "srvStat": "2",
            "hOut": "210",
        },
        {
            # should not return
            "srvStat": "3",
            "hOut": "360",
        },
        {
            # should not return
            "srvStat": "3",
            "hOut": "390",
        },
        {
            # should not return
            "srvStat": "3",
            "hOut": "210",
        },
        {
            # should not return
            "srvStat": "1",
            "hOut": "360",
        },
        {
            # should not return
            "srvStat": "2",
            "hOut": "390",
        },
    ]
    # act
    result = filter_cases(cases)

    # assert
    assert result == [{"hOut": "210", "srvStat": "1"}, {"hOut": "210", "srvStat": "2"}]


def test_validate_request(mock_create_job_task):
    validate_request(mock_create_job_task)


def test_validate_request_missing_fields():
    with pytest.raises(Exception) as err:
        validate_request({"world_id": ""})
    assert (
        str(err.value) == "Required fields missing from request payload: ['instrument']"
    )


@mock.patch.object(Config, "from_env")
@mock.patch("cloud_functions.create_instrument_case_tasks.validate_request")
@mock.patch("cloud_functions.create_instrument_case_tasks.retrieve_world_id")
@mock.patch("cloud_functions.create_instrument_case_tasks.retrieve_case_data")
@mock.patch("cloud_functions.create_instrument_case_tasks.filter_cases")
@mock.patch("cloud_functions.create_instrument_case_tasks.map_totalmobile_job_models")
@mock.patch("cloud_functions.create_instrument_case_tasks.prepare_tasks")
def test_create_case_tasks_for_instrument(
    mock_prepare_tasks,
    mock_map_totalmobile_job_models,
    mock_filter_cases,
    mock_retrieve_case_data,
    mock_retrieve_world_id,
    mock_validate_request,
    mock_from_env,
):
    # arrange
    mock_request = flask.Request.from_values(json={"instrument": "OPN2101A"})

    # act
    result = create_case_tasks_for_instrument(mock_request)

    # assert
    assert result == "Done"


@mock.patch.object(Config, "from_env")
def test_create_case_tasks_for_instrument_error(mock_from_env):
    # arrange
    mock_request = flask.Request.from_values(json={"questionnaire": ""})

    # assert
    with pytest.raises(Exception) as err:
        create_case_tasks_for_instrument(mock_request)
    assert (
        str(err.value) == "Required fields missing from request payload: ['instrument']"
    )
