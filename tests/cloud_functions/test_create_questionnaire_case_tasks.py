import json
from unittest import mock

import blaise_restapi
import flask
import pytest
import logging
from models.questionnaire_case_model import QuestionnaireCaseModel, UacChunks

from tests.helpers import config_helper
from client.optimise import OptimiseClient
from cloud_functions.create_questionnaire_case_tasks import (
    create_questionnaire_case_tasks,
    create_task_name,
    filter_cases,
    get_wave_from_questionnaire_name,
    map_totalmobile_job_models,
    get_questionnaire_case_model_list,
    get_world_ids,
    validate_request,
    append_uacs_to_retained_case
)
from models.totalmobile_job_model import TotalmobileJobModel


def test_create_task_name_returns_correct_name_when_called():
    questionnaire_case_model = QuestionnaireCaseModel(serial_number = "90001")
    model = TotalmobileJobModel("OPN2101A", "world", questionnaire_case_model)

    assert create_task_name(model).startswith("OPN2101A-90001-")


def test_create_task_name_returns_unique_name_each_time_when_passed_the_same_model():
    questionnaire_case_model = QuestionnaireCaseModel(serial_number = "90001")
    model = TotalmobileJobModel("OPN2101A", "world", questionnaire_case_model)

    assert create_task_name(model) != create_task_name(model)


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_case_data_calls_the_rest_api_client_with_the_correct_parameters(_mock_rest_api_client):
    config = config_helper.get_default_config()
    blaise_server_park = "gusty"
    questionnaire_name = "DST2106Z"
    fields = [
        "qiD.Serial_Number",
        "dataModelName",
        "qDataBag.TLA",
        "qDataBag.Wave",
        "qDataBag.Prem1",
        "qDataBag.Prem2",
        "qDataBag.Prem3",
        "qDataBag.District",
        "qDataBag.PostTown",
        "qDataBag.PostCode",
        "qDataBag.TelNo",
        "qDataBag.TelNo2",
        "telNoAppt",
        "hOut",
        "qDataBag.UPRN_Latitude",
        "qDataBag.UPRN_Longitude",
        "qDataBag.Priority",
        "qDataBag.FieldRegion",
        "qDataBag.FieldTeam",
        "qDataBag.WaveComDTE"
    ]

    # act
    get_questionnaire_case_model_list(questionnaire_name, config)

    # assert
    _mock_rest_api_client.assert_called_with(
        blaise_server_park, questionnaire_name, fields
    )


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_case_data_returns_the_case_data_supplied_by_the_rest_api_client(
        _mock_rest_api_client,
):
    # arrange
    config = config_helper.get_default_config()
    _mock_rest_api_client.return_value = {
        "questionnaireName": "DST2106Z",
        "questionnaireId": "12345-12345-12345-12345-12345",
        "reportingData": [
            {"qiD.Serial_Number": "10010", "hOut": "110"},
            {"qiD.Serial_Number": "10020", "hOut": "210"},
            {"qiD.Serial_Number": "10030", "hOut": "310"},
        ],
    }
    questionnaire_name = "OPN2101A"

    # act
    result = get_questionnaire_case_model_list(questionnaire_name, config)

    # assert
    assert result[0].serial_number == "10010" 
    assert result[0].outcome_code == "110"

    assert result[1].serial_number == "10020" 
    assert result[1].outcome_code == "210"

    assert result[2].serial_number == "10030" 
    assert result[2].outcome_code == "310"


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
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "1",
            outcome_code= "310"  
        ),
        # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "123435",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "1",
            outcome_code= "310"  
        ),      
        # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "123435",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "1",
            outcome_code= "310"  
        ),      
        # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "123435",          
            wave = "1",
            priority = "1",
            outcome_code= "310"  
        ),    
        # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "2",
            priority = "1",
            outcome_code= "310"  
        ),       
         # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "6",
            outcome_code= "310"  
        ),                       
        # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "1",
            outcome_code= "410"  
        ),       
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "1",
            outcome_code= "0"  
        ),      
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "2",
            outcome_code= "0"  
        ),   
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "3",
            outcome_code= "0"  
        ),  
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "4",
            outcome_code= "0"  
        ),  
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "5",
            outcome_code= "0"  
        ),     
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "5",
            outcome_code= ""  
        )                                                
    ]
    # act

    result = filter_cases(cases)
    print(len(cases))
    print(len(result))

    # assert
    assert result == [
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "1",
            outcome_code= "310"  
        ),
   # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "1",
            outcome_code= "0"  
        ),      
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "2",
            outcome_code= "0"  
        ),   
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "3",
            outcome_code= "0"  
        ),  
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "4",
            outcome_code= "0"  
        ),  
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "5",
            outcome_code= "0"  
        ),     
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",          
            wave = "1",
            priority = "5",
            outcome_code= ""  
        )  
    ]


