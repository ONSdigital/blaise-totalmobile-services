from unittest.mock import call, create_autospec

import pytest

from models.totalmobile.totalmobile_get_jobs_response_model import (
    Job,
    TotalmobileGetJobsResponseModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.blaise_service import BlaiseService
from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService
from services.totalmobile_service import TotalmobileService
from tests.helpers import get_blaise_case_model_helper


@pytest.mark.parametrize(
    "outcome_code",
    [
        (110),
        (210),
        (300),
        (360),
        (370),
        (371),
        (372),
        (380),
        (390),
        (411),
        (412),
        (413),
        (430),
        (440),
        (460),
        (461),
        (510),
        (540),
        (541),
        (542),
        (551),
        (560),
        (561),
        (562),
        (580),
        (631),
        (640),
        (791),
        (792),
        (793),
        (794),
        (795),
    ],
)
def test_delete_totalmobile_jobs_completed_in_blaise_deletes_incomplete_jobs_only_for_completed_cases_in_blaise(
    outcome_code,
):
    # arrange
    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    mock_totalmobile_service.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id=world_id)]
    )

    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
            [
                {"visitComplete": True, "identity": {"reference": "LMS1111-AA1.12345"}},
                {"visitComplete": True, "identity": {"reference": "LMS1111-AA1.22222"}},
                {
                    "visitComplete": False,
                    "identity": {"reference": "LMS1111-AA1.67890"},
                },
            ]
        )
    )

    mock_blaise_service.get_cases.return_value = [
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="12345", outcome_code=outcome_code
        ),
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="22222", outcome_code=310
        ),
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="67890", outcome_code=outcome_code
        ),
    ]

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(
        mock_totalmobile_service, mock_blaise_service
    )

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert mock_totalmobile_service.delete_job.call_count == 1
    mock_totalmobile_service.delete_job.assert_any_call(
        world_id, "LMS1111-AA1.67890", "completed in blaise"
    )


def test_delete_totalmobile_jobs_completed_in_blaise_deletes_jobs_for_completed_cases_in_blaise_for_multiple_questionnaires():
    # arrange
    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    mock_totalmobile_service.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id=world_id)]
    )

    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
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

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(
        mock_totalmobile_service, mock_blaise_service
    )

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


def test_delete_totalmobile_jobs_completed_in_blaise_only_calls_case_status_information_once_per_questionnaire():
    # arrange
    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    mock_totalmobile_service.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id=world_id)]
    )

    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
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

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(
        mock_totalmobile_service, mock_blaise_service
    )

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


def test_delete_totalmobile_jobs_completed_in_blaise_does_not_get_caseids_for_questionnaires_that_have_no_incomplete_jobs():
    # arrange
    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)
    mock_totalmobile_service.get_world_model.return_value = TotalmobileWorldModel(
        worlds=[World(region="Region 1", id=world_id)]
    )

    mock_totalmobile_service.get_jobs_model.return_value = (
        TotalmobileGetJobsResponseModel(
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

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(
        mock_totalmobile_service, mock_blaise_service
    )

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert mock_blaise_service.get_cases.call_count == 0
    assert mock_totalmobile_service.delete_job.call_count == 0


def test_get_world_id_gets_the_expected_id_for_region_1():
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

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(
        mock_totalmobile_service, mock_blaise_service
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
        TotalmobileGetJobsResponseModel(
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
