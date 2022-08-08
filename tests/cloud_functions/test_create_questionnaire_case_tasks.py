import json
from unittest import mock

import flask
import pytest
import logging
from models.questionnaire_case_model import QuestionnaireCaseModel, UacChunks
from models.totalmobile_case_model import TotalMobileCaseModel

from tests.helpers import config_helper
from client.optimise import OptimiseClient
from cloud_functions.create_questionnaire_case_tasks import (
    create_questionnaire_case_tasks,
    create_task_name,
    map_totalmobile_job_models,
    validate_request,
    get_cases_with_valid_world_ids
)
from models.totalmobile_job_model import TotalmobileJobModel
from tests.helpers.questionnaire_case_model_helper import populated_case_model


def test_create_task_name_returns_correct_name_when_called():
    questionnaire_case_model = populated_case_model()
    questionnaire_case_model.case_id = "90001"
    questionnaire_name = "OPN2101A"
    totalmobile_case_model = TotalMobileCaseModel.import_case(questionnaire_name, questionnaire_case_model)
    model = TotalmobileJobModel("OPN2101A", "world", "90001", totalmobile_case_model.to_payload())

    assert create_task_name(model).startswith("OPN2101A-90001-")


def test_create_task_name_returns_unique_name_each_time_when_passed_the_same_model():
    questionnaire_case_model = populated_case_model()
    questionnaire_case_model.case_id = "90001"
    model = TotalmobileJobModel("OPN2101A", "world", "90001", questionnaire_case_model.to_dict())

    assert create_task_name(model) != create_task_name(model)


def test_map_totalmobile_job_models_maps_the_correct_list_of_models():
    # arrange
    questionnaire_name = "OPN2101A"

    case_data = [
        populated_case_model(case_id="10010", outcome_code="110"),
        populated_case_model(case_id="10020", outcome_code="120"),
        populated_case_model(case_id="10030", outcome_code="130")
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
        TotalmobileJobModel(questionnaire='OPN2101A', world_id='3fa85f64-5717-4562-b3fc-2c963f66afa6', case_id='10010',
                            payload={'identity': {'reference': 'OPN2101A.10010'},
                                     'description': 'Study: OPN2101A\nCase ID: 10010', 'origin': 'ONS', 'duration': 15,
                                     'workType': 'LMS', 'skills': [{'identity': {'reference': 'LMS'}}],
                                     'dueDate': '01 - 01 - 2023', 'location': {
                                    'addressDetail': {'addressLine1': '12 Blaise Street', 'addressLine2': 'Blaise Hill',
                                                      'addressLine3':
                                                          'Blaiseville',
                                                      'addressLine4': 'Gwent', 'addressLine5': 'Newport',
                                                      'postCode': 'FML134D', 'coordinates': {
                                            'latitude': '10020202', 'longitude': '34949494'}}},
                                     'contact': {'name': 'FML134D'}, 'additionalProperties': [
                                    {'name': 'surveyName', 'value': 'LM2007'}, {'name': 'tla', 'value': 'LMS'},
                                    {'name': 'wave', 'value': '1'}, {'name': 'priority', 'value': '1'},
                                    {'name': 'fieldTeam', 'value': 'B - Team'}, {'name': 'uac1', 'value': '3456'},
                                    {'name': 'uac2', 'value': '3453'}, {'name': 'uac3', 'value': '4546'}]}),
        TotalmobileJobModel(questionnaire='OPN2101A', world_id='3fa85f64-5717-4562-b3fc-2c963f66afa7', case_id='10020',
                            payload={'identity': {'reference': 'OPN2101A.10020'},
                                     'description': 'Study: OPN2101A\nCase ID: 10020', 'origin': 'ONS', 'duration': 15,
                                     'workType': 'LMS', 'skills': [{'identity': {'reference': 'LMS'}}],
                                     'dueDate': '01 - 01 - 2023', 'location': {
                                    'addressDetail': {'addressLine1': '12 Blaise Street', 'addressLine2': 'Blaise Hill',
                                                      'addressLine3':
                                                          'Blaiseville',
                                                      'addressLine4': 'Gwent', 'addressLine5': 'Newport',
                                                      'postCode': 'FML134D', 'coordinates': {
                                            'latitude': '10020202', 'longitude': '34949494'}}},
                                     'contact': {'name': 'FML134D'}, 'additionalProperties': [
                                    {'name': 'surveyName', 'value': 'LM2007'}, {'name': 'tla', 'value': 'LMS'},
                                    {'name': 'wave', 'value': '1'},
                                    {'name': 'priority', 'value': '1'}, {'name': 'fieldTeam', 'value': 'B - Team'},
                                    {'name': 'uac1', 'value': '3456'},
                                    {'name': 'uac2', 'value': '3453'}, {'name': 'uac3', 'value': '4546'}]}),
        TotalmobileJobModel(questionnaire='OPN2101A', world_id='3fa85f64-5717-4562-b3fc-2c963f66afa9', case_id='10030',
                            payload={'identity': {'reference': 'OPN2101A.10030'},
                                     'description': 'Study: OPN2101A\nCase ID: 10030', 'origin': 'ONS', 'duration': 15,
                                     'workType': 'LMS', 'skills': [{'identity': {'reference': 'LMS'}}],
                                     'dueDate': '01 - 01 - 2023', 'location': {
                                    'addressDetail': {'addressLine1': '12 Blaise Street', 'addressLine2': 'Blaise Hill',
                                                      'addressLine3':
                                                          'Blaiseville',
                                                      'addressLine4': 'Gwent', 'addressLine5': 'Newport',
                                                      'postCode': 'FML134D', 'coordinates': {
                                            'latitude': '10020202', 'longitude': '34949494'}}},
                                     'contact': {'name': 'FML134D'}, 'additionalProperties': [
                                    {'name': 'surveyName', 'value': 'LM2007'}, {'name': 'tla', 'value': 'LMS'},
                                    {'name': 'wave', 'value': '1'}, {'name': 'priority', 'value': '1'},
                                    {'name': 'fieldTeam', 'value': 'B - Team'}, {'name': 'uac1', 'value': '3456'},
                                    {'name': 'uac2',
                                     'value': '3453'}, {'name': 'uac3', 'value': '4546'}]}),
    ]


