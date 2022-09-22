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
from tests.helpers import get_blaise_case_model_helper

INCOMPLETE_JOB_OUTCOMES = [0, 120, 310, 320]
COMPLETE_JOB_OUTCOMES = [123, 110, 543]


@pytest.fixture()
def delete_totalmobile_jobs_service(mock_totalmobile_service, mock_blaise_service):
    return DeleteTotalmobileJobsService(
        mock_totalmobile_service, mock_blaise_service, INCOMPLETE_JOB_OUTCOMES
    )


@pytest.fixture()
def mock_totalmobile_service(world_id):
    mock = create_autospec(TotalmobileService)
    mock.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id=world_id)]
    )
    return mock


@pytest.fixture()
def mock_blaise_service():
    return create_autospec(BlaiseService)


@pytest.fixture()
def world_id():
    return "13013122-d69f-4d6b-gu1d-721f190c4479"


@pytest.fixture()
def create_job_in_totalmobile(mock_totalmobile_service, world_id):
    def create(job_reference, visit_completed):
        reference_model = TotalmobileReferenceModel.from_reference(job_reference)
        results = {
            world_id: (
                TotalmobileGetJobsResponseModel(
                    {
                        reference_model.questionnaire_name: [
                            Job(
                                job_reference,
                                reference_model.case_id,
                                visit_completed,
                            )
                        ]
                    }
                )
            )
        }
        mock_totalmobile_service.get_jobs_model.side_effect = results.get

    return create


@pytest.fixture()
def create_case_in_blaise(mock_blaise_service):
    def create(questionnaire_name, case_id, outcome_code):
        results = {
            questionnaire_name: [
                get_blaise_case_model_helper.get_populated_case_model(
                    case_id=case_id, outcome_code=outcome_code
                )
            ]
        }
        mock_blaise_service.get_cases.side_effect = results.get

    return create


