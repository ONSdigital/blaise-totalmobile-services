from client import OptimiseClient, AuthException
from config import Config
from unittest import mock
from cloud_functions.create_job import create_totalmobile_job
import flask
import pytest


@mock.patch.object(Config, "validate")
@mock.patch.object(OptimiseClient, "create_job")
def test_create_totalmobile_job(
    _mock_create_job, _mock_config_validate, mock_create_job_task
):
    mock_request = flask.Request.from_values(json=mock_create_job_task)
    assert create_totalmobile_job(mock_request) == "Done"


@mock.patch.object(Config, "validate")
@mock.patch.object(OptimiseClient, "create_job")
def test_create_totalmobile_job_error(
    mock_create_job, _mock_config_validate, mock_create_job_task
):
    mock_create_job.side_effect = AuthException()
    mock_request = flask.Request.from_values(json=mock_create_job_task)
    with pytest.raises(AuthException):
        create_totalmobile_job(mock_request)
