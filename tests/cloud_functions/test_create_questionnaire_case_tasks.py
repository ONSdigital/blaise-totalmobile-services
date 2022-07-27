import json
from unittest import mock

import blaise_restapi
import flask
import pytest
import logging

from appconfig import Config
from client.optimise import OptimiseClient
from cloud_functions.create_questionnaire_case_tasks import (
    create_questionnaire_case_tasks,
    create_task_name,
    filter_cases,
    get_wave_from_questionnaire_name,
    map_totalmobile_job_models,
    retrieve_case_data,
    retrieve_world_ids,
    validate_request,
    append_uacs_to_case_data
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
        "telNoAppt",
        "hOut",
        "qiD.Serial_Number",
        "qDataBag.Wave",
        "qDataBag.Priority",
        "qDataBag.FieldRegion"
    ]

    # act
    retrieve_case_data(questionnaire_name, config)

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


def test_map_totalmobile_job_models_maps_the_correct_list_of_models():
    # arrange
    questionnaire_name = "OPN2101A"

    case_data = [
        {"qiD.Serial_Number": "10010", "qhAdmin.HOut": "110"},
        {"qiD.Serial_Number": "10020", "qhAdmin.HOut": "120"},
        {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "130"},
    ]

    world_ids = [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "3fa85f64-5717-4562-b3fc-2c963f66afa9",
    ]

    # act
    result = map_totalmobile_job_models(case_data, world_ids, questionnaire_name)

    # assert
    assert result == [
        TotalmobileJobModel(
            "OPN2101A", "3fa85f64-5717-4562-b3fc-2c963f66afa6", {"qiD.Serial_Number": "10010", "qhAdmin.HOut": "110",
                                                                 }
        ),
        TotalmobileJobModel(
            "OPN2101A", "3fa85f64-5717-4562-b3fc-2c963f66afa7", {"qiD.Serial_Number": "10020", "qhAdmin.HOut": "120",
                                                                 }
        ),
        TotalmobileJobModel(
            "OPN2101A", "3fa85f64-5717-4562-b3fc-2c963f66afa9", {"qiD.Serial_Number": "10030", "qhAdmin.HOut": "130",
                                                                 }
        ),
    ]


def test_filter_cases_returns_cases_only_where_criteria_is_met():
    # arrange
    cases = [
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "telNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1",
            "hOut": "310"
        },
        {
            # should not return
            "qDataBag.TelNo": "123435",
            "qDataBag.TelNo2": "",
            "telNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1",
            "hOut": "310"
        },
        {
            # should not return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "12345",
            "telNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1",
            "hOut": "310"
        },
        {
            # should not return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "telNoAppt": "12345",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1",
            "hOut": "310"
        },
        {
            # should not return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "telNoAppt": "",
            "qDataBag.Wave": "2",
            "qDataBag.Priority": "1",
            "hOut": "310"
        },
        {
            # should not return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "telNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "6",
            "hOut": "310"
        },
        {
            # should not return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "telNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1",
            "hOut": "410"
        },
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "telNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "1",
            "hOut": "0"
        },
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "telNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "2",
            "hOut": "0"
        },
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "telNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "3",
            "hOut": "0"
        },
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "telNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "4",
            "hOut": "0"
        },
        {
            # should return
            "qDataBag.TelNo": "",
            "qDataBag.TelNo2": "",
            "telNoAppt": "",
            "qDataBag.Wave": "1",
            "qDataBag.Priority": "5",
            "hOut": "0"
        },
    ]

    # act
    result = filter_cases(cases)

    # assert
    assert result == [{"qDataBag.TelNo": "", "qDataBag.TelNo2": "", "telNoAppt": "", "qDataBag.Wave": "1",
                       "qDataBag.Priority": "1", "hOut": "310"},
                      {"qDataBag.TelNo": "", "qDataBag.TelNo2": "", "telNoAppt": "", "qDataBag.Wave": "1",
                       "qDataBag.Priority": "1", "hOut": "0"},
                      {"qDataBag.TelNo": "", "qDataBag.TelNo2": "", "telNoAppt": "", "qDataBag.Wave": "1",
                       "qDataBag.Priority": "2", "hOut": "0"},
                      {"qDataBag.TelNo": "", "qDataBag.TelNo2": "", "telNoAppt": "", "qDataBag.Wave": "1",
                       "qDataBag.Priority": "3", "hOut": "0"},
                      {"qDataBag.TelNo": "", "qDataBag.TelNo2": "", "telNoAppt": "", "qDataBag.Wave": "1",
                       "qDataBag.Priority": "4", "hOut": "0"},
                      {"qDataBag.TelNo": "", "qDataBag.TelNo2": "", "telNoAppt": "", "qDataBag.Wave": "1",
                       "qDataBag.Priority": "5", "hOut": "0"}]


def test_validate_request(mock_create_job_task):
    validate_request(mock_create_job_task)


