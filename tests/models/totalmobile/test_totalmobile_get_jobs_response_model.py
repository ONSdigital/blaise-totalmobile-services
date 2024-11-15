from datetime import datetime, timedelta

import pytest

from client.optimise import DueDate, GetJobResponse, Identity
from models.delete.totalmobile_get_jobs_response_model import (
    Job,
    TotalmobileGetJobsResponseModel,
)
from tests.helpers.date_helper import (
    format_date_as_totalmobile_formatted_string,
    get_date_as_totalmobile_formatted_string,
)


def test_total_mobile_job_models_maps_expected_list_of_models_from_job_response():
    # arrange

    job_response = [
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.12345"),
            dueDate=DueDate(end=get_date_as_totalmobile_formatted_string(4)),
            visitComplete=True,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS2222-BB2.22222"),
            dueDate=DueDate(end=get_date_as_totalmobile_formatted_string(2)),
            visitComplete=False,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.67890"),
            dueDate=DueDate(end=get_date_as_totalmobile_formatted_string(3)),
            visitComplete=False,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.45678"),
            dueDate=DueDate(end=None),
            visitComplete=False,
            allocatedResource=None,
            workType="LMS",
        ),
    ]

    # act
    result = TotalmobileGetJobsResponseModel.from_get_jobs_response(job_response)

    # assert
    assert len(result.questionnaire_jobs) == 2

    assert len(result.questionnaire_jobs["LMS1111_AA1"]) == 3
    assert result.questionnaire_jobs["LMS1111_AA1"][0].case_id == "12345"
    assert result.questionnaire_jobs["LMS1111_AA1"][0].reference == "LMS1111-AA1.12345"
    assert result.questionnaire_jobs["LMS1111_AA1"][0].visit_complete is True
    assert result.questionnaire_jobs["LMS1111_AA1"][0].past_field_period is False

    assert result.questionnaire_jobs["LMS1111_AA1"][1].case_id == "67890"
    assert result.questionnaire_jobs["LMS1111_AA1"][1].reference == "LMS1111-AA1.67890"
    assert result.questionnaire_jobs["LMS1111_AA1"][1].visit_complete is False
    assert result.questionnaire_jobs["LMS1111_AA1"][1].past_field_period is True

    assert result.questionnaire_jobs["LMS1111_AA1"][2].case_id == "45678"
    assert result.questionnaire_jobs["LMS1111_AA1"][2].reference == "LMS1111-AA1.45678"
    assert result.questionnaire_jobs["LMS1111_AA1"][2].visit_complete is False
    assert result.questionnaire_jobs["LMS1111_AA1"][2].past_field_period is False

    assert len(result.questionnaire_jobs["LMS2222_BB2"]) == 1
    assert result.questionnaire_jobs["LMS2222_BB2"][0].case_id == "22222"
    assert result.questionnaire_jobs["LMS2222_BB2"][0].reference == "LMS2222-BB2.22222"
    assert result.questionnaire_jobs["LMS2222_BB2"][0].visit_complete is False
    assert result.questionnaire_jobs["LMS2222_BB2"][0].past_field_period is True


def test_questionnaires_with_incomplete_jobs_returns_expected_dictionary():
    # arrange
    job_response = [
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.12345"),
            dueDate=DueDate(end=None),
            visitComplete=True,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS2222-BB2.22222"),
            dueDate=DueDate(end=None),
            visitComplete=False,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS2222-BB2.33333"),
            dueDate=DueDate(end=None),
            visitComplete=True,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.67890"),
            dueDate=DueDate(end=None),
            visitComplete=True,
            allocatedResource=None,
            workType="LMS",
        ),
    ]

    # act
    model = TotalmobileGetJobsResponseModel.from_get_jobs_response(job_response)
    result = model.questionnaires_with_incomplete_jobs()

    # assert
    assert len(result) == 1

    assert result["LMS2222_BB2"] == [
        Job("LMS2222-BB2.22222", "22222", False, False, None, "LMS"),
    ]


def test_from_get_jobs_response_skips_jobs_with_bad_references():
    # arrange
    job_response = [
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.12345"),
            dueDate=DueDate(end=None),
            visitComplete=False,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="this is not a valid reference"),
            dueDate=DueDate(end=None),
            visitComplete=False,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.67890"),
            dueDate=DueDate(end=None),
            visitComplete=False,
            allocatedResource=dict(reference="stuart.minion"),
            workType="LMS",
        ),
    ]

    # act
    model = TotalmobileGetJobsResponseModel.from_get_jobs_response(job_response)
    result = model.questionnaires_with_incomplete_jobs()

    # assert
    assert result["LMS1111_AA1"] == [
        Job("LMS1111-AA1.12345", "12345", False, False, None, "LMS"),
        Job("LMS1111-AA1.67890", "67890", False, False, "stuart.minion", "LMS"),
    ]


