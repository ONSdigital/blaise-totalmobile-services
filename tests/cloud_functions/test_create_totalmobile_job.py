from unittest.mock import create_autospec

import flask
import pytest

from client import AuthException
from cloud_functions.create_totalmobile_job import create_totalmobile_job
from services.totalmobile_service import TotalmobileService


def test_create_totalmobile_job(mock_create_job_task):
    mock_request = flask.Request.from_values(json=mock_create_job_task)
    total_mobile_service_mock = create_autospec(TotalmobileService)
    assert create_totalmobile_job(mock_request, total_mobile_service_mock) == "Done"


def test_create_totalmobile_job_error(mock_create_job_task):
    mock_request = flask.Request.from_values(json=mock_create_job_task)
    total_mobile_service_mock = create_autospec(TotalmobileService)
    total_mobile_service_mock.create_job.side_effect = AuthException()
    with pytest.raises(AuthException):
        create_totalmobile_job(mock_request, total_mobile_service_mock)
