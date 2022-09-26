import pytest

from models.totalmobile.totalmobile_get_jobs_response_model import Job
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService


@pytest.fixture()
def service() -> FakeTotalmobileService:
    return FakeTotalmobileService()


def test_job_exists(service: FakeTotalmobileService):
    # arrange & act
    service.add_job("LMS11111-AA1.12345")
    service.add_job("LMS22222-BB2.67890")

    # assert
    assert service.job_exists("LMS11111-AA1.12345")
    assert service.job_exists("LMS22222-BB2.67890")
    assert not service.job_exists("LMS88888-CC3.88888")
    assert not service.job_exists("LMS99999-DD4.99999")


def test_remove_job(service: FakeTotalmobileService):
    # arrange
    reference = "LMS11111-AA1.12345"

    # act
    service.add_job(reference)
    service.delete_job("foo", reference)

    # assert
    assert service.delete_job_has_been_called(reference)


def test_get_jobs_model(service: FakeTotalmobileService):
    # arrange
    service.add_job("LMS11111-AA1.12345")
    service.add_job("LMS11111-AA1.56789", True)

    # act
    jobs_model = service.get_jobs_model("123")

    # assert
    assert jobs_model.questionnaire_jobs == {
        "LMS11111_AA1": [
            Job("LMS11111-AA1.12345", "12345", False),
            Job("LMS11111-AA1.56789", "56789", True),
        ]
    }