@pytest.mark.parametrize("days", [4, 5, 6])
def test_field_period_has_expired_returns_false_when_due_date_is_more_than_3_days_in_the_future_for_lms(
    days: int,
):
    # arrange
    due_date_str = get_date_as_totalmobile_formatted_string(days)

    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(due_date_str, "LMS")

    # assert
    assert result is False


@pytest.mark.parametrize("days", [-2, -1, 0, 1, 2])
def test_field_period_has_expired_returns_true_when_due_date_is_less_than_3_days_in_the_future_for_lms(
    days: int,
):
    # arrange
    due_date_str = get_date_as_totalmobile_formatted_string(days)

    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(due_date_str, "LMS")

    # assert
    assert result is True


def test_field_period_has_expired_returns_true_when_due_date_is_3_days_in_the_future_for_lms():
    # arrange
    due_date_str = get_date_as_totalmobile_formatted_string(3)

    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(due_date_str, "LMS")

    # assert
    assert result is True

def test_field_period_has_expired_returns_true_when_due_date_is_3_days_23_hours_59_mins_59_secs_in_the_future_for_lms():
    # arrange
    desired_due_date = datetime.today().date() + timedelta(
        days=3, hours=23, minutes=59, seconds=59
    )
    due_date = datetime.combine(desired_due_date, datetime.min.time())
    due_date_str = format_date_as_totalmobile_formatted_string(due_date)

    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(due_date_str, "LMS")

    # assert
    assert result is True

def test_field_period_has_expired_returns_true_when_due_date_is_today_for_non_lms_surveys():
    # arrange
    due_date_str = get_date_as_totalmobile_formatted_string(0)

    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(due_date_str, "FRS")

    # assert
    assert result is True

def test_field_period_has_expired_returns_true_when_due_date_is_1_day_in_the_past_for_non_lms_surveys():
    # arrange
    desired_due_date = datetime.today().date() + timedelta(
        days=-1, hours=0, minutes=0, seconds=0
    )
    due_date = datetime.combine(desired_due_date, datetime.min.time())
    due_date_str = format_date_as_totalmobile_formatted_string(due_date)

    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(due_date_str, "FRS")

    # assert
    assert result is True

def test_field_period_has_expired_returns_true_when_due_date_is_1_day_in_the_future_for_non_lms_surveys():
    # arrange
    desired_due_date = datetime.today().date() + timedelta(
        days=1, hours=0, minutes=0, seconds=0
    )
    due_date = datetime.combine(desired_due_date, datetime.min.time())
    due_date_str = format_date_as_totalmobile_formatted_string(due_date)

    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(due_date_str, "FRS")

    # assert
    assert result is False

def test_field_period_has_expired_returns_false_when_due_date_not_provided():
    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(None, "LMS")

    # assert
    assert result is False


def test_total_number_of_incomplete_jobs_returns_expected_number():
    # arrange

    job_response = [
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.12345"),
            dueDate=DueDate(end=get_date_as_totalmobile_formatted_string(4)),
            visitComplete=True,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS2222-BB2.22222"),
            dueDate=DueDate(end=get_date_as_totalmobile_formatted_string(2)),
            visitComplete=False,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.67890"),
            dueDate=DueDate(end=get_date_as_totalmobile_formatted_string(3)),
            visitComplete=False,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="FRS2504A.12345"),
            dueDate=DueDate(end=get_date_as_totalmobile_formatted_string(0)),
            visitComplete=False,
            allocatedResource=None,
            workType="FRS",
        ),
        GetJobResponse(
            identity=Identity(reference="FRS2504A.56789"),
            dueDate=DueDate(end=get_date_as_totalmobile_formatted_string(-1)),
            visitComplete=False,
            allocatedResource=None,
            workType="FRS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.45678"),
            dueDate=DueDate(end=None),
            visitComplete=False,
            allocatedResource=None,
            workType="LMS",
        ),
    ]

    model = TotalmobileGetJobsResponseModel.from_get_jobs_response(job_response)

    # act
    result = model.total_number_of_incomplete_jobs()

    # assert
    assert result == 5