def test_validate_request(mock_create_job_task):
    validate_request(mock_create_job_task)


def test_validate_request_when_missing_fields():
    with pytest.raises(Exception) as err:
        validate_request({"world_id": ""})
    assert (
            str(err.value) == "Required fields missing from request payload: ['questionnaire']"
    )


@mock.patch("cloud_functions.create_questionnaire_case_tasks.append_uacs_to_retained_case")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.get_world_ids")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.get_questionnaire_case_model_list")
@mock.patch("client.bus.BusClient.get_uacs_by_case_id")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.filter_cases")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.run_async_tasks")
def test_create_case_tasks_for_questionnaire(
        mock_run_async_tasks,
        mock_filter_cases,
        mock_get_uacs_by_case_id,
        mock_get_questionnaire_case_model_list,
        mock_get_world_ids,
        mock_append_uacs_to_retained_case
):
    # arrange
    mock_request = flask.Request.from_values(json={"questionnaire": "LMS2101_AA1"})
    config = config_helper.get_default_config()
    mock_get_questionnaire_case_model_list.return_value = [
        QuestionnaireCaseModel(serial_number = "10010"), 
        QuestionnaireCaseModel(serial_number = "10012")]
    mock_filter_cases.return_value = [QuestionnaireCaseModel(serial_number = "10010")]
    mock_get_uacs_by_case_id.return_value = {
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
    mock_append_uacs_to_retained_case.return_value = [QuestionnaireCaseModel(
                serial_number = "10010",
                uac_chunks = UacChunks(uac1 = "8176", uac2 = "4726", uac3 = "3991"))]
    
    mock_get_world_ids.return_value = "1", [QuestionnaireCaseModel(serial_number = "10010")]
    # act
    result = create_questionnaire_case_tasks(mock_request, config)

    # assert
    mock_get_questionnaire_case_model_list.assert_called_with("LMS2101_AA1", config)
    mock_get_world_ids.assert_called_with(config, [QuestionnaireCaseModel(
                serial_number = "10010",
                uac_chunks = UacChunks(uac1 = "8176", uac2 = "4726", uac3 = "3991"))])
    mock_filter_cases.assert_called_with([
        QuestionnaireCaseModel(serial_number = "10010"), 
        QuestionnaireCaseModel(serial_number = "10012")])
    mock_run_async_tasks.assert_called_once()
    kwargs = mock_run_async_tasks.call_args.kwargs
    assert kwargs['cloud_function'] == "totalmobile_job_cloud_function"
    assert kwargs['queue_id'] == "totalmobile_jobs_queue_id"
    assert len(kwargs['tasks']) == 1
    task = kwargs['tasks'][0]
    assert task[0][0:3] == "LMS"
    print(json.loads(task[1]))

    assert json.loads(task[1]) == {'questionnaire': 'LMS2101_AA1', 'world_id': '1', 'case': {'serial_number': '10010', 'data_model_name': '', 'survey_type': '', 'wave': '', 'address_line_1': '', 'address_line_2': '', 'address_line_3': '', 'county': '', 'town': '', 'postcode': '', 'telephone_number_1': '', 'telephone_number_2': '', 'appointment_telephone_number': '', 'outcome_code': '', 'latitude': '', 'longitude': '', 'priority': '', 'field_region': '', 'field_team': '', 'wave_com_dte': '', 'uac_chunks': {'uac1': '', 'uac2': '', 'uac3': ''}}}
    assert result == "Done"


@mock.patch("cloud_functions.create_questionnaire_case_tasks.get_questionnaire_case_model_list")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.run_async_tasks")
def test_create_questionnaire_case_tasks_when_no_cases(
        mock_run_async_tasks,
        mock_get_questionnaire_case_model_list,
):
    # arrange
    mock_request = flask.Request.from_values(json={"questionnaire": "LMS2101_AA1"})
    config = config_helper.get_default_config()
    mock_get_questionnaire_case_model_list.return_value = []

    # act
    result = create_questionnaire_case_tasks(mock_request, config)

    # assert
    mock_run_async_tasks.assert_not_called()
    assert result == "Exiting as no cases to send for questionnaire LMS2101_AA1"


@mock.patch("cloud_functions.create_questionnaire_case_tasks.get_questionnaire_case_model_list")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.filter_cases")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.run_async_tasks")
def test_create_questionnaire_case_tasks_when_no_cases_after_filtering(
        mock_run_async_tasks,
        mock_filter_cases,
        mock_get_questionnaire_case_model_list,
):
    # arrange
    mock_request = flask.Request.from_values(json={"questionnaire": "LMS2101_AA1"})
    config = config_helper.get_default_config()
    mock_get_questionnaire_case_model_list.return_value = [QuestionnaireCaseModel(serial_number = "10010")]
    mock_filter_cases.return_value = []
    # act
    result = create_questionnaire_case_tasks(mock_request, config)

    # assert
    mock_run_async_tasks.assert_not_called()
    assert result == "Exiting as no cases to send after filtering for questionnaire LMS2101_AA1"


