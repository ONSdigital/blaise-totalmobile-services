import json
import logging
from datetime import datetime
from unittest import mock
from unittest.mock import create_autospec

from google.cloud import datastore

from appconfig import Config
from client.optimise import OptimiseClient
from cloud_functions.create_totalmobile_jobs_trigger import (
    create_questionnaire_case_task_name,
    create_questionnaire_case_tasks,
    create_totalmobile_jobs_trigger,
    get_cases_with_valid_world_ids,
    get_questionnaires_with_release_date_of_today,
    map_questionnaire_case_task_models,
    map_totalmobile_job_models,
)
from models.blaise.blaise_case_information_model import UacChunks
from models.cloud_tasks.questionnaire_case_cloud_task_model import (
    QuestionnaireCaseTaskModel,
)
from models.totalmobile.totalmobile_outgoing_job_payload_model import (
    TotalMobileOutgoingJobPayloadModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.questionnaire_service import QuestionnaireService
from services.totalmobile_service import TotalmobileService
from tests.helpers import config_helper
from tests.helpers.get_blaise_case_model_helper import get_populated_case_model


def entity_builder(key, questionnaire, tmreleasedate):
    entity = datastore.Entity(datastore.Key("TmReleaseDate", key, project="test"))
    entity["questionnaire"] = questionnaire
    entity["tmreleasedate"] = tmreleasedate
    return entity


@mock.patch("cloud_functions.create_totalmobile_jobs_trigger.get_datastore_records")
def test_get_questionnaires_with_release_date_of_today_only_returns_questionnaires_with_todays_date(
    mock_get_datastore_records,
):
    # arrange
    mock_datastore_entity = [
        entity_builder(1, "LMS2111Z", datetime.today()),
        entity_builder(2, "LMS2000Z", datetime(2021, 12, 31)),
    ]
    mock_get_datastore_records.return_value = mock_datastore_entity

    # act
    result = get_questionnaires_with_release_date_of_today()

    # assert
    assert result == ["LMS2111Z"]


@mock.patch("cloud_functions.create_totalmobile_jobs_trigger.get_datastore_records")
def test_get_questionnaires_with_release_date_of_today_returns_an_empty_list_when_there_are_no_release_dates_for_today(
    mock_get_datastore_records,
):
    # arrange
    mock_datastore_entity = [
        entity_builder(1, "LMS2111Z", datetime(2021, 12, 31)),
        entity_builder(2, "LMS2000Z", datetime(2021, 12, 31)),
    ]
    mock_get_datastore_records.return_value = mock_datastore_entity

    # act
    result = get_questionnaires_with_release_date_of_today()

    # assert
    assert result == []


@mock.patch("cloud_functions.create_totalmobile_jobs_trigger.get_datastore_records")
def test_get_questionnaires_with_release_date_of_today_returns_an_empty_list_when_there_are_no_records_in_datastore(
    mock_get_datastore_records,
):
    # arrange
    mock_get_datastore_records.return_value = []

    # act
    result = get_questionnaires_with_release_date_of_today()

    # assert
    assert result == []


@mock.patch(
    "cloud_functions.create_totalmobile_jobs_trigger.get_questionnaires_with_release_date_of_today"
)
def test_check_questionnaire_release_date_logs_when_there_are_no_questionnaires_for_release(
    mock_get_questionnaires_with_todays_release_date, caplog
):
    # arrange
    config = config_helper.get_default_config()
    mock_get_questionnaires_with_todays_release_date.return_value = []

    total_mobile_service_mock = create_autospec(TotalmobileService)
    questionnaire_service_mock = create_autospec(QuestionnaireService)

    questionnaire_service_mock.get_wave_from_questionnaire_name.return_value = "1"
    questionnaire_service_mock.get_cases.return_value = []
    # act
    result = create_totalmobile_jobs_trigger(
        config, total_mobile_service_mock, questionnaire_service_mock
    )

    # assert
    assert result == "There are no questionnaires with a release date of today"
    assert (
        "root",
        logging.INFO,
        "There are no questionnaires with a release date of today",
    ) in caplog.record_tuples


def test_map_questionnaire_case_task_models_maps_the_correct_list_of_models():
    # arrange
    todays_questionnaires_for_release = ["LMS2111Z", "LMS2112T"]

    # act
    result = map_questionnaire_case_task_models(todays_questionnaires_for_release)

    # assert
    assert result == [
        QuestionnaireCaseTaskModel(questionnaire="LMS2111Z"),
        QuestionnaireCaseTaskModel(questionnaire="LMS2112T"),
    ]


def test_create_questionnaire_case_task_name_returns_unique_name_each_time_when_passed_the_same_model():
    # arrange
    model = QuestionnaireCaseTaskModel("LMS2101A")

    # act
    result1 = create_questionnaire_case_task_name(model)
    result2 = create_questionnaire_case_task_name(model)

    # assert
    assert result1 != result2


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


@mock.patch("cloud_functions.create_totalmobile_jobs_trigger.run_async_tasks")
@mock.patch(
    "cloud_functions.create_totalmobile_jobs_trigger.get_cases_with_valid_world_ids"
)
def test_create_case_tasks_for_questionnaire(
    mock_get_cases_with_valid_world_ids,
    mock_run_async_tasks,
):
    # arrange
    config = config_helper.get_default_config()
    total_mobile_service_mock = create_autospec(TotalmobileService)
    questionnaire_service_mock = create_autospec(QuestionnaireService)
    total_mobile_service_mock.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6")]
    )

    questionnaire_name = "LMS2101_AA1"
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

    questionnaire_service_mock.get_eligible_cases.return_value = questionnaire_cases

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
    questionnaire_service_mock.get_wave_from_questionnaire_name.return_value = "1"
    questionnaire_service_mock.get_cases.return_value = []

    # act
    result = create_questionnaire_case_tasks(
        questionnaire_name,
        config,
        total_mobile_service_mock,
        questionnaire_service_mock,
    )

    # assert
    questionnaire_service_mock.get_eligible_cases.assert_called_with("LMS2101_AA1")

    mock_run_async_tasks.assert_called_once()
    kwargs = mock_run_async_tasks.call_args.kwargs
    assert kwargs["cloud_function"] == "bts-create-totalmobile-jobs-processor"
    assert kwargs["queue_id"] == config.create_totalmobile_jobs_task_queue_id
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


@mock.patch("cloud_functions.create_totalmobile_jobs_trigger.run_async_tasks")
def test_create_questionnaire_case_tasks_when_no_eligible_cases(mock_run_async_tasks):
    # arrange
    config = config_helper.get_default_config()
    questionnaire_name = "LMS2101_AA1"
    total_mobile_service_mock = create_autospec(TotalmobileService)
    questionnaire_service_mock = create_autospec(QuestionnaireService)

    questionnaire_service_mock.get_wave_from_questionnaire_name.return_value = "1"
    questionnaire_service_mock.get_cases.return_value = []

    # act
    result = create_questionnaire_case_tasks(
        questionnaire_name,
        config,
        total_mobile_service_mock,
        questionnaire_service_mock,
    )

    # assert
    mock_run_async_tasks.assert_not_called()
    assert (
        result == "Exiting as no eligible cases to send for questionnaire LMS2101_AA1"
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
