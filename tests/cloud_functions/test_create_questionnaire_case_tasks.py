import json
import logging
from unittest import mock
from unittest.mock import create_autospec

import flask
import pytest

from client.optimise import OptimiseClient
from cloud_functions.create_questionnaire_case_tasks import (
    create_questionnaire_case_tasks,
    get_cases_with_valid_world_ids,
    map_totalmobile_job_models,
    validate_request,
)
from models.blaise.blaise_case_information_model import UacChunks
from models.totalmobile.totalmobile_outgoing_job_payload_model import (
    TotalMobileOutgoingJobPayloadModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.questionnaire_service import QuestionnaireService
from services.totalmobile_service import TotalmobileService
from tests.helpers import config_helper
from tests.helpers.get_blaise_case_model_helper import get_populated_case_model


def test_map_totalmobile_job_models_maps_the_correct_list_of_models():
    # arrange
    questionnaire_name = "LMS2101_AA1"

    case_data = [
        get_populated_case_model(
            case_id="10010", outcome_code=110, field_region="region1"
        ),
        get_populated_case_model(
            case_id="10020", outcome_code=120, field_region="region2"
        ),
        get_populated_case_model(
            case_id="10030", outcome_code=130, field_region="region3"
        ),
    ]

    world_model = TotalmobileWorldModel(
        worlds=[
            World(region="region1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="region2", id="3fa85f64-5717-4562-b3fc-2c963f66afa7"),
            World(region="region3", id="3fa85f64-5717-4562-b3fc-2c963f66afa9"),
        ]
    )

    # act
    result = map_totalmobile_job_models(case_data, world_model, questionnaire_name)

    # assert
    assert len(result) == 3

    assert result[0].questionnaire == "LMS2101_AA1"
    assert result[0].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    assert result[0].case_id == "10010"
    assert (
        result[0].payload
        == TotalMobileOutgoingJobPayloadModel.import_case(
            questionnaire_name, case_data[0]
        ).to_payload()
    )

    assert result[1].questionnaire == "LMS2101_AA1"
    assert result[1].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    assert result[1].case_id == "10020"
    assert (
        result[1].payload
        == TotalMobileOutgoingJobPayloadModel.import_case(
            questionnaire_name, case_data[1]
        ).to_payload()
    )

    assert result[2].questionnaire == "LMS2101_AA1"
    assert result[2].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa9"
    assert result[2].case_id == "10030"
    assert (
        result[2].payload
        == TotalMobileOutgoingJobPayloadModel.import_case(
            questionnaire_name, case_data[2]
        ).to_payload()
    )


def test_validate_request(mock_create_job_task):
    validate_request(mock_create_job_task)


def test_validate_request_when_missing_fields():
    with pytest.raises(Exception) as err:
        validate_request({"world_id": ""})
    assert (
        str(err.value)
        == "Required fields missing from request payload: ['questionnaire']"
    )


@mock.patch.object(QuestionnaireService, "get_eligible_cases")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.run_async_tasks")
@mock.patch(
    "cloud_functions.create_questionnaire_case_tasks.get_cases_with_valid_world_ids"
)
def test_create_case_tasks_for_questionnaire(
    mock_get_cases_with_valid_world_ids,
    mock_run_async_tasks,
    mock_get_eligible_cases,
):
    # arrange
    config = config_helper.get_default_config()
    total_mobile_service_mock = create_autospec(TotalmobileService)
    total_mobile_service_mock.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6")]
    )

    request_mock = flask.Request.from_values(json={"questionnaire": "LMS2101_AA1"})

    questionnaire_cases = [
        get_populated_case_model(
            case_id="10010",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code=310,
            uac_chunks=UacChunks(uac1="8176", uac2="4726", uac3="3991"),
            field_region="Region 1",
        ),
    ]

    mock_get_eligible_cases.return_value = questionnaire_cases

    mock_get_cases_with_valid_world_ids.return_value = [
        get_populated_case_model(
            case_id="10010",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code=310,
            uac_chunks=UacChunks(uac1="8176", uac2="4726", uac3="3991"),
            field_region="Region 1",
        )
    ]

    # act
    result = create_questionnaire_case_tasks(
        request_mock, config, total_mobile_service_mock
    )

    # assert
    mock_get_eligible_cases.assert_called_with("LMS2101_AA1")

    mock_run_async_tasks.assert_called_once()
    kwargs = mock_run_async_tasks.call_args.kwargs
    assert kwargs["cloud_function"] == "totalmobile_job_cloud_function"
    assert kwargs["queue_id"] == "totalmobile_jobs_queue_id"
    assert len(kwargs["tasks"]) == 1
    task = kwargs["tasks"][0]
    assert task[0][0:3] == "LMS"
    print(json.loads(task[1]))
    assert json.loads(task[1]) == {
        "questionnaire": "LMS2101_AA1",
        "world_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "case_id": "10010",
        "payload": TotalMobileOutgoingJobPayloadModel.import_case(
            "LMS2101_AA1", questionnaire_cases[0]
        ).to_payload(),
    }
    assert result == "Done"


@mock.patch.object(QuestionnaireService, "get_eligible_cases")
@mock.patch("cloud_functions.create_questionnaire_case_tasks.run_async_tasks")
def test_create_questionnaire_case_tasks_when_no_eligible_cases(
    mock_run_async_tasks, mock_get_eligible_cases
):
    # arrange
    request_mock = flask.Request.from_values(json={"questionnaire": "LMS2101_AA1"})
    total_mobile_service_mock = create_autospec(TotalmobileService)

    config = config_helper.get_default_config()
    mock_get_eligible_cases.return_value = []

    # act
    result = create_questionnaire_case_tasks(
        request_mock, config, total_mobile_service_mock
    )

    # assert
    mock_run_async_tasks.assert_not_called()
    assert (
        result == "Exiting as no eligible cases to send for questionnaire LMS2101_AA1"
    )


def test_create_questionnaire_case_tasks_errors_if_missing_questionnaire():
    # arrange
    request_mock = flask.Request.from_values(json={"blah": "blah"})
    total_mobile_service_mock = create_autospec(TotalmobileService)

    config = config_helper.get_default_config()
    # assert
    with pytest.raises(Exception) as err:
        create_questionnaire_case_tasks(request_mock, config, total_mobile_service_mock)
    assert (
        str(err.value)
        == "Required fields missing from request payload: ['questionnaire']"
    )


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_cases_with_valid_world_ids_logs_a_console_error_when_given_an_unknown_region(
    _mock_optimise_client, caplog
):
    filtered_cases = [get_populated_case_model(field_region="Risca")]
    world_model = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6")]
    )

    get_cases_with_valid_world_ids(filtered_cases, world_model)

    assert ("root", logging.WARNING, "Unsupported world: Risca") in caplog.record_tuples