def test_create_questionnaire_case_tasks_errors_if_misssing_questionnaire():
    # arrange
    mock_request = flask.Request.from_values(json={"blah": "blah"})
    config = config_helper.get_default_config()
    # assert
    with pytest.raises(Exception) as err:
        create_questionnaire_case_tasks(mock_request, config)
    assert (
            str(err.value) == "Required fields missing from request payload: ['questionnaire']"
    )


@mock.patch("cloud_functions.create_questionnaire_case_tasks.get_world_ids")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.get_questionnaire_case_model_list")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.filter_cases")
def test_get_wave_from_questionnaire_name_errors_for_non_lms_questionnaire(
        mock_filter_cases,
        mock_get_questionnaire_case_model_list,
        mock_get_world_ids,
):
    # arrange
    config = config_helper.get_default_config()
    mock_request = flask.Request.from_values(json={"questionnaire": "OPN2101A"})
    mock_get_questionnaire_case_model_list.return_value = [QuestionnaireCaseModel(serial_number = "10010"), QuestionnaireCaseModel(serial_number = "10012")]
    mock_get_world_ids.return_value = "1"
    mock_filter_cases.return_value = [QuestionnaireCaseModel(serial_number = "10010")]

    # act
    with pytest.raises(Exception) as err:
        create_questionnaire_case_tasks(mock_request, config)

    # assert
    assert str(err.value) == "Invalid format for questionnaire name: OPN2101A"


def test_get_wave_from_questionnaire_name():
    assert get_wave_from_questionnaire_name("LMS2101_AA1") == "1"
    assert get_wave_from_questionnaire_name("LMS1234_ZZ2") == "2"


