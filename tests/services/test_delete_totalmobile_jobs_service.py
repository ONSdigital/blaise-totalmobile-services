import logging
from unittest.mock import Mock, call, create_autospec

import pytest

from models.totalmobile.totalmobile_get_jobs_response_model import (
    Job,
    TotalmobileGetJobsResponseModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService
from services.totalmobile_service import RecallJobError, TotalmobileService
from tests.helpers.get_blaise_case_model_helper import get_populated_case_model

CASE_OUTCOMES_WHOSE_JOBS_SHOULD_BE_DELETED = [123, 110, 543]


@pytest.fixture()
def delete_totalmobile_jobs_service(mock_totalmobile_service, mock_blaise_service):
    return DeleteTotalmobileJobsService(
        totalmobile_service=mock_totalmobile_service, blaise_service=mock_blaise_service
    )


@pytest.fixture()
def mock_totalmobile_service(world_id):
    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_totalmobile_service.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id=world_id)]
    )
    return mock_totalmobile_service


@pytest.fixture()
def mock_blaise_service():
    return Mock()


@pytest.fixture()
def world_id():
    return "13013122-d69f-4d6b-gu1d-721f190c4479"


@pytest.mark.parametrize("outcome_code", CASE_OUTCOMES_WHOSE_JOBS_SHOULD_BE_DELETED)
def test_delete_jobs_for_completed_cases_deletes_job_when_case_is_completed_and_totalmobile_job_is_incomplete(
    mock_totalmobile_service,
    mock_blaise_service,
    delete_totalmobile_jobs_service,
    world_id,
    outcome_code,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
            questionnaire_jobs={
                "LMS1111_AA1": [
                    Job(
                        reference="LMS1111-AA1.67890",
                        case_id="67890",
                        visit_complete=False,
                        past_field_period=False,
                        allocated_resource_reference="stuart.minion",
                        work_type="LMS",
                    )
                ]
            }
        )
    )

    mock_blaise_service.get_cases.return_value = [
        get_populated_case_model(case_id="67890", outcome_code=outcome_code)
    ]

    # act
    delete_totalmobile_jobs_service.delete_jobs_for_completed_cases()

    # assert
    mock_totalmobile_service.recall_job.assert_called_with(
        "stuart.minion", "LMS", "LMS1111-AA1.67890"
    )
    mock_totalmobile_service.delete_job.assert_called_with(
        world_id, "LMS1111-AA1.67890", "completed in blaise"
    )


@pytest.mark.parametrize(
    "outcome_code",
    DeleteTotalmobileJobsService.CASE_OUTCOMES_WHOSE_JOBS_SHOULD_NOT_BE_DELETED,
)
def test_delete_jobs_for_completed_cases_does_not_delete_job_when_case_is_incomplete_and_totalmobile_job_is_incomplete(
    mock_totalmobile_service,
    mock_blaise_service,
    delete_totalmobile_jobs_service,
    outcome_code,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
            questionnaire_jobs={
                "LMS1111_AA1": [
                    Job(
                        reference="LMS1111-AA1.67890",
                        case_id="67890",
                        visit_complete=False,
                        past_field_period=False,
                        allocated_resource_reference=None,
                        work_type="LMS",
                    )
                ]
            }
        )
    )

    mock_blaise_service.get_cases.return_value = [
        get_populated_case_model(case_id="67890", outcome_code=outcome_code)
    ]

    # act
    delete_totalmobile_jobs_service.delete_jobs_for_completed_cases()

    # assert
    mock_totalmobile_service.recall_job.assert_not_called()
    mock_totalmobile_service.delete_job.assert_not_called()


@pytest.mark.parametrize("outcome_code", CASE_OUTCOMES_WHOSE_JOBS_SHOULD_BE_DELETED)
def test_delete_jobs_for_completed_cases_does_not_delete_job_when_case_is_complete_and_totalmobile_job_is_complete(
    mock_totalmobile_service,
    mock_blaise_service,
    delete_totalmobile_jobs_service,
    outcome_code,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
            questionnaire_jobs={
                "LMS1111_AA1": [
                    Job(
                        reference="LMS1111-AA1.67890",
                        case_id="67890",
                        visit_complete=True,
                        past_field_period=False,
                        allocated_resource_reference=None,
                        work_type="LMS",
                    )
                ]
            }
        )
    )

    mock_blaise_service.get_cases.return_value = [
        get_populated_case_model(case_id="67890", outcome_code=outcome_code)
    ]

    # act
    delete_totalmobile_jobs_service.delete_jobs_for_completed_cases()

    # assert
    mock_totalmobile_service.recall_job.assert_not_called()
    mock_totalmobile_service.delete_job.assert_not_called()


