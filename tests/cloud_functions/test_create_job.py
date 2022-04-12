from unittest import mock

import flask
import pytest

from appconfig import Config
from client import AuthException, OptimiseClient
from cloud_functions.create_totalmobile_job import (
    create_job_payload,
    create_totalmobile_job,
    description,
    job_reference,
    validate_case_data,
    validate_request,
)


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


def test_validate_request(mock_create_job_task):
    validate_request(mock_create_job_task)


def test_validate_request_missing_fields():
    with pytest.raises(Exception) as err:
        validate_request({"world_id": ""})
    assert (
        str(err.value)
        == "Required fields missing from request payload: ['instrument', 'case']"
    )


def test_validate_case_data(mock_create_job_task):
    validate_case_data(mock_create_job_task["case"])


def test_validate_case_data_missing_fields():
    with pytest.raises(Exception) as err:
        validate_case_data(
            {"qDataBag.UPRN_Latitude": "", "qDataBag.UPRN_Longitude": ""}
        )
    assert (
        str(err.value)
        == "Required fields missing from case data: ['qiD.Serial_Number', 'qDataBag.Prem1', 'qDataBag.Prem2', 'qDataBag.Prem3', 'qDataBag.PostTown', 'qDataBag.PostCode', 'qDataBag.TelNo', 'qDataBag.TelNo2']"
    )


def test_create_job_payload(mock_create_job_task):
    assert create_job_payload(mock_create_job_task) == {
        "additionalProperties": [
            {"name": "study", "value": "DST2101A"},
            {"name": "case_id", "value": "100100"},
        ],
        "clientReference": "2",
        "contact": {
            "contactDetail": {
                "contactId": "DST",
                "contactIdLabel": "A",
                "preferredName": "101",
            },
            "homePhone": "TelNo",
            "mobilePhone": "TelNo2",
            "name": "PostCode",
        },
        "description": "Study: DST2101A\nCase ID: 100100\n\nIf you need to provide a UAC please contact SEL",
        "dueDate": {"end": "", "start": ""},
        "duration": 30,
        "identity": {"reference": "DST2101A.100100"},
        "location": {
            "address": "prem1, prem2, PostTown",
            "addressDetail": {
                "addressLine2": "prem1",
                "addressLine3": "prem2",
                "addressLine4": "PostTown",
                "coordinates": {
                    "latitude": "UPRN_Latitude",
                    "longitude": "UPRN_Longitude",
                },
                "name": "prem1, prem2, PostTown",
                "postCode": "PostCode",
            },
            "reference": "100100",
        },
        "origin": "ONS",
        "skills": [{"identity": {"reference": "KTN"}}],
        "workType": "KTN",
    }


def test_job_reference():
    assert job_reference("LMS2201A_BB1", "100100") == "LMS2201A-BB1.100100"


def test_description():
    assert (
        description("LMS2201A_BB1", "100100")
        == """Study: LMS2201A_BB1
Case ID: 100100

If you need to provide a UAC please contact SEL"""
    )
