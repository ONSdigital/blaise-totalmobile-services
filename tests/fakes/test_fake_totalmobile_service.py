import pytest

from models.totalmobile.totalmobile_get_jobs_response_model import Job
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService


@pytest.fixture()
def service() -> FakeTotalmobileService:
    return FakeTotalmobileService()


def test_remove_job(service: FakeTotalmobileService):
    # arrange
    service.add_job("LMS11111-AA1.12345", "Region 1")
    service.add_job("LMS11111-AA1.34680", "Region 1")

    # act
    service.delete_job("world-id-1", "LMS11111-AA1.12345")

    # assert
    assert not service.job_exists("LMS11111-AA1.12345")
    assert service.job_exists("LMS11111-AA1.34680")


def test_job_exists(service: FakeTotalmobileService):
    # arrange
    service.add_job("LMS11111-AA1.12345", "Region 1")
    service.add_job("LMS11111-AA1.34680", "Region 2")

    # assert
    assert service.job_exists("LMS11111-AA1.12345")
    assert service.job_exists("LMS11111-AA1.34680")
    assert not service.job_exists("LMS11111-AA1.23456")


def test_job_raises_exception_when_adding_job_with_same_reference_twice(
    service: FakeTotalmobileService,
):
    # arrange
    service.add_job("LMS11111-AA1.12345", "Region 1")

    # assert
    with pytest.raises(
        Exception, match="Job with reference LMS11111-AA1.12345 already exists"
    ):
        service.add_job("LMS11111-AA1.12345", "Region 2")


def test_get_jobs_model(service: FakeTotalmobileService):
    # arrange
    service.add_job("LMS11111-AA1.12345", "Region 1")
    service.add_job("LMS11111-AA1.56789", "Region 1", True)
    service.add_job("LMS11111-AA1.54321", "Region 2", True)

    # act
    jobs_model = service.get_jobs_model("world-id-1")

    # assert
    assert jobs_model.questionnaire_jobs == {
        "LMS11111_AA1": [
            Job("LMS11111-AA1.12345", "12345", False, False),
            Job("LMS11111-AA1.56789", "56789", True, False),
        ]
    }


def test_get_world_model(service: FakeTotalmobileService):
    # arrange
    model = service.get_world_model()

    # assert
    assert isinstance(model, TotalmobileWorldModel)
    assert model.worlds == [
        World(region="Region 1", id="world-id-1"),
        World(region="Region 2", id="world-id-2"),
        World(region="Region 3", id="world-id-3"),
        World(region="Region 4", id="world-id-4"),
        World(region="Region 5", id="world-id-5"),
        World(region="Region 6", id="world-id-6"),
        World(region="Region 7", id="world-id-7"),
        World(region="Region 8", id="world-id-8"),
    ]
