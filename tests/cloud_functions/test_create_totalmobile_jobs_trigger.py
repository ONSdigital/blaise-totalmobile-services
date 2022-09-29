import json
import logging
from unittest import mock
from unittest.mock import create_autospec

from cloud_functions.create_totalmobile_jobs_trigger import (
    create_cloud_tasks,
    create_totalmobile_jobs_trigger,
    map_totalmobile_job_models,
)
from models.blaise.blaise_case_information_model import UacChunks
from models.totalmobile.totalmobile_outgoing_create_job_payload_model import (
    TotalMobileOutgoingCreateJobPayloadModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.questionnaire_service import QuestionnaireService
from services.totalmobile_service import TotalmobileService
from tests.helpers import config_helper
from tests.helpers.get_blaise_case_model_helper import get_populated_case_model


def test_check_questionnaire_release_date_logs_when_there_are_no_questionnaires_for_release(
        caplog
):
    # arrange
    config = config_helper.get_default_config()
    total_mobile_service_mock = create_autospec(TotalmobileService)
    questionnaire_service_mock = create_autospec(QuestionnaireService)

    questionnaire_service_mock.get_questionnaires_with_totalmobile_release_date_of_today.return_value = []
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
        == TotalMobileOutgoingCreateJobPayloadModel.import_case(
            questionnaire_name, case_data[0]
        ).to_payload()
    )

    assert result[1].questionnaire == "LMS2101_AA1"
    assert result[1].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa7"
    assert result[1].case_id == "10020"
    assert (
        result[1].payload
        == TotalMobileOutgoingCreateJobPayloadModel.import_case(
            questionnaire_name, case_data[1]
        ).to_payload()
    )

    assert result[2].questionnaire == "LMS2101_AA1"
    assert result[2].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa9"
    assert result[2].case_id == "10030"
    assert (
        result[2].payload
        == TotalMobileOutgoingCreateJobPayloadModel.import_case(
            questionnaire_name, case_data[2]
        ).to_payload()
    )


@mock.patch("cloud_functions.create_totalmobile_jobs_trigger.run_async_tasks")
def test_create_case_tasks_for_questionnaire(
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

    questionnaire_service_mock.get_wave_from_questionnaire_name.return_value = "1"
    questionnaire_service_mock.get_cases.return_value = []

    # act
    result = create_cloud_tasks(
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
        "payload": TotalMobileOutgoingCreateJobPayloadModel.import_case(
            "LMS2101_AA1", questionnaire_cases[0]
        ).to_payload(),
    }
    assert result == "Done"


@mock.patch("cloud_functions.create_totalmobile_jobs_trigger.run_async_tasks")
def test_create_cloud_tasks_when_no_eligible_cases(mock_run_async_tasks):
    # arrange
    config = config_helper.get_default_config()
    questionnaire_name = "LMS2101_AA1"
    total_mobile_service_mock = create_autospec(TotalmobileService)
    questionnaire_service_mock = create_autospec(QuestionnaireService)

    questionnaire_service_mock.get_wave_from_questionnaire_name.return_value = "1"
    questionnaire_service_mock.get_cases.return_value = []

    # act
    result = create_cloud_tasks(
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
