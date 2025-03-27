import pytest

from models.common.totalmobile.totalmobile_world_model import (
    TotalmobileWorldModel,
    World,
)
from models.delete.totalmobile_get_jobs_response_model import Job
from services.totalmobile_service import DeleteJobError
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService


@pytest.fixture()
def service() -> FakeTotalmobileService:
    return FakeTotalmobileService()


def test_delete_job(service: FakeTotalmobileService):
    # arrange
    service.add_job("LMS11111-AA1.12345", "Region 1")
    service.add_job("LMS11111-AA1.34680", "Region 1")

    # act
    service.delete_job("world-id-1", "LMS11111-AA1.12345")

    # assert
    assert not service.job_exists("LMS11111-AA1.12345")
    assert service.job_exists("LMS11111-AA1.34680")


def test_delete_job_raises_when_set_to_error(service: FakeTotalmobileService):
    # arrange
    service.add_job("LMS11111-AA1.12345", "Region 1")
    service.method_throws_exception("delete_job")

    # act & assert
    with pytest.raises(DeleteJobError):
        service.delete_job("world-id-1", "LMS11111-AA1.12345")


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


class TestGetJobsModel:
    def test_raises_when_no_jobs_exist(self, service: FakeTotalmobileService):
        with pytest.raises(
            Exception, match="get_jobs_models was called when no jobs were present"
        ):
            service.get_jobs_model("world-id-1")

    @pytest.mark.parametrize(
        "region_name,world_id",
        [
            (region_name, world_id)
            for region_name, world_id in FakeTotalmobileService.REGIONS.items()
        ],
    )
    def test_returns_the_models_in_the_given_region(
        self, region_name, world_id, service: FakeTotalmobileService
    ):
        # arrange
        service.add_job("LMS11111-AA1.12345", region_name, False)
        service.add_job("LMS11111-AA1.56789", region_name, True)

        # act
        jobs_model = service.get_jobs_model(world_id)

        # assert
        assert jobs_model.questionnaire_jobs == {
            "LMS11111_AA1": [
                Job("LMS11111-AA1.12345", "12345", False, False, None, "LMS"),
                Job("LMS11111-AA1.56789", "56789", True, False, None, "LMS"),
            ]
        }

    def test_raise_when_configured_to(self, service: FakeTotalmobileService):
        # arrange
        service.add_job("LMS11111-AA1.12345", "Region 1", False)
        service.method_throws_exception("get_jobs_model")

        # act & assert
        with pytest.raises(Exception, match="get_jobs_model has errored"):
            service.get_jobs_model("world-id-1")

    def test_does_not_return_jobs_from_another_region(
        self, service: FakeTotalmobileService
    ):
        # arrange
        service.add_job("LMS11111-AA1.12345", "Region 2", False)

        # act
        jobs_model = service.get_jobs_model("world-id-1")

        # assert
        assert jobs_model.questionnaire_jobs == {}

    def test_returns_jobs_grouped_by_questionnaire(
        self, service: FakeTotalmobileService
    ):
        # arrange
        service.add_job("LMS11111-AA1.11111", "Region 1", False)
        service.add_job("LMS11111-BB1.11111", "Region 1", False)
        service.add_job("LMS11111-BB1.22222", "Region 1", False)

        # act
        jobs_model = service.get_jobs_model("world-id-1")

        # assert
        assert jobs_model.questionnaire_jobs == {
            "LMS11111_AA1": [
                Job(
                    "LMS11111-AA1.11111",
                    "11111",
                    False,
                    False,
                    None,
                    "LMS",
                )
            ],
            "LMS11111_BB1": [
                Job("LMS11111-BB1.11111", "11111", False, False, None, "LMS"),
                Job("LMS11111-BB1.22222", "22222", False, False, None, "LMS"),
            ],
        }

    def test_returns_allocated_resource_when_present(
        self, service: FakeTotalmobileService
    ):
        # arrange
        service.add_job(
            "LMS11111-AA1.11111",
            "Region 1",
            False,
            allocated_resource_reference="carl.minion",
        )

        # act
        jobs_model = service.get_jobs_model("world-id-1")

        # assert
        assert jobs_model.questionnaire_jobs == {
            "LMS11111_AA1": [
                Job(
                    "LMS11111-AA1.11111",
                    "11111",
                    False,
                    False,
                    "carl.minion",
                    "LMS",
                )
            ],
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
        World(region="Region 9", id="world-id-9"),
        World(region="Region 10", id="world-id-10"),
        World(region="Region 11", id="world-id-11"),
        World(region="Region 12", id="world-id-12"),
    ]


class TestJobHasBeenRecalled:
    def test_returns_false_when_no_jobs_have_been_recalled(
        self, service: FakeTotalmobileService
    ):
        assert (
            service.job_has_been_recalled("stuart.minion", "LMS2206-AA1.11111") is False
        )

    def test_returns_true_when_the_job_has_been_recalled(
        self, service: FakeTotalmobileService
    ):
        service.recall_job("bob.minion", "LMS", "LMS2206-AA1.22222")
        assert service.job_has_been_recalled("bob.minion", "LMS2206-AA1.22222") is True

    def test_returns_false_when_a_different_job_has_been_recalled(
        self, service: FakeTotalmobileService
    ):
        service.recall_job("bob.minion", "LMS", "LMS2206-AA1.22222")
        assert service.job_has_been_recalled("bob.minion", "LMS2206-AA1.11111") is False

    def test_returns_false_when_the_job_has_been_recalled_from_a_different_resource(
        self, service: FakeTotalmobileService
    ):
        service.recall_job("bob.minion", "LMS", "LMS2206-AA1.11111")
        assert (
            service.job_has_been_recalled("norbert.minion", "LMS2206-AA1.11111")
            is False
        )
