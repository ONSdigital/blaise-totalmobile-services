from unittest.mock import call, create_autospec

import pytest

from models.totalmobile.totalmobile_get_jobs_response_model import (
    Job,
    TotalmobileGetJobsResponseModel,
)
from models.totalmobile.totalmobile_reference_model import TotalmobileReferenceModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.blaise_service import BlaiseService
from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService
from services.totalmobile_service import TotalmobileService
from tests.fakes.fake_blaise_service import FakeBlaiseService
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService
from tests.helpers import get_blaise_case_model_helper

INCOMPLETE_JOB_OUTCOMES = [0, 120, 310, 320]
COMPLETE_JOB_OUTCOMES = [123, 110, 543]


@pytest.fixture()
def delete_totalmobile_jobs_service(fake_totalmobile_service, fake_blaise_service):
    return DeleteTotalmobileJobsService(fake_totalmobile_service, fake_blaise_service)


@pytest.fixture()
def fake_totalmobile_service():
    return FakeTotalmobileService()


@pytest.fixture()
def fake_blaise_service():
    return FakeBlaiseService()


@pytest.fixture()
def world_id():
    return "13013122-d69f-4d6b-gu1d-721f190c4479"


@pytest.fixture()
def create_job_in_totalmobile(fake_totalmobile_service, world_id):
    def create(job_reference, visit_completed):
        fake_totalmobile_service.add_job(job_reference, visit_completed)

    return create


@pytest.fixture()
def create_case_in_blaise(fake_blaise_service):
    def create(questionnaire_name, case_id, outcome_code):
        fake_blaise_service.add_questionnaire(questionnaire_name)
        fake_blaise_service.add_case_to_questionnaire(questionnaire_name, case_id)
        fake_blaise_service.update_outcome_code_of_case_in_questionnaire(
            questionnaire_name, case_id, outcome_code
        )

    return create


@pytest.mark.parametrize("outcome_code", COMPLETE_JOB_OUTCOMES)
def test_delete_totalmobile_jobs_completed_in_blaise_deletes_job_when_case_is_completed_and_totalmobile_job_is_incomplete(
    fake_totalmobile_service,
    create_job_in_totalmobile,
    create_case_in_blaise,
    world_id,
    delete_totalmobile_jobs_service,
    outcome_code,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.67890", visit_completed=False)
    create_case_in_blaise("LMS1111_AA1", "67890", outcome_code)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    # TODO: assert reason and world id
    assert fake_totalmobile_service.delete_job_has_been_called("LMS1111-AA1.67890")


@pytest.mark.parametrize("outcome_code", INCOMPLETE_JOB_OUTCOMES)
def test_delete_totalmobile_jobs_completed_in_blaise_does_not_delete_job_when_case_is_incomplete_and_totalmobile_job_is_incomplete(
    fake_totalmobile_service,
    create_job_in_totalmobile,
    create_case_in_blaise,
    delete_totalmobile_jobs_service,
    outcome_code,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.67890", visit_completed=False)
    create_case_in_blaise("LMS1111_AA1", "67890", outcome_code)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert not fake_totalmobile_service.delete_job_has_been_called("LMS1111-AA1.67890")


@pytest.mark.parametrize("outcome_code", COMPLETE_JOB_OUTCOMES)
def test_delete_totalmobile_jobs_completed_in_blaise_does_not_delete_job_when_case_is_complete_and_totalmobile_job_is_complete(
    fake_totalmobile_service,
    create_job_in_totalmobile,
    create_case_in_blaise,
    delete_totalmobile_jobs_service,
    outcome_code,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.67890", visit_completed=True)
    create_case_in_blaise("LMS1111_AA1", "67890", outcome_code)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert not fake_totalmobile_service.delete_job_has_been_called("LMS1111-AA1.67890")


def test_delete_totalmobile_jobs_completed_in_blaise_deletes_jobs_for_completed_cases_in_blaise_for_multiple_questionnaires(
    fake_totalmobile_service,
    create_job_in_totalmobile,
    create_case_in_blaise,
    world_id,
    delete_totalmobile_jobs_service,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.67890", visit_completed=False)
    create_case_in_blaise("LMS1111_AA1", "67890", 123)
    create_job_in_totalmobile("LMS1111-BB2.12345", visit_completed=False)
    create_case_in_blaise("LMS1111_BB2", "12345", 456)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    # TODO: assert reason and world id
    assert fake_totalmobile_service.delete_job_has_been_called("LMS1111-AA1.67890")
    assert fake_totalmobile_service.delete_job_has_been_called("LMS1111-BB2.12345")


def test_delete_totalmobile_jobs_completed_in_blaise_only_calls_case_status_information_once_per_questionnaire(
    fake_blaise_service,
    delete_totalmobile_jobs_service,
    create_case_in_blaise,
    create_job_in_totalmobile,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.12345", visit_completed=True)
    create_job_in_totalmobile("LMS1111-AA1.67890", visit_completed=False)

    create_case_in_blaise("LMS1111_AA1", "12345", 310)
    create_case_in_blaise("LMS1111_AA1", "67890", 110)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert fake_blaise_service.get_cases_call_count("LMS1111_AA1") == 1


def test_delete_totalmobile_jobs_completed_in_blaise_does_not_get_caseids_for_questionnaires_that_have_no_incomplete_jobs(
    fake_blaise_service, delete_totalmobile_jobs_service, create_job_in_totalmobile
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.12345", visit_completed=True)
    create_job_in_totalmobile("LMS1111-AA1.22222", visit_completed=True)
    create_job_in_totalmobile("LMS1111-AA1.67890", visit_completed=True)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert fake_blaise_service.get_cases_call_count("LMS1111_AA1") == 0


def test_get_world_id_gets_the_expected_id_for_region_1(fake_blaise_service):
    # arrange
    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_totalmobile_service.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="3fa85f64-5717-4562-b3fc-2c963f66afa7"),
            World(region="Region 3", id="3fa85f64-5717-4562-b3fc-2c963f66afa8"),
            World(region="Region 4", id="3fa85f64-5717-4562-b3fc-2c963f66afa9"),
            World(region="Region 5", id="3fa85f64-5717-4562-b3fc-2c963f66afa2"),
        ]
    )

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(
        mock_totalmobile_service, fake_blaise_service
    )

    # act
    result = delete_totalmobile_jobs_service.get_world_id()

    # assert
    assert result == "3fa85f64-5717-4562-b3fc-2c963f66afa6"


def test_delete_totalmobile_jobs_completed_in_blaise_only_gets_jobs_in_region_1():
    # arrange
    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)
    mock_totalmobile_service.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="3fa85f64-5717-4562-b3fc-2c963f66afa7"),
            World(region="Region 3", id="3fa85f64-5717-4562-b3fc-2c963f66afa8"),
            World(region="Region 4", id="3fa85f64-5717-4562-b3fc-2c963f66afa9"),
            World(region="Region 5", id="3fa85f64-5717-4562-b3fc-2c963f66afa2"),
        ]
    )

    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel.from_get_jobs_response(
            [
                {"visitComplete": True, "identity": {"reference": "LMS1111-AA1.12345"}},
            ]
        )
    )

    mock_blaise_service.get_cases.side_effect = [
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="12345", outcome_code=310
        ),
    ]

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(
        mock_totalmobile_service, mock_blaise_service
    )

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert mock_totalmobile_service.get_jobs_model.call_count == 1
    mock_totalmobile_service.get_jobs_model.assert_any_call(
        "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
