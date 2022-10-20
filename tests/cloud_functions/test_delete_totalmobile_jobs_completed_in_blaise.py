import logging

import pytest

from cloud_functions.delete_totalmobile_jobs_completed_in_blaise import (
    delete_totalmobile_jobs_completed_in_blaise,
)
from tests.fakes.fake_blaise_service import FakeBlaiseService
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService


@pytest.fixture()
def totalmobile_service() -> FakeTotalmobileService:
    return FakeTotalmobileService()


@pytest.fixture()
def blaise_service() -> FakeBlaiseService:
    return FakeBlaiseService()


@pytest.fixture(autouse=True)
def setup(
    totalmobile_service: FakeTotalmobileService,
    blaise_service: FakeBlaiseService,
):
    blaise_service.add_questionnaire("LMS2209_AA1")
    blaise_service.add_case_to_questionnaire(
        questionnaire="LMS2209_AA1",
        case_id="10000",
        outcome_code=110,
        wave="1",
    )
    totalmobile_service.add_job(
        "LMS2209-AA1.10000", "Region 1", allocated_resource_reference="darwin.minion"
    )


def test_delete_totalmobile_jobs_completed_in_blaise_deletes_completed_jobs(
    totalmobile_service: FakeTotalmobileService,
    blaise_service: FakeBlaiseService,
):
    delete_totalmobile_jobs_completed_in_blaise(blaise_service, totalmobile_service)

    assert not totalmobile_service.job_exists("LMS2209-AA1.10000")


def test_delete_totalmobile_jobs_completed_in_blaise_recalls_completed_jobs(
    totalmobile_service: FakeTotalmobileService,
    blaise_service: FakeBlaiseService,
):
    delete_totalmobile_jobs_completed_in_blaise(blaise_service, totalmobile_service)

    assert totalmobile_service.job_has_been_recalled(
        "darwin.minion", "LMS2209-AA1.10000"
    )


def test_delete_totalmobile_jobs_completed_in_blaise_logs_activity(
    totalmobile_service: FakeTotalmobileService,
    blaise_service: FakeBlaiseService,
    caplog,
):
    with caplog.at_level(logging.INFO):
        delete_totalmobile_jobs_completed_in_blaise(blaise_service, totalmobile_service)

    assert (
        "root",
        logging.INFO,
        "Found 1 incomplete jobs in totalmobile for world world-id-1",
    ) in caplog.record_tuples
    assert (
        "root",
        logging.INFO,
        "Successfully removed job LMS2209-AA1.10000 from Totalmobile",
    ) in caplog.record_tuples


def test_delete_totalmobile_jobs_completed_in_blaise_returns_done(
    totalmobile_service: FakeTotalmobileService,
    blaise_service: FakeBlaiseService,
    caplog,
):
    result = delete_totalmobile_jobs_completed_in_blaise(
        blaise_service, totalmobile_service
    )

    assert result == "Done"
