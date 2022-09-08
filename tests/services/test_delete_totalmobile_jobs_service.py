from services.blaise_service import BlaiseService
from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService
from unittest.mock import create_autospec

from services.totalmobile_service import TotalmobileService


def test_delete_totalmobile_job_calls_correct_service():
    # arrange
    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(mock_totalmobile_service, mock_blaise_service)

    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"
    job_reference = "LMS1111-AA1.12345"
    reason = "110"

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_job(world_id, job_reference, reason)

    # assert
    mock_totalmobile_service.delete_job.assert_called_with(world_id, job_reference, reason)


def test_get_incomplete_totalmobile_job_references_returns_an_expected_list_of_job_references():
    # arrange
    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    mock_totalmobile_service.get_jobs.return_value = [
        {
            "visitComplete": True,
            "identity": {"reference": "LMS1111-AA1.12345"}
        },
        {
            "visitComplete": False,
            "identity": {"reference": "LMS1111-AA1.67890"}
        },
        {
            "visitComplete": False,
            "identity": {"reference": "LMS2222-BB2.12345"}
        },
    ]

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(mock_totalmobile_service, mock_blaise_service)

    # act
    result = delete_totalmobile_jobs_service.get_incomplete_totalmobile_job_references(world_id)

    # assert
    assert result == ["LMS1111-AA1.67890", "LMS2222-BB2.12345"]


def test_map_reference_models_from_list_of_job_references_returns_an_expected_list_of_reference_models():
    # arrange
    job_references = ["LMS1111-AA1.67890", "LMS2222-BB2.12345"]

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(mock_totalmobile_service, mock_blaise_service)

    # act
    result = delete_totalmobile_jobs_service.map_reference_models_from_list_of_job_references(job_references)

    # assert
    assert result[0].questionnaire_name == "LMS1111_AA1"
    assert result[0].case_id == "67890"

    assert result[1].questionnaire_name == "LMS2222_BB2"
    assert result[1].case_id == "12345"


def test_get_completed_blaise_cases_returns_an_expected_list_of_case_ids():
    # arrange
    questionnaire_name = "LMS1111_AA1"
    case_status_list = [
        {
            "primaryKey": "12345",
            "outcome": 110
        },
        {
            "primaryKey": "22222",
            "outcome": 310
        },
        {
            "primaryKey": "67890",
            "outcome": 110
        }
    ]

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    mock_blaise_service.get_case_status_information.return_value = case_status_list
    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(mock_totalmobile_service, mock_blaise_service)

    # act and assert
    assert delete_totalmobile_jobs_service.get_completed_blaise_cases(questionnaire_name) == ["12345", "67890"]


def test_delete_totalmobile_jobs_completed_in_blaise_deletes_jobs_for_completed_cases_in_blaise_for_one_questionnaire():
    # arrange
    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    mock_totalmobile_service.get_jobs.return_value = [
        {
            "visitComplete": True,
            "identity": {"reference": "LMS1111-AA1.12345"}
        },
        {
            "visitComplete": False,
            "identity": {"reference": "LMS1111-AA1.67890"}
        },
        {
            "visitComplete": False,
            "identity": {"reference": "LMS1111-AA1.22222"}
        },
    ]
    mock_blaise_service.get_case_status_information.return_value = [
        {
            "primaryKey": "12345",
            "outcome": 310
        },
        {
            "primaryKey": "22222",
            "outcome": 310
        },
        {
            "primaryKey": "67890",
            "outcome": 110
        }
    ]

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(mock_totalmobile_service, mock_blaise_service)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    mock_totalmobile_service.delete_job.assert_called_with(world_id, "LMS1111-AA1.67890", "110")


def test_delete_totalmobile_jobs_completed_in_blaise_deletes_jobs_for_completed_cases_in_blaise_for_multiple_questionnaires():
    # arrange
    world_id = "13013122-d69f-4d6b-gu1d-721f190c4479"

    mock_totalmobile_service = create_autospec(TotalmobileService)
    mock_blaise_service = create_autospec(BlaiseService)

    mock_totalmobile_service.get_jobs.return_value = [
        {
            "visitComplete": True,
            "identity": {"reference": "LMS1111-AA1.12345"}
        },
        {
            "visitComplete": False,
            "identity": {"reference": "LMS2222-BB2.22222"}
        },
        {
            "visitComplete": False,
            "identity": {"reference": "LMS1111-AA1.67890"}
        },
    ]
    # return this thing first ("LMS1111-AA1.67890")
    mock_blaise_service.get_case_status_information.return_value = [
        {
            "primaryKey": "12345",
            "outcome": 310
        },
        {
            "primaryKey": "22222",
            "outcome": 310
        },
        {
            "primaryKey": "67890",
            "outcome": 110
        }
    ]

    # return this thing second ("LMS2222-BB2.22222")
    mock_blaise_service.get_case_status_information.return_value = [
        {
            "primaryKey": "12345",
            "outcome": 310
        },
        {
            "primaryKey": "22222",
            "outcome": 110
        },
        {
            "primaryKey": "67890",
            "outcome": 310
        }
    ]

    delete_totalmobile_jobs_service = DeleteTotalmobileJobsService(mock_totalmobile_service, mock_blaise_service)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    mock_totalmobile_service.delete_job.assert_called_with(world_id, "LMS1111-AA1.67890", "110")
    mock_totalmobile_service.delete_job.assert_called_with(world_id, "LMS2222-BB2.22222", "110")