@mock.patch.object(OptimiseClient, "get_worlds")
def test_get_cases_with_valid_world_ids_logs_a_console_error_and_returns_data_when_given_an_unknown_world_and_a_known_world(
    _mock_optimise_client, caplog
):
    filtered_cases = [
        get_populated_case_model(field_region="Risca"),
        get_populated_case_model(field_region="Region 1"),
    ]
    world_model = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6")]
    )

    cases_with_valid_world_ids = get_cases_with_valid_world_ids(
        filtered_cases, world_model
    )

    assert len(cases_with_valid_world_ids) == 1
    assert cases_with_valid_world_ids == [
        get_populated_case_model(field_region="Region 1")
    ]
    assert ("root", logging.WARNING, "Unsupported world: Risca") in caplog.record_tuples


def test_get_cases_with_valid_world_ids_logs_a_console_error_when_field_region_is_an_empty_value(
    caplog,
):
    filtered_cases = [get_populated_case_model(field_region="")]
    world_model = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6")]
    )
    get_cases_with_valid_world_ids(filtered_cases, world_model)

    assert (
        "root",
        logging.WARNING,
        "Case rejected. Missing Field Region",
    ) in caplog.record_tuples


def test_get_world_ids_logs_a_console_error_and_returns_data_when_given_an_unknown_world_and_a_known_world_and_a_known_world(
    caplog,
):
    config = config_helper.get_default_config()

    filtered_cases = [
        get_populated_case_model(field_region=""),
        get_populated_case_model(field_region="Region 1"),
    ]

    world_model = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6")]
    )

    cases_with_valid_world_ids = get_cases_with_valid_world_ids(
        filtered_cases, world_model
    )

    assert len(cases_with_valid_world_ids) == 1
    assert cases_with_valid_world_ids == [
        get_populated_case_model(field_region="Region 1")
    ]
    assert (
        "root",
        logging.WARNING,
        "Case rejected. Missing Field Region",
    ) in caplog.record_tuples