@pytest.mark.parametrize("outcome_code", COMPLETE_JOB_OUTCOMES)
def test_delete_totalmobile_jobs_completed_in_blaise_deletes_job_when_case_is_completed_and_totalmobile_job_is_incomplete(
    mock_totalmobile_service,
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
    mock_totalmobile_service.delete_job.assert_called_with(
        world_id, "LMS1111-AA1.67890", "completed in blaise"
    )


@pytest.mark.parametrize("outcome_code", INCOMPLETE_JOB_OUTCOMES)
def test_delete_totalmobile_jobs_completed_in_blaise_does_not_delete_job_when_case_is_incomplete_and_totalmobile_job_is_incomplete(
    mock_totalmobile_service,
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
    mock_totalmobile_service.delete_job.assert_not_called()


@pytest.mark.parametrize("outcome_code", COMPLETE_JOB_OUTCOMES)
def test_delete_totalmobile_jobs_completed_in_blaise_does_not_delete_job_when_case_is_complete_and_totalmobile_job_is_complete(
    mock_totalmobile_service,
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
    mock_totalmobile_service.delete_job.assert_not_called()


def test_delete_totalmobile_jobs_completed_in_blaise_deletes_jobs_for_completed_cases_in_blaise_for_multiple_questionnaires(
    mock_totalmobile_service,
    mock_blaise_service,
    world_id,
    delete_totalmobile_jobs_service,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel.from_get_jobs_response(
            [
                {"visitComplete": True, "identity": {"reference": "LMS1111-AA1.12345"}},
                {
                    "visitComplete": False,
                    "identity": {"reference": "LMS2222-BB2.22222"},
                },
                {
                    "visitComplete": False,
                    "identity": {"reference": "LMS1111-AA1.67890"},
                },
            ]
        )
    )

    mock_blaise_service.get_cases.side_effect = [
        [
            get_blaise_case_model_helper.get_populated_case_model(
                case_id="12345", outcome_code=310
            ),
            get_blaise_case_model_helper.get_populated_case_model(
                case_id="67890", outcome_code=110
            ),
        ],
        [
            get_blaise_case_model_helper.get_populated_case_model(
                case_id="22222", outcome_code=110
            )
        ],
    ]

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert mock_totalmobile_service.delete_job.call_count == 2
    mock_totalmobile_service.delete_job.assert_any_call(
        world_id, "LMS1111-AA1.67890", "completed in blaise"
    )
    mock_totalmobile_service.delete_job.assert_any_call(
        world_id, "LMS2222-BB2.22222", "completed in blaise"
    )


def test_delete_totalmobile_jobs_completed_in_blaise_only_calls_case_status_information_once_per_questionnaire(
    mock_totalmobile_service,
    mock_blaise_service,
    world_id,
    delete_totalmobile_jobs_service,
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel.from_get_jobs_response(
            [
                {"visitComplete": True, "identity": {"reference": "LMS1111-AA1.12345"}},
                {
                    "visitComplete": False,
                    "identity": {"reference": "LMS2222-BB2.22222"},
                },
                {
                    "visitComplete": False,
                    "identity": {"reference": "LMS1111-AA1.67890"},
                },
                {
                    "visitComplete": False,
                    "identity": {"reference": "LMS2222-BB2.44444"},
                },
            ]
        )
    )

    mock_blaise_service.get_cases.side_effect = [
        [
            get_blaise_case_model_helper.get_populated_case_model(
                case_id="12345", outcome_code=310
            ),
            get_blaise_case_model_helper.get_populated_case_model(
                case_id="67890", outcome_code=110
            ),
        ],
        [
            get_blaise_case_model_helper.get_populated_case_model(
                case_id="22222", outcome_code=110
            ),
            get_blaise_case_model_helper.get_populated_case_model(
                case_id="44444", outcome_code=110
            ),
        ],
    ]

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert mock_totalmobile_service.delete_job.call_count == 3
    mock_totalmobile_service.delete_job.assert_any_call(
        world_id, "LMS1111-AA1.67890", "completed in blaise"
    )
    mock_totalmobile_service.delete_job.assert_any_call(
        world_id, "LMS2222-BB2.22222", "completed in blaise"
    )
    mock_totalmobile_service.delete_job.assert_any_call(
        world_id, "LMS2222-BB2.44444", "completed in blaise"
    )

    assert mock_blaise_service.get_cases.call_count == 2
    mock_blaise_service.get_cases.assert_any_call("LMS2222_BB2")
    mock_blaise_service.get_cases.assert_any_call("LMS1111_AA1")


def test_delete_totalmobile_jobs_completed_in_blaise_does_not_get_caseids_for_questionnaires_that_have_no_incomplete_jobs(
    mock_totalmobile_service, mock_blaise_service, delete_totalmobile_jobs_service
):
    # arrange
    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel.from_get_jobs_response(
            [
                {"visitComplete": True, "identity": {"reference": "LMS1111-AA1.12345"}},
                {"visitComplete": True, "identity": {"reference": "LMS1111-AA1.22222"}},
                {"visitComplete": True, "identity": {"reference": "LMS1111-AA1.67890"}},
            ]
        )
    )

    mock_blaise_service.get_cases.return_value = [
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="12345", outcome_code=110
        ),
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="22222", outcome_code=310
        ),
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="67890", outcome_code=110
        ),
    ]

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert mock_blaise_service.get_cases.call_count == 0
    assert mock_totalmobile_service.delete_job.call_count == 0


def test_get_world_id_gets_the_expected_id_for_region_1(
    mock_totalmobile_service, delete_totalmobile_jobs_service
):
    # arrange
    mock_totalmobile_service.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[
            World(region="Region 1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            World(region="Region 2", id="3fa85f64-5717-4562-b3fc-2c963f66afa7"),
            World(region="Region 3", id="3fa85f64-5717-4562-b3fc-2c963f66afa8"),
            World(region="Region 4", id="3fa85f64-5717-4562-b3fc-2c963f66afa9"),
            World(region="Region 5", id="3fa85f64-5717-4562-b3fc-2c963f66afa2"),
        ]
    )

    # act
    result = delete_totalmobile_jobs_service.get_world_id()

    # assert
    assert result == "3fa85f64-5717-4562-b3fc-2c963f66afa6"


def test_delete_totalmobile_jobs_completed_in_blaise_only_gets_jobs_in_region_1(
    mock_totalmobile_service, mock_blaise_service, delete_totalmobile_jobs_service
):
    # arrange
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

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert mock_totalmobile_service.get_jobs_model.call_count == 1
    mock_totalmobile_service.get_jobs_model.assert_any_call(
        "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    )
