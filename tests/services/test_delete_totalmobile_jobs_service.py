import pytest

from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService
from tests.fakes.fake_blaise_service import FakeBlaiseService
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService

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
def create_job_in_totalmobile(fake_totalmobile_service):
    def create(job_reference, region, visit_completed):
        fake_totalmobile_service.add_job(job_reference, region, visit_completed)

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
    delete_totalmobile_jobs_service,
    outcome_code,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.67890", "Region 1", visit_completed=False)
    create_case_in_blaise("LMS1111_AA1", "67890", outcome_code)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    # TODO: assert reason
    assert not fake_totalmobile_service.job_exists("LMS1111-AA1.67890")


@pytest.mark.parametrize("outcome_code", INCOMPLETE_JOB_OUTCOMES)
def test_delete_totalmobile_jobs_completed_in_blaise_does_not_delete_job_when_case_is_incomplete_and_totalmobile_job_is_incomplete(
    fake_totalmobile_service,
    create_job_in_totalmobile,
    create_case_in_blaise,
    delete_totalmobile_jobs_service,
    outcome_code,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.67890", "Region 1", visit_completed=False)
    create_case_in_blaise("LMS1111_AA1", "67890", outcome_code)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert fake_totalmobile_service.job_exists("LMS1111-AA1.67890")


@pytest.mark.parametrize("outcome_code", COMPLETE_JOB_OUTCOMES)
def test_delete_totalmobile_jobs_completed_in_blaise_does_not_delete_job_when_case_is_complete_and_totalmobile_job_is_complete(
    fake_totalmobile_service,
    create_job_in_totalmobile,
    create_case_in_blaise,
    delete_totalmobile_jobs_service,
    outcome_code,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.67890", "Region 1", visit_completed=True)
    create_case_in_blaise("LMS1111_AA1", "67890", outcome_code)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert fake_totalmobile_service.job_exists("LMS1111-AA1.67890")


@pytest.mark.parametrize(
    "region",
    [
        ("Region 1"),
        ("Region 2"),
        ("Region 3"),
        ("Region 4"),
        ("Region 5"),
        ("Region 6"),
        ("Region 7"),
        ("Region 8"),
    ],
)
def test_delete_totalmobile_jobs_completed_in_blaise_does_delete_job_for_all_regions_when_case_is_complete_and_totalmobile_job_is_complete(
    fake_totalmobile_service,
    create_job_in_totalmobile,
    create_case_in_blaise,
    delete_totalmobile_jobs_service,
    region,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.67890", region, visit_completed=False)
    create_case_in_blaise("LMS1111_AA1", "67890", 110)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert not fake_totalmobile_service.job_exists("LMS1111-AA1.67890")


@pytest.mark.parametrize(
    "region",
    [
        ("Region 0"),
        ("Region 9"),
    ],
)
def test_delete_totalmobile_jobs_completed_in_blaise_does_not_delete_job_in_unknown_regions(
    fake_totalmobile_service,
    create_job_in_totalmobile,
    create_case_in_blaise,
    delete_totalmobile_jobs_service,
    region,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.67890", region, visit_completed=False)
    create_case_in_blaise("LMS1111_AA1", "67890", 110)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert fake_totalmobile_service.job_exists("LMS1111-AA1.67890")


def test_delete_totalmobile_jobs_completed_in_blaise_deletes_jobs_for_completed_cases_in_blaise_for_multiple_questionnaires(
    fake_totalmobile_service,
    create_job_in_totalmobile,
    create_case_in_blaise,
    delete_totalmobile_jobs_service,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.67890", "Region 1", visit_completed=False)
    create_case_in_blaise("LMS1111_AA1", "67890", 123)
    create_job_in_totalmobile("LMS1111-BB2.12345", "Region 1", visit_completed=False)
    create_case_in_blaise("LMS1111_BB2", "12345", 456)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    # TODO: assert reason and world id
    assert not fake_totalmobile_service.job_exists("LMS1111-AA1.67890")
    assert not fake_totalmobile_service.job_exists("LMS1111-BB2.12345")


def test_delete_totalmobile_jobs_completed_in_blaise_only_calls_case_status_information_once_per_questionnaire(
    fake_blaise_service,
    delete_totalmobile_jobs_service,
    create_case_in_blaise,
    create_job_in_totalmobile,
):
    # arrange
    create_job_in_totalmobile("LMS1111-AA1.12345", "Region 1", visit_completed=True)
    create_job_in_totalmobile("LMS1111-AA1.67890", "Region 1", visit_completed=False)

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
    create_job_in_totalmobile("LMS1111-AA1.12345", "Region 1", visit_completed=True)
    create_job_in_totalmobile("LMS1111-AA1.22222", "Region 1", visit_completed=True)
    create_job_in_totalmobile("LMS1111-AA1.67890", "Region 1", visit_completed=True)

    # act
    delete_totalmobile_jobs_service.delete_totalmobile_jobs_completed_in_blaise()

    # assert
    assert fake_blaise_service.get_cases_call_count("LMS1111_AA1") == 0
