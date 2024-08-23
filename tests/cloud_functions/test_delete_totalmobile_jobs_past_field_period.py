import logging

import pytest

from cloud_functions.delete_totalmobile_jobs_past_field_period import (
    delete_totalmobile_jobs_past_field_period,
)
from services.delete.blaise_case_outcome_service import BlaiseCaseOutcomeService
from tests.fakes.fake_blaise_service import FakeBlaiseService
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService
from tests.helpers.date_helper import get_date_as_totalmobile_formatted_string


@pytest.fixture()
def totalmobile_service() -> FakeTotalmobileService:
    return FakeTotalmobileService()


@pytest.fixture()
def blaise_service() -> FakeBlaiseService:
    return FakeBlaiseService()


@pytest.fixture()
def blaise_outcome_service(blaise_service) -> BlaiseCaseOutcomeService:
    return BlaiseCaseOutcomeService(blaise_service)


@pytest.fixture(autouse=True)
def setup(
    totalmobile_service: FakeTotalmobileService,
    blaise_service: FakeBlaiseService,
):
    blaise_service.add_questionnaire("LMS2209_AA1")
    blaise_service.add_case_to_questionnaire(
        questionnaire="LMS2209_AA1",
        case_id="10000",
        outcome_code=310,
        wave=1,
    )
    totalmobile_service.add_job(
        "LMS2209-AA1.10000",
        "Region 1",
        allocated_resource_reference="darwin.minion",
        due_date=get_date_as_totalmobile_formatted_string(int(3)),
    )


def test_delete_totalmobile_jobs_past_field_period_deletes_completed_jobs(
    totalmobile_service: FakeTotalmobileService,
    blaise_outcome_service: BlaiseCaseOutcomeService,
):
    delete_totalmobile_jobs_past_field_period(
        blaise_outcome_service, totalmobile_service
    )

    assert not totalmobile_service.job_exists("LMS2209-AA1.10000")


def test_delete_totalmobile_jobs_past_field_period_recalls_completed_jobs(
    totalmobile_service: FakeTotalmobileService,
    blaise_outcome_service: BlaiseCaseOutcomeService,
):
    delete_totalmobile_jobs_past_field_period(
        blaise_outcome_service, totalmobile_service
    )

    assert totalmobile_service.job_has_been_recalled(
        "darwin.minion", "LMS2209-AA1.10000"
    )


def test_delete_totalmobile_jobs_past_field_period_logs_activity(
    totalmobile_service: FakeTotalmobileService,
    blaise_outcome_service: BlaiseCaseOutcomeService,
    caplog,
):
    with caplog.at_level(logging.INFO):
        delete_totalmobile_jobs_past_field_period(
            blaise_outcome_service, totalmobile_service
        )

    assert (
        "root",
        logging.INFO,
        "job with case ID 10000 has past field period value of True",
    ) in caplog.record_tuples
    assert (
        "root",
        logging.INFO,
        "Successfully removed job LMS2209-AA1.10000 from Totalmobile",
    ) in caplog.record_tuples


def test_delete_totalmobile_jobs_past_field_period_returns_done(
    totalmobile_service: FakeTotalmobileService,
    blaise_outcome_service: BlaiseCaseOutcomeService,
    caplog,
):
    result = delete_totalmobile_jobs_past_field_period(
        blaise_outcome_service, totalmobile_service
    )

    assert result == "Done"
