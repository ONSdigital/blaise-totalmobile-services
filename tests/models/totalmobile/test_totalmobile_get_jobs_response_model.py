from datetime import timedelta, datetime

import pytest

from client.optimise import GetJobResponse, Identity, DueDate
from models.totalmobile.totalmobile_get_jobs_response_model import (
    Job,
    TotalmobileGetJobsResponseModel,
)


def test_total_mobile_job_models_maps_expected_list_of_models_from_job_response():
    # arrange
    job_response = [
        GetJobResponse(identity=Identity(reference="LMS1111-AA1.12345"),
                       dueDate=DueDate(end=datetime.today() + timedelta(days=4)), visitComplete=True),
        GetJobResponse(identity=Identity(reference="LMS2222-BB2.22222"),
                       dueDate=DueDate(end=datetime.today() + timedelta(days=2)), visitComplete=False),
        GetJobResponse(identity=Identity(reference="LMS1111-AA1.67890"),
                       dueDate=DueDate(end=datetime.today() + timedelta(days=3)), visitComplete=False),
    ]

    # act
    result = TotalmobileGetJobsResponseModel.from_get_jobs_response(job_response)

    # assert
    assert len(result.questionnaire_jobs) == 2

    assert len(result.questionnaire_jobs["LMS1111_AA1"]) == 2
    assert result.questionnaire_jobs["LMS1111_AA1"][0].case_id == "12345"
    assert result.questionnaire_jobs["LMS1111_AA1"][0].reference == "LMS1111-AA1.12345"
    assert result.questionnaire_jobs["LMS1111_AA1"][0].visit_complete is True
    assert result.questionnaire_jobs["LMS1111_AA1"][0].past_field_period is False

    assert result.questionnaire_jobs["LMS1111_AA1"][1].case_id == "67890"
    assert result.questionnaire_jobs["LMS1111_AA1"][1].reference == "LMS1111-AA1.67890"
    assert result.questionnaire_jobs["LMS1111_AA1"][1].visit_complete is False
    assert result.questionnaire_jobs["LMS1111_AA1"][1].past_field_period is True

    assert len(result.questionnaire_jobs["LMS2222_BB2"]) == 1
    assert result.questionnaire_jobs["LMS2222_BB2"][0].case_id == "22222"
    assert result.questionnaire_jobs["LMS2222_BB2"][0].reference == "LMS2222-BB2.22222"
    assert result.questionnaire_jobs["LMS2222_BB2"][0].visit_complete is False
    assert result.questionnaire_jobs["LMS2222_BB2"][0].past_field_period is True


def test_questionnaires_with_incomplete_jobs_returns_expected_dictionary():
    # arrange
    job_response = [
        GetJobResponse(identity=Identity(reference="LMS1111-AA1.12345"),
                       dueDate=DueDate(end=datetime.today() + timedelta(days=4)), visitComplete=True),
        GetJobResponse(identity=Identity(reference="LMS2222-BB2.22222"),
                       dueDate=DueDate(end=datetime.today() + timedelta(days=4)), visitComplete=False),
        GetJobResponse(identity=Identity(reference="LMS2222-BB2.33333"),
                       dueDate=DueDate(end=datetime.today() + timedelta(days=4)), visitComplete=True),
        GetJobResponse(identity=Identity(reference="LMS1111-AA1.67890"),
                       dueDate=DueDate(end=datetime.today() + timedelta(days=4)), visitComplete=True),
    ]

    # act
    model = TotalmobileGetJobsResponseModel.from_get_jobs_response(job_response)
    result = model.questionnaires_with_incomplete_jobs()

    # assert
    assert len(result) == 1

    assert result["LMS2222_BB2"] == [
        Job("LMS2222-BB2.22222", "22222", False, False),
    ]


def test_from_get_jobs_response_skips_jobs_with_bad_references():
    # arrange
    job_response = [
        GetJobResponse(identity=Identity(reference="LMS1111-AA1.12345"),
                       dueDate=DueDate(end=None), visitComplete=False),
        GetJobResponse(identity=Identity(reference="this is not a valid reference"),
                       dueDate=DueDate(end=None), visitComplete=False),
        GetJobResponse(identity=Identity(reference="LMS1111-AA1.67890"),
                       dueDate=DueDate(end=None), visitComplete=False),
    ]

    # act
    model = TotalmobileGetJobsResponseModel.from_get_jobs_response(job_response)
    result = model.questionnaires_with_incomplete_jobs()

    # assert
    assert result["LMS1111_AA1"] == [
        Job("LMS1111-AA1.12345", "12345", False, False),
        Job("LMS1111-AA1.67890", "67890", False, False),
    ]


@pytest.mark.parametrize("days", [4, 5, 6])
def test_field_period_has_expired_returns_false_when_due_date_is_more_than_3_days_in_the_future(days: int):
    # arrange
    desired_due_date = datetime.today().date() + timedelta(days)
    due_date = datetime.combine(desired_due_date, datetime.min.time())

    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(due_date)

    # assert
    assert result is False


@pytest.mark.parametrize("days", [-2, -1, 0, 1, 2])
def test_field_period_has_expired_returns_true_when_due_date_is_less_than_3_days_in_the_future(days: int):
    # arrange
    desired_due_date = datetime.today().date() + timedelta(days)
    due_date = datetime.combine(desired_due_date, datetime.min.time())

    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(due_date)

    # assert
    assert result is True


def test_field_period_has_expired_returns_true_when_due_date_is_3_days_in_the_future():
    # arrange
    desired_due_date = datetime.today().date() + timedelta(3)
    due_date = datetime.combine(desired_due_date, datetime.min.time())

    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(due_date)

    # assert
    assert result is True


def test_field_period_has_expired_returns_true_when_due_date_is_3_days_23_hours_59_mins_59_secs_in_the_future():
    # arrange
    desired_due_date = datetime.today().date() + timedelta(days=3, hours=23, minutes=59, seconds=59)
    due_date = datetime.combine(desired_due_date, datetime.min.time())

    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(due_date)

    # assert
    assert result is True


def test_field_period_has_expired_returns_false_when_due_date_not_provided():
    # act
    result = TotalmobileGetJobsResponseModel.field_period_has_expired(None)

    # assert
    assert result is False

