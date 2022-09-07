import pytest

from tests.fakes.fake_totalmobile_service import FakeTotalmobileService, _JobDoesNotExistError


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
    service.remove_job(reference)

    # assert
    assert not service.job_exists(reference)


def test_remove_job_when_job_does_not_exist(service: FakeTotalmobileService):
    # arrange, act and assert
    with pytest.raises(_JobDoesNotExistError, match=f"Job 'unknown' does not exist"):
        service.remove_job("unknown")