def test_validate_request(mock_create_job_task):
    validate_request(mock_create_job_task)


def test_validate_request_when_missing_fields():
    with pytest.raises(Exception) as err:
        validate_request({"world_id": ""})
    assert (
            str(err.value) == "Required fields missing from request payload: ['questionnaire']"
    )


@mock.patch("services.world_id_service.get_world_ids")
@mock.patch("services.questionnaire_service.get_eligible_cases")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.run_async_tasks")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.get_cases_with_valid_world_ids")
def test_create_case_tasks_for_questionnaire(
        mock_get_cases_with_valid_world_ids,
        mock_run_async_tasks,
        mock_get_eligible_cases,
        mock_get_world_ids,
):
    # arrange
    config = config_helper.get_default_config()
    mock_request = flask.Request.from_values(json={"questionnaire": "LMS2101_AA1"})

    mock_get_eligible_cases.return_value = [
        populated_case_model(
            case_id="10010",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310",
            uac_chunks=UacChunks(
                uac1="8176",
                uac2="4726",
                uac3="3991"
            )
        ),
    ]

    mock_get_world_ids.return_value = {
        "Region 1": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }

    mock_get_cases_with_valid_world_ids.return_value = [
        populated_case_model(
            case_id="10010",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310",
            uac_chunks=UacChunks(
                uac1="8176",
                uac2="4726",
                uac3="3991"
            )
        )]

    # act
    result = create_questionnaire_case_tasks(mock_request, config)

    # assert
    mock_get_world_ids.assert_called_with(config)
    mock_get_eligible_cases.assert_called_with("LMS2101_AA1", config)

    mock_run_async_tasks.assert_called_once()
    kwargs = mock_run_async_tasks.call_args.kwargs
    assert kwargs['cloud_function'] == "totalmobile_job_cloud_function"
    assert kwargs['queue_id'] == "totalmobile_jobs_queue_id"
    assert len(kwargs['tasks']) == 1
    task = kwargs['tasks'][0]
    assert task[0][0:3] == "LMS"
    assert json.loads(task[1]) == {
        'questionnaire': 'LMS2101_AA1',
        'world_id': 'Region 1',
        'case': {
            'qiD.Serial_Number': '10010',
            'dataModelName': '',
            'qDataBag.TLA': '',
            'qDataBag.Wave': '1',
            'qDataBag.Prem1': '',
            'qDataBag.Prem2': '',
            'qDataBag.Prem3': '',
            'qDataBag.District': '',
            'qDataBag.PostTown': '',
            'qDataBag.PostCode': '',
            'qDataBag.TelNo': '',
            'qDataBag.TelNo2': '',
            'telNoAppt': '',
            'hOut': '310',
            'qDataBag.UPRN_Latitude': '',
            'qDataBag.UPRN_Longitude': '',
            'qDataBag.Priority': '1',
            'qDataBag.FieldRegion': '',
            'qDataBag.FieldTeam': '',
            'qDataBag.WaveComDTE': '',
            'uac_chunks': {
                'uac1': '8176',
                'uac2': '4726',
                'uac3': '3991'
            }
        }
    }
    assert result == "Done"


