import json
from unittest import mock

import blaise_restapi
import flask
import pytest

from appconfig import Config
from client.optimise import OptimiseClient
from cloud_functions.create_questionnaire_case_tasks import (
    create_questionnaire_case_tasks,
    create_task_name,
    filter_cases,
    get_wave_from_questionnaire_name,
    map_totalmobile_job_models,
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


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_retrieve_case_data_calls_the_rest_api_client_with_the_correct_parameters(
    _mock_rest_api_client,
):
    # arrange
    config = Config("", "", "", "", "", "", "", "", "rest_api_url", "gusty", "")
    _mock_rest_api_client.return_value = {
        "questionnaireName": "DST2106Z",
        "questionnaireId": "12345-12345-12345-12345-12345",
        "reportingData": "",
    }

    blaise_server_park = "gusty"
    questionnaire_name = "OPN2101A"

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
        "qDataBag.TelNoAppt",
        "hOut",
        "srvStat",
        "qiD.Serial_Number",
        "qDataBag.Wave",
        "qDataBag.Priority",
        "qDataBag.FieldRegion"
    ]

    # act
    foo = retrieve_case_data(questionnaire_name, config)

    # assert
    _mock_rest_api_client.assert_called_with(
        blaise_server_park, questionnaire_name, fields
    )


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_retrieve_case_data_returns_the_case_data_supplied_by_the_rest_api_client(
    _mock_rest_api_client,
):
    # arrange
    config = Config("", "", "", "", "", "", "", "", "rest_api_url", "gusty", "")
    _mock_rest_api_client.return_value = {
        "questionnaireName": "DST2106Z",
        "questionnaireId": "12345-12345-12345-12345-12345",
        "reportingData": [
            {"qiD.Serial_Number": "10010", "qhAdmin.HOut": "110"},
            {"qiD.Serial_Number": "10020", "qhAdmin.HOut": "110"},
            {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "110"},
        ],
    }
    questionnaire_name = "OPN2101A"

    # act
    result = retrieve_case_data(questionnaire_name, config)

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
    questionnaire_name = "OPN2101A"
    world_id = "Earth"

    case_data = [
        {"qiD.Serial_Number": "10010", "qhAdmin.HOut": "110"},
        {"qiD.Serial_Number": "10020", "qhAdmin.HOut": "120"},
        {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "130"},
    ]
    # act
    result = map_totalmobile_job_models(case_data, world_id, questionnaire_name)

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


def test_filter_cases_returns_cases_only_where_criteria_is_met():
    # arrange
    cases = [
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "qDataBag.TelNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1", 
            "hOut": 310
        },
        {
            # should not return
            "qDataBag.TelNo": "123435",
            "qDataBag.TelNo2": "",
            "qDataBag.TelNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1", 
            "hOut": 310
        },
        {
            # should not return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "12345",
            "qDataBag.TelNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1", 
            "hOut": 310
        },
        {
            # should not return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "qDataBag.TelNoAppt": "12345",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1", 
            "hOut": 310
        },
        {
            # should not return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "qDataBag.TelNoAppt": "",
            "qDataBag.Wave": "2",
            "qDataBag.Priority": "1", 
            "hOut": 310
        },
        {
            # should not return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "qDataBag.TelNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "6", 
            "hOut": 310
        },
        {
            # should not return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "qDataBag.TelNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1", 
            "hOut": 410
        },
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "qDataBag.TelNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1", 
            "hOut": 0
        },
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "qDataBag.TelNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "2", 
            "hOut": 0
        },
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "qDataBag.TelNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "3", 
            "hOut": 0
        },
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "qDataBag.TelNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "4", 
            "hOut": 0
        },
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "qDataBag.TelNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "5", 
            "hOut": 0
        },
    ]
    
    # act
    result = filter_cases(cases)

    # assert
    assert result == [{"qDataBag.TelNo": "","qDataBag.TelNo2": "","qDataBag.TelNoAppt": "","qDataBag.Wave": "1","qDataBag.Priority": "1", "hOut": 310 },
                        {"qDataBag.TelNo": "","qDataBag.TelNo2": "","qDataBag.TelNoAppt": "","qDataBag.Wave": "1","qDataBag.Priority": "1", "hOut": 0 },
                        {"qDataBag.TelNo": "","qDataBag.TelNo2": "","qDataBag.TelNoAppt": "","qDataBag.Wave": "1","qDataBag.Priority": "2", "hOut": 0 },
                        {"qDataBag.TelNo": "","qDataBag.TelNo2": "","qDataBag.TelNoAppt": "","qDataBag.Wave": "1","qDataBag.Priority": "3", "hOut": 0 },
                        {"qDataBag.TelNo": "","qDataBag.TelNo2": "","qDataBag.TelNoAppt": "","qDataBag.Wave": "1","qDataBag.Priority": "4", "hOut": 0 },
                        {"qDataBag.TelNo": "","qDataBag.TelNo2": "","qDataBag.TelNoAppt": "","qDataBag.Wave": "1","qDataBag.Priority": "5", "hOut": 0 }]