def test_validate_request_missing_fields():
    with pytest.raises(Exception) as err:
        validate_request({"world_id": ""})
    assert (
            str(err.value) == "Required fields missing from request payload: ['questionnaire']"
    )

@mock.patch("cloud_functions.create_questionnaire_case_tasks.append_uacs_to_case_data")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_world_ids")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_case_data")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_case_uac_data")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.filter_cases")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.run_async_tasks")
def test_create_case_tasks_for_questionnaire(
        mock_run_async_tasks,
        mock_filter_cases,
        mock_retrieve_case_uac_data,
        mock_retrieve_case_data,
        mock_retrieve_world_ids,
        mock_append_uacs_to_case_data
):
    # arrange
    mock_request = flask.Request.from_values(json={"questionnaire": "LMS2101_AA1"})
    config = Config("", "", "", "", "queue-id", "cloud-function", "", "", "", "", "", )
    mock_retrieve_case_data.return_value = [{"qiD.Serial_Number": "10010"}, {"qiD.Serial_Number": "10012"}]
    mock_filter_cases.return_value = [{"qiD.Serial_Number": "10010"}]
    mock_retrieve_case_uac_data.return_value = {
        "10010": {
            "instrument_name": "LMS2101_AA1",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "8176",
                "uac2": "4726",
                "uac3": "3991"
            },
            "full_uac": "817647263991"
        }
    }
    mock_append_uacs_to_case_data.return_value = [
        {
            "qiD.Serial_Number": "10010",
            "uac_chunks": {
                "uac1": "8176",
                "uac2": "4726",
                "uac3": "3991"
            },
        }
    ]
    mock_retrieve_world_ids.return_value = "1", [{"qiD.Serial_Number": "10010"}]
    # act
    result = create_questionnaire_case_tasks(mock_request, config)

    # assert
    mock_retrieve_case_data.assert_called_with("LMS2101_AA1", config)
    mock_retrieve_world_ids.assert_called_with(config, [{"qiD.Serial_Number": "10010", "uac_chunks": {
        "uac1": "8176",
        "uac2": "4726",
        "uac3": "3991"
    }, }])
    mock_filter_cases.assert_called_with([{"qiD.Serial_Number": "10010"}, {"qiD.Serial_Number": "10012"}])
    mock_run_async_tasks.assert_called_once()
    kwargs = mock_run_async_tasks.call_args.kwargs
    assert kwargs['cloud_function'] == "cloud-function"
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
    config = Config("", "", "", "", "queue-id", "cloud-function", "", "", "", "", "", )
    # assert
    with pytest.raises(Exception) as err:
        create_questionnaire_case_tasks(mock_request, config)
    assert (
            str(err.value) == "Required fields missing from request payload: ['questionnaire']"
    )


@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_world_ids")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_case_data")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.filter_cases")
def test_get_wave_from_questionnaire_name_none_LMS_error(
        mock_filter_cases,
        mock_retrieve_case_data,
        mock_retrieve_world_ids,
):
    # arrange
    config = Config("", "", "", "", "queue-id", "cloud-function", "", "", "", "", "", )
    mock_request = flask.Request.from_values(json={"questionnaire": "OPN2101A"})
    mock_retrieve_case_data.return_value = [{"qiD.Serial_Number": "10010"}, {"qiD.Serial_Number": "10012"}]
    mock_retrieve_world_ids.return_value = "1"
    mock_filter_cases.return_value = [{"qiD.Serial_Number": "10010"}]

    # act
    with pytest.raises(Exception) as err:
        create_questionnaire_case_tasks(mock_request, config)

    # assert
    assert str(err.value) == "Invalid format for questionnaire name: OPN2101A"


@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_world_ids")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.retrieve_case_data")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.filter_cases")
def test_get_wave_from_questionnaire_name_unsupported_wave_error(
        mock_filter_cases,
        mock_retrieve_case_data,
        mock_retrieve_world_ids,
):
    # arrange
    config = Config("", "", "", "", "queue-id", "cloud-function", "", "", "", "", "", )
    mock_request = flask.Request.from_values(json={"questionnaire": "LMS2101_AA2"})
    mock_retrieve_case_data.return_value = [{"qiD.Serial_Number": "10010"}, {"qiD.Serial_Number": "10012"}]
    mock_retrieve_world_ids.return_value = "1"
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


@mock.patch.object(OptimiseClient, "get_worlds")
def test_retrieve_world_ids_correctly_maps_a_case_field_region_to_a_world_id(_mock_optimise_client):
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

    filtered_cases = [
        {"qDataBag.FieldRegion": "Region 1"},
        {"qDataBag.FieldRegion": "Region 2"},
        {"qDataBag.FieldRegion": "Region 4"},
    ]

    _mock_optimise_client.return_value = [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {
                "reference": "Region 1"
            },
            "type": "foo"
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "identity": {
                "reference": "Region 2"
            },
            "type": "foo"
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
            "identity": {
                "reference": "Region 3"
            },
            "type": "foo"
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
            "identity": {
                "reference": "Region 4"
            },
            "type": "foo"
        },
    ]

    world_ids, new_filtered_cases = retrieve_world_ids(config, filtered_cases)

    # assert
    assert world_ids == [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "3fa85f64-5717-4562-b3fc-2c963f66afa9",
    ]
    assert new_filtered_cases == [
        {"qDataBag.FieldRegion": "Region 1"},
        {"qDataBag.FieldRegion": "Region 2"},
        {"qDataBag.FieldRegion": "Region 4"},
    ]


