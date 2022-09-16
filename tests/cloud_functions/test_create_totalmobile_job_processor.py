import logging
from unittest.mock import create_autospec

import flask
import pytest

from client import AuthException
from client.errors import BadRequest
from cloud_functions.create_totalmobile_jobs_processor import (
    create_totalmobile_jobs_processor,
)
from models.cloud_tasks.totalmobile_create_job_model import TotalmobileCreateJob
from services.totalmobile_service import TotalmobileService


def test_create_totalmobile_job(mock_create_job_task):
    mock_request = flask.Request.from_values(json=mock_create_job_task)
    total_mobile_service_mock = create_autospec(TotalmobileService)
    assert (
        create_totalmobile_jobs_processor(mock_request, total_mobile_service_mock)
        == "Done"
    )


def test_create_totalmobile_job_error(mock_create_job_task):
    mock_request = flask.Request.from_values(json=mock_create_job_task)
    total_mobile_service_mock = create_autospec(TotalmobileService)
    total_mobile_service_mock.create_job.side_effect = AuthException()
    with pytest.raises(AuthException):
        create_totalmobile_jobs_processor(mock_request, total_mobile_service_mock)


def test_create_totalmobile_job_when_job_already_exists(mock_create_job_task, caplog):
    mock_request = flask.Request.from_values(json=mock_create_job_task)
    total_mobile_service_mock = create_autospec(TotalmobileService)
    total_mobile_service_mock.create_job.side_effect = BadRequest(
        error_details={
            "jobEntity": ["Job already exists with Reference DST2101-AA1.100100."]
        }
    )
    with caplog.at_level(logging.WARNING):
        create_totalmobile_jobs_processor(mock_request, total_mobile_service_mock)
    assert (
        "root",
        logging.WARNING,
        "Job already exists with Reference DST2101-AA1.100100.",
    ) in caplog.record_tuples


@pytest.mark.parametrize(
    "error_details",
    [
        ({"jobEntity": ["You made a bad request"]}),
        (None),
        ({}),
        ({"jobEntity": ""}),
        ({"jobEntity": []}),
        (123),
    ],
)
def test_create_totalmobile_job_raises_bad_request_error(
    mock_create_job_task, error_details
):
    mock_request = flask.Request.from_values(json=mock_create_job_task)
    total_mobile_service_mock = create_autospec(TotalmobileService)
    total_mobile_service_mock.create_job.side_effect = BadRequest(
        error_details=error_details
    )
    with pytest.raises(BadRequest):
        create_totalmobile_jobs_processor(mock_request, total_mobile_service_mock)