def test_delete_jobs_for_completed_cases_deletes_jobs_for_completed_cases_in_blaise_for_multiple_questionnaires(
    mock_totalmobile_service,
    mock_blaise_service,
    delete_totalmobile_jobs_service,
    world_id,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
            questionnaire_jobs={
                "LMS1111_AA1": [
                    Job(
                        reference="LMS1111-AA1.67890",
                        case_id="67890",
                        visit_complete=False,
                        past_field_period=False,
                        allocated_resource_reference="kevin.minion",
                        work_type="LMS",
                    )
                ],
                "LMS1111_BB2": [
                    Job(
                        reference="LMS1111-BB2.12345",
                        case_id="12345",
                        visit_complete=False,
                        past_field_period=False,
                        allocated_resource_reference=None,
                        work_type="LMS",
                    )
                ],
            }
        )
    )

    mock_blaise_service.get_cases.side_effect = [
        [get_populated_case_model(case_id="67890", outcome_code=123)],
        [get_populated_case_model(case_id="12345", outcome_code=456)],
    ]

    # act
    delete_totalmobile_jobs_service.delete_jobs_for_completed_cases()

    # assert
    mock_totalmobile_service.recall_job.assert_called_once_with(
        "kevin.minion", "LMS", "LMS1111-AA1.67890"
    )
    mock_totalmobile_service.delete_job.assert_has_calls(
        [
            call(world_id, "LMS1111-AA1.67890", "completed in blaise"),
            call(world_id, "LMS1111-BB2.12345", "completed in blaise"),
        ]
    )


def test_delete_jobs_for_completed_cases_only_calls_get_cases_once_per_questionnaire(
    mock_totalmobile_service,
    mock_blaise_service,
    delete_totalmobile_jobs_service,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
            questionnaire_jobs={
                "LMS1111_AA1": [
                    Job(
                        reference="LMS1111-AA1.67890",
                        case_id="67890",
                        visit_complete=False,
                        past_field_period=False,
                        allocated_resource_reference=None,
                        work_type="LMS",
                    ),
                    Job(
                        reference="LMS1111-AA1.23423",
                        case_id="23423",
                        visit_complete=False,
                        past_field_period=False,
                        allocated_resource_reference=None,
                        work_type="LMS",
                    ),
                ],
                "LMS1111_BB2": [
                    Job(
                        reference="LMS1111-BB2.12345",
                        case_id="12345",
                        visit_complete=False,
                        past_field_period=False,
                        allocated_resource_reference=None,
                        work_type="LMS",
                    )
                ],
            }
        )
    )

    mock_blaise_service.get_cases.side_effect = [
        [
            get_populated_case_model(case_id="67890", outcome_code=123),
            get_populated_case_model(case_id="23423", outcome_code=110),
        ],
        [get_populated_case_model(case_id="12345", outcome_code=456)],
    ]

    # act
    delete_totalmobile_jobs_service.delete_jobs_for_completed_cases()

    # assert
    mock_blaise_service.get_cases.assert_has_calls(
        [call("LMS1111_AA1"), call("LMS1111_BB2")]
    )


def test_delete_jobs_for_completed_cases_does_not_get_caseids_for_questionnaires_that_have_no_incomplete_jobs(
    mock_totalmobile_service,
    mock_blaise_service,
    delete_totalmobile_jobs_service,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
            questionnaire_jobs={
                "LMS1111_AA1": [
                    Job(
                        reference="LMS1111-AA1.67890",
                        case_id="67890",
                        visit_complete=True,
                        past_field_period=False,
                        allocated_resource_reference=None,
                        work_type="LMS",
                    ),
                    Job(
                        reference="LMS1111-AA1.23423",
                        case_id="23423",
                        visit_complete=True,
                        past_field_period=False,
                        allocated_resource_reference=None,
                        work_type="LMS",
                    ),
                ],
                "LMS1111_BB2": [
                    Job(
                        reference="LMS1111-BB2.12345",
                        case_id="12345",
                        visit_complete=True,
                        past_field_period=False,
                        allocated_resource_reference=None,
                        work_type="LMS",
                    )
                ],
            }
        )
    )

    # act
    delete_totalmobile_jobs_service.delete_jobs_for_completed_cases()

    # assert
    mock_blaise_service.get_cases.assert_not_called()