def test_validate_request(mock_create_job_task):
    validate_request(mock_create_job_task)


def test_validate_request_missing_fields():
    with pytest.raises(Exception) as err:
        validate_request({"world_id": ""})
    assert (
        str(err.value) == "Required fields missing from request payload: ['questionnaire']"
    )


@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_world_id")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_case_data")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.filter_cases")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.run_async_tasks")
def test_create_case_tasks_for_questionnaire(
    mock_run_async_tasks,
    mock_filter_cases,
    mock_retrieve_case_data,
    mock_retrieve_world_id,
):
    # arrange
    mock_request = flask.Request.from_values(json={"questionnaire": "LMS2101_AA1"})
    config = Config("", "", "", "", "queue-id", "cloud-function", "", "", "", "", "",)
    mock_retrieve_case_data.return_value = [{"qiD.Serial_Number": "10010"},{"qiD.Serial_Number": "10012"}]
    mock_retrieve_world_id.return_value = "1"
    mock_filter_cases.return_value = [{"qiD.Serial_Number": "10010"}]
    
    # act
    result = create_questionnaire_case_tasks(mock_request, config)

    # assert
    mock_retrieve_case_data.assert_called_with("LMS2101_AA1", config)
    mock_retrieve_world_id.assert_called_with(config)
    mock_filter_cases.assert_called_with([{"qiD.Serial_Number": "10010"},{"qiD.Serial_Number": "10012"}])
    mock_run_async_tasks.assert_called_once()
    kwargs = mock_run_async_tasks.call_args.kwargs
    assert kwargs['cloud_function_name'] == "cloud-function"
    assert kwargs['queue_id'] == "queue-id"
    assert len(kwargs['tasks']) == 1
    task = kwargs['tasks'][0]
    assert task[0][0:3] == "LMS"
    assert json.loads(task[1]) == {'case': {'qiD.Serial_Number': '10010'}, 
                                'questionnaire': 'LMS2101_AA1', 'world_id': '1'}
    assert result == "Done"


def test_create_questionnaire_case_tasks_error():
    # arrange
    mock_request = flask.Request.from_values(json={"instrument": ""})
    config = Config("", "", "", "", "queue-id", "cloud-function", "", "", "", "", "",)
    # assert
    with pytest.raises(Exception) as err:
        create_questionnaire_case_tasks(mock_request, config)
    assert (
        str(err.value) == "Required fields missing from request payload: ['questionnaire']"
    )


@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_world_id")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_case_data")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.filter_cases")
def test_get_wave_from_questionnaire_name_none_LMS_error(
    mock_filter_cases,
    mock_retrieve_case_data,
    mock_retrieve_world_id,
):
    # arrange
    config = Config("", "", "", "", "queue-id", "cloud-function", "", "", "", "", "",)
    mock_request = flask.Request.from_values(json={"questionnaire": "OPN2101A"})
    mock_retrieve_case_data.return_value = [{"qiD.Serial_Number": "10010"},{"qiD.Serial_Number": "10012"}]
    mock_retrieve_world_id.return_value = "1"
    mock_filter_cases.return_value = [{"qiD.Serial_Number": "10010"}]
    
    # act
    with pytest.raises(Exception) as err:
        create_questionnaire_case_tasks(mock_request, config)

    # assert
    assert str(err.value) == "Invalid format for questionnaire name: OPN2101A"


@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_world_id")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_case_data")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.filter_cases")
def test_get_wave_from_questionnaire_name_unsupported_wave_error(
    mock_filter_cases,
    mock_retrieve_case_data,
    mock_retrieve_world_id,
):
    # arrange
    config = Config("", "", "", "", "queue-id", "cloud-function", "", "", "", "", "",)
    mock_request = flask.Request.from_values(json={"questionnaire": "LMS2101_AA2"})
    mock_retrieve_case_data.return_value = [{"qiD.Serial_Number": "10010"},{"qiD.Serial_Number": "10012"}]
    mock_retrieve_world_id.return_value = "1"
    mock_filter_cases.return_value = [{"qiD.Serial_Number": "10010"}]
    
    # act
    with pytest.raises(Exception) as err:
        create_questionnaire_case_tasks(mock_request, config)

    # assert
    assert str(err.value) == "Invalid wave: currently only wave 1 supported"


def test_get_wave_from_questionnaire_name():
    assert get_wave_from_questionnaire_name("LMS2101_AA1") == "1"
    assert get_wave_from_questionnaire_name("LMS1234_ZZ2") == "2"


def test_get_wave_from_questionnaire_name_with_invalid_format_raises_error():
    with pytest.raises(Exception) as err:
        get_wave_from_questionnaire_name("ABC1234_AA1")
    assert str(err.value) == "Invalid format for questionnaire name: ABC1234_AA1"