def test_get_wave_from_questionnaire_name_with_invalid_format_raises_error():
    with pytest.raises(Exception) as err:
        get_wave_from_questionnaire_name("ABC1234_AA1")
    assert str(err.value) == "Invalid format for questionnaire name: ABC1234_AA1"


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_world_ids_correctly_maps_a_case_field_region_to_a_world_id(_mock_optimise_client):
    # arrange
    config = config_helper.get_default_config()

    filtered_cases = [QuestionnaireCaseModel(field_region = "Region 1"),
                      QuestionnaireCaseModel(field_region = "Region 2"),
                      QuestionnaireCaseModel(field_region = "Region 4")]    

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

    world_ids, new_filtered_cases = get_world_ids(config, filtered_cases)

    # assert
    assert world_ids == [
        "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "3fa85f64-5717-4562-b3fc-2c963f66afa7",
        "3fa85f64-5717-4562-b3fc-2c963f66afa9",
    ]

    assert new_filtered_cases == [
        QuestionnaireCaseModel(field_region = "Region 1"),
        QuestionnaireCaseModel(field_region = "Region 2"),
        QuestionnaireCaseModel(field_region = "Region 4")
    ]


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_world_ids_logs_a_console_error_when_given_an_unknown_world(_mock_optimise_client, caplog):
    # arrange
    config = config_helper.get_default_config()

    filtered_cases = [QuestionnaireCaseModel(field_region = "Risca")]    

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
    get_world_ids(config, filtered_cases)

    # assert
    assert ('root', logging.WARNING, 'Unsupported world: Risca') in caplog.record_tuples


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_world_ids_logs_a_console_error_and_returns_data_when_given_an_unknown_world_and_a_known_world(
        _mock_optimise_client, caplog):
    # arrange
    config = config_helper.get_default_config()

    filtered_cases = [QuestionnaireCaseModel(field_region = "Risca"),
                      QuestionnaireCaseModel(field_region = "Region 1")]    

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
    world_ids, new_filtered_cases = get_world_ids(config, filtered_cases)

    # assert
    assert len(world_ids) == len(new_filtered_cases)
    assert world_ids == ["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
    assert new_filtered_cases == [QuestionnaireCaseModel(field_region = "Region 1")]
    assert ('root', logging.WARNING, 'Unsupported world: Risca') in caplog.record_tuples


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_world_ids_logs_a_console_error_when_field_region_is_missing(_mock_optimise_client, caplog):
    # arrange
    config = config_helper.get_default_config()

    filtered_cases = [QuestionnaireCaseModel(field_region = "")]    

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
    get_world_ids(config, filtered_cases)

    # assert
    assert ('root', logging.WARNING, 'Case rejected. Missing Field Region') in caplog.record_tuples


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_world_ids_logs_a_console_error_and_returns_data_when_given_an_unknown_world_and_a_known_world_and_a_known_world(
        _mock_optimise_client, caplog):
    # arrange
    config = config_helper.get_default_config()

    filtered_cases = [QuestionnaireCaseModel(field_region = ""),
                      QuestionnaireCaseModel(field_region = "Region 1")]    

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
    world_ids, new_filtered_cases = get_world_ids(config, filtered_cases)

    # assert
    assert len(world_ids) == len(new_filtered_cases)
    assert world_ids == ["3fa85f64-5717-4562-b3fc-2c963f66afa6"]
    assert new_filtered_cases == [QuestionnaireCaseModel(field_region = "Region 1")]
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

    filtered_cases = [QuestionnaireCaseModel(
        serial_number = "10030", 
        telephone_number_1 = "", 
        telephone_number_2 = "", 
        appointment_telephone_number = "",
        wave = "1", 
        priority = "1", 
        outcome_code = "310")]    

    result = append_uacs_to_retained_case(filtered_cases, case_uacs)
    assert result == [QuestionnaireCaseModel(
                serial_number = "10030", 
                telephone_number_1 = "", 
                telephone_number_2 = "", 
                appointment_telephone_number = "",
                wave = "1", 
                priority = "1", 
                outcome_code = "310",
                uac_chunks = UacChunks(
                    uac1 = "8176",
                    uac2 = "4726",
                    uac3 = "3993"
                ))]  


def test_uacs_with_blank_values_are_appended_to_case_data_when_case_id_not_found_in_bus():
    case_uacs = {
        "10000": {
            "instrument_name": "OPN2101A",
            "case_id": "10000",
            "uac_chunks": {
                "uac1": "8176",
                "uac2": "4726",
                "uac3": "3991"
            },
            "full_uac": "817647263991"
        },
    }

    filtered_cases = [QuestionnaireCaseModel(
        serial_number = "10030", 
        telephone_number_1 = "", 
        telephone_number_2 = "", 
        appointment_telephone_number = "",
        wave = "1", 
        priority = "1", 
        outcome_code = "310")]    


    result = append_uacs_to_retained_case(filtered_cases, case_uacs)
    assert result == [QuestionnaireCaseModel(
                serial_number = "10030", 
                telephone_number_1 = "", 
                telephone_number_2 = "", 
                appointment_telephone_number = "",
                wave = "1", 
                priority = "1", 
                outcome_code = "310",
                uac_chunks = UacChunks(
                    uac1 = "",
                    uac2 = "",
                    uac3 = ""
                ))]   
    

def test_an_error_is_logged_when_the_case_id_is_not_found_in_bus(caplog):
    case_uacs = {
        "10000": {
            "instrument_name": "OPN2101A",
            "case_id": "10000",
            "uac_chunks": {
                "uac1": "8176",
                "uac2": "4726",
                "uac3": "3991"
            },
            "full_uac": "817647263991"
        },
    }

    filtered_cases = [QuestionnaireCaseModel(
        serial_number = "10030", 
        telephone_number_1 = "", 
        telephone_number_2 = "", 
        appointment_telephone_number = "",
        wave = "1", 
        priority = "1", 
        outcome_code = "310")]    

    result = append_uacs_to_retained_case(filtered_cases, case_uacs)
    assert ('root', logging.WARNING, 'Serial number 10030 not found in BUS') in caplog.record_tuples