@mock.patch("services.questionnaire_service.get_eligible_cases")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.run_async_tasks")
def test_create_questionnaire_case_tasks_when_no_eligible_cases(
        mock_run_async_tasks,
        mock_get_eligible_cases
):
    # arrange
    mock_request = flask.Request.from_values(json={"questionnaire": "LMS2101_AA1"})
    config = config_helper.get_default_config()
    mock_get_eligible_cases.return_value = []

    # act
    result = create_questionnaire_case_tasks(mock_request, config)

    # assert
    mock_run_async_tasks.assert_not_called()
    assert result == "Exiting as no eligible cases to send for questionnaire LMS2101_AA1"


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


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_cases_with_valid_world_ids_logs_a_console_error_when_given_an_unknown_region(_mock_optimise_client,
                                                                                          caplog):
    filtered_cases = [populated_case_model(field_region="Risca")]
    world_ids = {
        "Region 1": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }

    get_cases_with_valid_world_ids(filtered_cases, world_ids)

    assert ('root', logging.WARNING, 'Unsupported world: Risca') in caplog.record_tuples


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_cases_with_valid_world_ids_logs_a_console_error_and_returns_data_when_given_an_unknown_world_and_a_known_world(
        _mock_optimise_client, caplog):
    filtered_cases = [populated_case_model(field_region="Risca"),
                      populated_case_model(field_region="Region 1")]
    world_ids = {
        "Region 1": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }

    cases_with_valid_world_ids = get_cases_with_valid_world_ids(filtered_cases, world_ids)

    assert len(cases_with_valid_world_ids) == 1
    assert cases_with_valid_world_ids == [populated_case_model(field_region="Region 1")]
    assert ('root', logging.WARNING, 'Unsupported world: Risca') in caplog.record_tuples


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_cases_with_valid_world_ids_logs_a_console_error_when_field_region_is_an_empty_value(_mock_optimise_client,
                                                                                                 caplog):
    filtered_cases = [populated_case_model(field_region="")]
    world_ids = {
        "Region 1": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }

    get_cases_with_valid_world_ids(filtered_cases, world_ids)

    assert ('root', logging.WARNING, 'Case rejected. Missing Field Region') in caplog.record_tuples


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_world_ids_logs_a_console_error_and_returns_data_when_given_an_unknown_world_and_a_known_world_and_a_known_world(
        _mock_optimise_client, caplog):
    config = config_helper.get_default_config()

    filtered_cases = [populated_case_model(field_region=""),
                      populated_case_model(field_region="Region 1")]

    world_ids = {
        "Region 1": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    }

    cases_with_valid_world_ids = get_cases_with_valid_world_ids(filtered_cases, world_ids)

    assert len(cases_with_valid_world_ids) == 1
    assert cases_with_valid_world_ids == [populated_case_model(field_region="Region 1")]
    assert ('root', logging.WARNING, 'Case rejected. Missing Field Region') in caplog.record_tuples