def test_delete_jobs_past_field_period_deletes_job_when_field_period_has_expired(
    mock_totalmobile_service,
    delete_totalmobile_jobs_service,
    world_id,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
            questionnaire_jobs={
                "LMS1111_AA1": [
                    Job(
                        reference="LMS1111-AA1.67890",
                        case_id="67890",
                        visit_complete=False,
                        past_field_period=True,
                        allocated_resource_reference=None,
                        work_type="LMS",
                    )
                ],
                "LMS1111_BB2": [
                    Job(
                        reference="LMS1111-BB2.12345",
                        case_id="12345",
                        visit_complete=False,
                        past_field_period=True,
                        allocated_resource_reference="bob.minion",
                        work_type="LMS",
                    )
                ],
            }
        )
    )

    # act
    delete_totalmobile_jobs_service.delete_jobs_past_field_period()

    # assert
    mock_totalmobile_service.recall_job.assert_called_once_with(
        "bob.minion", "LMS", "LMS1111-BB2.12345"
    )
    mock_totalmobile_service.delete_job.assert_has_calls(
        [
            call(world_id, "LMS1111-AA1.67890", "past field period"),
            call(world_id, "LMS1111-BB2.12345", "past field period"),
        ]
    )


def test_delete_jobs_past_field_period_does_not_delete_job_when_field_period_has_not_expired(
    mock_totalmobile_service,
    delete_totalmobile_jobs_service,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
            questionnaire_jobs={
                "LMS1111_AA1": [
                    Job(
                        reference="LMS1111-AA1.67890",
                        case_id="67890",
                        visit_complete=False,
                        past_field_period=False,
                        allocated_resource_reference=None,
                        work_type="LMS",
                    )
                ]
            }
        )
    )

    # act
    delete_totalmobile_jobs_service.delete_jobs_past_field_period()

    # assert
    mock_totalmobile_service.recall_job.assert_not_called()
    mock_totalmobile_service.delete_job.assert_not_called()


def test_delete_jobs_for_completed_cases_logs_when_a_log_is_recalled(
    mock_totalmobile_service,
    mock_blaise_service,
    delete_totalmobile_jobs_service,
    world_id,
    caplog,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
            questionnaire_jobs={
                "LMS1111_AA1": [
                    Job(
                        reference="LMS1111-AA1.67890",
                        case_id="67890",
                        visit_complete=False,
                        past_field_period=False,
                        allocated_resource_reference="stuart.minion",
                        work_type="LMS",
                    )
                ]
            }
        )
    )

    mock_blaise_service.get_cases.return_value = [
        get_populated_case_model(case_id="67890", outcome_code=110)
    ]

    # act
    with caplog.at_level(level=logging.INFO):
        delete_totalmobile_jobs_service.delete_jobs_for_completed_cases()

    # assert
    assert (
        "root",
        logging.INFO,
        "Successfully recalled job LMS1111-AA1.67890 from stuart.minion on Totalmobile",
    ) in caplog.record_tuples


def test_delete_jobs_for_completed_cases_continues_to_delete_when_a_recall_fails(
    mock_totalmobile_service,
    mock_blaise_service,
    delete_totalmobile_jobs_service,
    world_id,
    caplog,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
            questionnaire_jobs={
                "LMS1111_AA1": [
                    Job(
                        reference="LMS1111-AA1.67890",
                        case_id="67890",
                        visit_complete=False,
                        past_field_period=False,
                        allocated_resource_reference="stuart.minion",
                        work_type="LMS",
                    )
                ]
            }
        )
    )

    mock_blaise_service.get_cases.return_value = [
        get_populated_case_model(case_id="67890", outcome_code=110)
    ]

    mock_totalmobile_service.recall_job.side_effect = RecallJobError("Error occurred")

    # act
    with caplog.at_level(level=logging.ERROR):
        delete_totalmobile_jobs_service.delete_jobs_for_completed_cases()

    # assert
    assert (
        "root",
        logging.ERROR,
        "Failed to recall job LMS1111-AA1.67890 from stuart.minion on Totalmobile",
    ) in caplog.record_tuples
    mock_totalmobile_service.delete_job.assert_called_with(
        world_id, "LMS1111-AA1.67890", "completed in blaise"
    )
