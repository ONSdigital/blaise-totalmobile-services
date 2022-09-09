from unittest.mock import call, create_autospec

from models.totalmobile.totalmobile_jobs_response_model import Job, TotalmobileJobsResponseModel
from services.blaise_service import BlaiseService
from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService
from services.totalmobile_service import TotalmobileService


def test_get_completed_blaise_cases_returns_an_expected_list_of_case_ids():
    # arrange
    questionnaire_name = "LMS1111_AA1"
    case_status_list = [
        {"primaryKey": "12345", "outcome": 110},
        {"primaryKey": "22222", "outcome": 310},
        {"primaryKey": "67890", "outcome": 110},
    ]

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    mock_blaise_service.get_case_status_information.return_value = case_status_list
    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(
        mock_totalmobile_service, mock_blaise_service
    )

    # act and assert
    assert delete_totalmobile_jobs_service.get_completed_blaise_cases(
        questionnaire_name
    ) == ["12345", "67890"]


def test_delete_totalmobile_jobs_completed_in_blaise_deletes_incomplete_jobs_only_for_completed_cases_in_blaise():
    # arrange
    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    mock_totalmobile_service.get_jobs_model.return_value = TotalmobileJobsResponseModel(
        [
            {"visitComplete": "True", "identity": {"reference": "LMS1111-AA1.12345"}},
            {"visitComplete": "True", "identity": {"reference": "LMS1111-AA1.22222"}},
            {"visitComplete": "False", "identity": {"reference": "LMS1111-AA1.67890"}},
        ]
    )

    mock_blaise_service.get_case_status_information.return_value = [
        {"primaryKey": "12345", "outcome": 310},
        {"primaryKey": "22222", "outcome": 110},
        {"primaryKey": "67890", "outcome": 110},
    ]

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(
        mock_totalmobile_service, mock_blaise_service
    )

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert mock_totalmobile_service.delete_job.call_count == 1
    mock_totalmobile_service.delete_job.assert_any_call(
        world_id, "LMS1111-AA1.67890", "110"
    )


def test_delete_totalmobile_jobs_completed_in_blaise_deletes_jobs_for_completed_cases_in_blaise_for_multiple_questionnaires():
    # arrange
    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    mock_totalmobile_service.get_jobs_model.return_value = TotalmobileJobsResponseModel(
        [
            {"visitComplete": "True", "identity": {"reference": "LMS1111-AA1.12345"}},
            {"visitComplete": "False", "identity": {"reference": "LMS2222-BB2.22222"}},
            {"visitComplete": "False", "identity": {"reference": "LMS1111-AA1.67890"}},
        ]
    )

    mock_blaise_service.get_case_status_information.side_effect = [
        [
            {"primaryKey": "12345", "outcome": 310},
            {"primaryKey": "67890", "outcome": 110},
        ],
        [
            {"primaryKey": "22222", "outcome": 110},
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
        world_id, "LMS1111-AA1.67890", "110"
    )
    mock_totalmobile_service.delete_job.assert_any_call(
        world_id, "LMS2222-BB2.22222", "110"
    )


def test_delete_totalmobile_jobs_completed_in_blaise_only_calls_case_status_information_once_per_questionnaire():
    # arrange
    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    mock_totalmobile_service.get_jobs_model.return_value = TotalmobileJobsResponseModel(
        [
            {"visitComplete": "True", "identity": {"reference": "LMS1111-AA1.12345"}},
            {"visitComplete": "False", "identity": {"reference": "LMS2222-BB2.22222"}},
            {"visitComplete": "False", "identity": {"reference": "LMS1111-AA1.67890"}},
            {"visitComplete": "False", "identity": {"reference": "LMS2222-BB2.44444"}},
        ]
    )

    mock_blaise_service.get_case_status_information.side_effect = [
        [
            {"primaryKey": "12345", "outcome": 310},
            {"primaryKey": "67890", "outcome": 110},
        ],
        [
            {"primaryKey": "22222", "outcome": 110},
            {"primaryKey": "44444", "outcome": 110},
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
        world_id, "LMS1111-AA1.67890", "110"
    )
    mock_totalmobile_service.delete_job.assert_any_call(
        world_id, "LMS2222-BB2.22222", "110"
    )
    mock_totalmobile_service.delete_job.assert_any_call(
        world_id, "LMS2222-BB2.44444", "110"
    )

    assert mock_blaise_service.get_case_status_information.call_count == 2
    mock_blaise_service.get_case_status_information.assert_any_call("LMS2222_BB2")
    mock_blaise_service.get_case_status_information.assert_any_call("LMS1111_AA1")
