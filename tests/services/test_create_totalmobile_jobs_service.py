import json
import logging
from typing import Dict
from unittest.mock import Mock

import pytest

from client.bus import Uac
from models.blaise.questionnaire_uac_model import QuestionnaireUacModel, UacChunks
from models.totalmobile.totalmobile_outgoing_create_job_payload_model import (
    TotalMobileOutgoingCreateJobPayloadModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.create_totalmobile_jobs_service import CreateTotalmobileJobsService
from tests.helpers.get_blaise_case_model_helper import get_populated_case_model


@pytest.fixture()
def mock_totalmobile_service():
    return Mock()


@pytest.fixture()
def mock_questionnaire_service():
    return Mock()


@pytest.fixture()
def mock_uac_service():
    return Mock()


@pytest.fixture()
def mock_cloud_task_service():
    return Mock()


@pytest.fixture()
def service(
    mock_totalmobile_service,
    mock_questionnaire_service,
    mock_uac_service,
    mock_cloud_task_service,
) -> CreateTotalmobileJobsService:
    return CreateTotalmobileJobsService(
        totalmobile_service=mock_totalmobile_service,
        questionnaire_service=mock_questionnaire_service,
        uac_service=mock_uac_service,
        cloud_task_service=mock_cloud_task_service,
    )


def test_check_questionnaire_release_date_logs_when_there_are_no_questionnaires_for_release(
    mock_questionnaire_service,
    service: CreateTotalmobileJobsService,
    caplog,
):
    # arrange
    mock_questionnaire_service.get_questionnaires_with_totalmobile_release_date_of_today.return_value = (
        []
    )
    mock_questionnaire_service.get_wave_from_questionnaire_name.return_value = "1"
    mock_questionnaire_service.get_cases.return_value = []
    # act
    result = service.create_totalmobile_jobs()

    # assert
    assert result == "There are no questionnaires with a release date of today"
    with caplog.at_level(logging.INFO):
        service.create_totalmobile_jobs()
    assert (
        "root",
        logging.INFO,
        "There are no questionnaires with a release date of today",
    ) in caplog.record_tuples


def test_map_totalmobile_job_models_maps_the_correct_list_of_models(
    mock_totalmobile_service, mock_uac_service, service: CreateTotalmobileJobsService
):
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

    uac_data_dictionary: Dict[str, Uac] = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {"uac1": "8175", "uac2": "4725", "uac3": "3990"},
            "full_uac": "817647263991",
        },
        "10020": {
            "instrument_name": "OPN2101A",
            "case_id": "10020",
            "uac_chunks": {"uac1": "4175", "uac2": "5725", "uac3": "6990"},
            "full_uac": "417657266991",
        },
    }

    questionnaire_uac_model = QuestionnaireUacModel.import_uac_data(uac_data_dictionary)
    mock_uac_service.get_questionnaire_uac_model.return_value = questionnaire_uac_model

    world_model = TotalmobileWorldModel(
        worlds=[
            World(region="region1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="region2", id="3fa85f64-5717-4562-b3fc-2c963f66afa7"),
            World(region="region3", id="3fa85f64-5717-4562-b3fc-2c963f66afa9"),
        ]
    )

    mock_totalmobile_service.get_world_model.return_value = world_model

    # act
    result = service.map_totalmobile_job_models(
        questionnaire_name=questionnaire_name, cases=case_data
    )

    # assert
    assert len(result) == 3

    assert result[0].questionnaire == "LMS2101_AA1"
    assert result[0].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    assert result[0].case_id == "10010"
    assert (
        result[0].payload
        == TotalMobileOutgoingCreateJobPayloadModel.import_case(
            questionnaire_name,
            case_data[0],
            questionnaire_uac_model.get_uac_chunks("10010"),
        ).to_payload()
    )
    assert result[0].payload["description"].startswith("UAC: 8175 4725 3990")

    assert result[1].questionnaire == "LMS2101_AA1"
    assert result[1].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    assert result[1].case_id == "10020"
    assert (
        result[1].payload
        == TotalMobileOutgoingCreateJobPayloadModel.import_case(
            questionnaire_name,
            case_data[1],
            questionnaire_uac_model.get_uac_chunks("10020"),
        ).to_payload()
    )
    assert result[1].payload["description"].startswith("UAC: 4175 5725 6990")

    assert result[2].questionnaire == "LMS2101_AA1"
    assert result[2].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa9"
    assert result[2].case_id == "10030"
    assert (
        result[2].payload
        == TotalMobileOutgoingCreateJobPayloadModel.import_case(
            questionnaire_name,
            case_data[2],
            questionnaire_uac_model.get_uac_chunks("10030"),
        ).to_payload()
    )
    assert result[2].payload["description"].startswith("UAC: \nDue Date")


def test_create_totalmobile_jobs_for_eligible_questionnaire_cases(
    mock_questionnaire_service,
    mock_totalmobile_service,
    mock_uac_service,
    mock_cloud_task_service,
    service: CreateTotalmobileJobsService,
):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    questionnaire_cases = [
        get_populated_case_model(
            case_id="10010",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            priority="1",
            outcome_code=310,
            field_region="Region 1",
        ),
    ]

    mock_questionnaire_service.get_eligible_cases.return_value = questionnaire_cases

    mock_questionnaire_service.get_wave_from_questionnaire_name.return_value = "1"
    mock_questionnaire_service.get_cases.return_value = []

    world_model = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6")]
    )

    mock_totalmobile_service.get_world_model.return_value = world_model

    uac_data_dictionary: Dict[str, Uac] = {
        "10010": {
            "instrument_name": "OPN2101A",
            "case_id": "10010",
            "uac_chunks": {"uac1": "8175", "uac2": "4725", "uac3": "3990"},
            "full_uac": "817647263991",
        },
        "10020": {
            "instrument_name": "OPN2101A",
            "case_id": "10020",
            "uac_chunks": {"uac1": "4175", "uac2": "5725", "uac3": "6990"},
            "full_uac": "417657266991",
        },
    }

    questionnaire_uac_model = QuestionnaireUacModel.import_uac_data(uac_data_dictionary)

    mock_uac_service.get_questionnaire_uac_model.return_value = questionnaire_uac_model

    # act
    result = service.create_totalmobile_jobs_for_eligible_questionnaire_cases(
        questionnaire_name=questionnaire_name
    )

    # assert
    mock_questionnaire_service.get_eligible_cases.assert_called_with("LMS2101_AA1")

    mock_cloud_task_service.create_and_run_tasks.assert_called_once()
    kwargs = mock_cloud_task_service.create_and_run_tasks.call_args.kwargs
    assert kwargs["cloud_function"] == "bts-create-totalmobile-jobs-processor"
    assert len(kwargs["task_request_models"]) == 1
    task_request_model = kwargs["task_request_models"][0]
    assert task_request_model.task_name.startswith("LMS")
    print(json.loads(task_request_model.task_body))
    assert json.loads(task_request_model.task_body) == {
        "questionnaire": "LMS2101_AA1",
        "world_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "case_id": "10010",
        "payload": TotalMobileOutgoingCreateJobPayloadModel.import_case(
            "LMS2101_AA1",
            questionnaire_cases[0],
            UacChunks(uac1="8175", uac2="4725", uac3="3990"),
        ).to_payload(),
    }
    assert result == "Done"


def test_create_cloud_tasks_when_no_eligible_cases(
    mock_questionnaire_service,
    mock_cloud_task_service,
    service: CreateTotalmobileJobsService,
):
    # arrange
    questionnaire_name = "LMS2101_AA1"

    mock_questionnaire_service.get_wave_from_questionnaire_name.return_value = "1"
    mock_questionnaire_service.get_eligible_cases.return_value = []

    # act
    result = service.create_totalmobile_jobs_for_eligible_questionnaire_cases(
        questionnaire_name=questionnaire_name
    )

    # assert
    mock_cloud_task_service.create_and_run_tasks.assert_not_called()
    assert (
        result == "Exiting as no eligible cases to send for questionnaire LMS2101_AA1"
    )