@mock.patch.object(OptimiseClient, "get_worlds")
def test_retrieve_world_ids_logs_a_console_error_when_given_an_unknown_world(_mock_optimise_client, caplog):
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

    filtered_cases = [
        {"qDataBag.FieldRegion": "Risca"},
    ]

    _mock_optimise_client.return_value = [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {
                "reference": "Region 1"
            },
            "type": "foo"
        },
    ]

    # act 
    retrieve_world_ids(config, filtered_cases)

    # assert
    assert ('root', logging.WARNING, 'Unsupported world: Risca') in caplog.record_tuples


@mock.patch.object(OptimiseClient, "get_worlds")
def test_retrieve_world_ids_logs_a_console_error_and_returns_data_when_given_an_unknown_world_and_a_known_world(
        _mock_optimise_client, caplog):
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

    filtered_cases = [
        {"qDataBag.FieldRegion": "Risca"},
        {"qDataBag.FieldRegion": "Region 1"},
    ]

    _mock_optimise_client.return_value = [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {
                "reference": "Region 1"
            },
            "type": "foo"
        },
    ]

    # act 
    world_ids, new_filtered_cases = retrieve_world_ids(config, filtered_cases)

    # assert
    assert len(world_ids) == len(new_filtered_cases)
    assert world_ids == ["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
    assert new_filtered_cases == [{"qDataBag.FieldRegion": "Region 1"}]
    assert ('root', logging.WARNING, 'Unsupported world: Risca') in caplog.record_tuples


@mock.patch.object(OptimiseClient, "get_worlds")
def test_retrieve_world_ids_logs_a_console_error_when_field_region_is_missing(_mock_optimise_client, caplog):
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

    filtered_cases = [
        {"qDataBag.FieldRegion": ""},
    ]

    _mock_optimise_client.return_value = [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {
                "reference": "Region 1"
            },
            "type": "foo"
        },
    ]

    # act
    retrieve_world_ids(config, filtered_cases)

    # assert
    assert ('root', logging.WARNING, 'Case rejected. Missing Field Region') in caplog.record_tuples


@mock.patch.object(OptimiseClient, "get_worlds")
def test_retrieve_world_ids_logs_a_console_error_and_returns_data_when_given_an_unknown_world_and_a_known_world_and_a_known_world(
        _mock_optimise_client, caplog):
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

    filtered_cases = [
        {"qDataBag.FieldRegion": ""},
        {"qDataBag.FieldRegion": "Region 1"},
    ]

    _mock_optimise_client.return_value = [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {
                "reference": "Region 1"
            },
            "type": "foo"
        },
    ]

    # act
    world_ids, new_filtered_cases = retrieve_world_ids(config, filtered_cases)

    # assert
    assert len(world_ids) == len(new_filtered_cases)
    assert world_ids == ["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
    assert new_filtered_cases == [{"qDataBag.FieldRegion": "Region 1"}]
    assert ('root', logging.WARNING, 'Case rejected. Missing Field Region') in caplog.record_tuples


def test_uacs_are_correctly_appended_to_case_data():
    case_uacs = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {
                "uac1": "8176",
                "uac2": "4726",
                "uac3": "3991"
            },
            "full_uac": "817647263991"
        },
        "10020": {
            "instrument_name": "OPN2101A",
            "case_id": "10020",
            "uac_chunks": {
                "uac1": "8176",
                "uac2": "4726",
                "uac3": "3992"
            },
            "full_uac": "817647263992"
        },
        "10030": {
            "instrument_name": "OPN2101A",
            "case_id": "10030",
            "uac_chunks": {
                "uac1": "8176",
                "uac2": "4726",
                "uac3": "3993"
            },
            "full_uac": "817647263994"
        },
    }

    filtered_cases = [{"qiD.Serial_Number": "10030", "qDataBag.TelNo": "", "qDataBag.TelNo2": "", "telNoAppt": "",
                       "qDataBag.Wave": "1",
                       "qDataBag.Priority": "1", "hOut": "310"},
                      ]

    result = append_uacs_to_case_data(filtered_cases, case_uacs)
    assert result == [{
        "hOut": "310",
        "qDataBag.Priority": "1",
        "qDataBag.TelNo": "",
        "qDataBag.TelNo2": "",
        "qDataBag.Wave": "1",
        "qiD.Serial_Number": "10030",
        "telNoAppt": "",
        "uac_chunks": {
            "uac1": "8176",
            "uac2": "4726",
            "uac3": "3993"
        },
    }]
