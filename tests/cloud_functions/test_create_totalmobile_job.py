from unittest import mock

import flask
import pytest
import logging

from appconfig import Config
from client import AuthException, OptimiseClient
from cloud_functions.create_totalmobile_job import (
    create_job_payload,
    create_totalmobile_job,
    create_description,
    create_job_reference,
    validate_case_data,
    validate_request,
    validate_totalmobile_payload
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


def test_validate_request_when_missing_fields():
    with pytest.raises(Exception) as err:
        validate_request({"world_id": ""})
    assert (
            str(err.value)
            == "Required fields missing from request payload: ['questionnaire', 'case']"
    )


def test_validate_case_data(mock_create_job_task):
    validate_case_data(mock_create_job_task["case"])


def test_validate_case_data_when_missing_fields():
    with pytest.raises(Exception) as err:
        validate_case_data(
            {
                "qiD.Serial_Number": "100100",
                "dataModelName": "DST2101_AA1",
                "qDataBag.TLA": "DST",
                "qDataBag.Wave": "1",
                "qDataBag.Prem1": "Ye Olde Fighting Cocks",
                "qDataBag.Prem2": "16 Abbey Mill Lane",
                "qDataBag.Prem3": "",
                "qDataBag.District": "",
                "qDataBag.PostTown": "St Albans",
                "qDataBag.PostCode": "AL3 4HE",
                "qDataBag.TelNo": "",
                "qDataBag.TelNo2": "",
                "telNoAppt": "",
                "hOut": "",
                "qDataBag.Priority": "1",
                "qDataBag.FieldRegion": "",
                "qDataBag.FieldTeam": "The A Team",
                "qDataBag.WaveComDTE": "2020-11-17",
            }
        )
    assert (
            str(err.value)
            == "Required fields missing from case data: ['qDataBag.UPRN_Latitude', 'qDataBag.UPRN_Longitude']"
    )


def test_create_job_payload(mock_create_job_task):
    assert create_job_payload(mock_create_job_task) == {
        "identity": {
            "reference": "DST2101-AA1.100100"
            },
        "description": "Study: DST2101_AA1\nCase ID: 100100",
        "origin": "ONS",
        "duration": 15,
        "workType": "DST",
        "skills": [
            {
                "identity": {
                    "reference": "DST"
                    }
            }
        ],
        "dueDate": {
            "end": "2020-11-17",
        },
        "location": {
            "addressDetail": {
                "addressLine1": "Ye Olde Fighting Cocks",
                "addressLine2": "16 Abbey Mill Lane",
                "addressLine3": "",
                "addressLine4": "",
                "addressLine5": "St Albans",
                "postCode": "AL3 4HE",
                "coordinates": {
                    "latitude": "51.748930",
                    "longitude": "-0.346820",
                },
            },
        },
        "contact": {
            "name": "AL3 4HE",
        },
        "additionalProperties": [
            {
                "name": "surveyName"
                , "value": "DST2101_AA1"
            },
            {
                "name": "tla",
                "value": "DST"
            },
            {
                "name": "wave",
                "value": "1"
            },
            {
                "name": "priority",
                "value": "1"
            },
            {
                "name": "fieldTeam",
                "value": "The A Team"
            },
            {
                "name": "uac1",
                "value": "8176"
            },
            {
                "name": "uac2",
                "value": "4726"
            },
            {
                "name": "uac3",
                "value": "3993"
            },
        ],
    }


def test_an_error_is_logged_when_the_duration_field_is_missing_from_the_totalmobile_payload(caplog):
    totalmobile_payload = {
        "identity": {
            "reference": "DST2101-AA1.100100"
            },
        "description": "Study: DST2101_AA1\nCase ID: 100100",
        "origin": "ONS",
        "workType": "DST",
        "skills": [
            {
                "identity": {
                    "reference": "DST"
                    }
            }
        ],
        "dueDate": {
            "end": "2020-11-17",
        },
        "location": {
            "addressDetail": {
                "addressLine1": "Ye Olde Fighting Cocks",
                "addressLine2": "16 Abbey Mill Lane",
                "addressLine3": "",
                "addressLine4": "",
                "addressLine5": "St Albans",
                "postCode": "AL3 4HE",
                "coordinates": {
                    "latitude": "51.748930",
                    "longitude": "-0.346820",
                },
            },
        },
        "contact": {
            "name": "AL3 4HE",
        },
        "additionalProperties": [
            {
                "name": "surveyName"
                , "value": "DST2101_AA1"
            },
            {
                "name": "tla",
                "value": "DST"
            },
            {
                "name": "wave",
                "value": "1"
            },
            {
                "name": "priority",
                "value": "1"
            },
            {
                "name": "fieldTeam",
                "value": "The A Team"
            },
        ],
    }

    validate_totalmobile_payload(totalmobile_payload)
    assert (
        'root', logging.WARNING, "Totalmobile payload was sent without the 'duration' field") in caplog.record_tuples


def test_an_error_is_logged_when_the_origin_field_is_missing_from_the_totalmobile_payload(caplog):
    totalmobile_payload = {
        "identity": {
            "reference": "DST2101-AA1.100100"
            },
        "description": "Study: DST2101_AA1\nCase ID: 100100",
        "duration": 15,
        "workType": "DST",
        "skills": [
            {
                "identity": {
                    "reference": "DST"
                    }
            }
        ],
        "dueDate": {
            "end": "2020-11-17",
        },
        "location": {
            "addressDetail": {
                "addressLine1": "Ye Olde Fighting Cocks",
                "addressLine2": "16 Abbey Mill Lane",
                "addressLine3": "",
                "addressLine4": "",
                "addressLine5": "St Albans",
                "postCode": "AL3 4HE",
                "coordinates": {
                    "latitude": "51.748930",
                    "longitude": "-0.346820",
                },
            },
        },
        "contact": {
            "name": "AL3 4HE",
        },
        "additionalProperties": [
            {
                "name": "surveyName"
                , "value": "DST2101_AA1"
            },
            {
                "name": "tla",
                "value": "DST"
            },
            {
                "name": "wave",
                "value": "1"
            },
            {
                "name": "priority",
                "value": "1"
            },
            {
                "name": "fieldTeam",
                "value": "The A Team"
            },
        ],
    }

    validate_totalmobile_payload(totalmobile_payload)
    assert ('root', logging.WARNING, "Totalmobile payload was sent without the 'origin' field") in caplog.record_tuples


def test_an_error_is_logged_when_both_the_origin_and_duration_fields_are_missing_from_the_totalmobile_payload(caplog):
    totalmobile_payload = {
        "identity": {
            "reference": "DST2101-AA1.100100"
            },
        "description": "Study: DST2101_AA1\nCase ID: 100100",
        "workType": "DST",
        "skills": [
            {
                "identity": {
                    "reference": "DST"
                    }
            }
        ],
        "dueDate": {
            "end": "2020-11-17",
        },
        "location": {
            "addressDetail": {
                "addressLine1": "Ye Olde Fighting Cocks",
                "addressLine2": "16 Abbey Mill Lane",
                "addressLine3": "",
                "addressLine4": "",
                "addressLine5": "St Albans",
                "postCode": "AL3 4HE",
                "coordinates": {
                    "latitude": "51.748930",
                    "longitude": "-0.346820",
                },
            },
        },
        "contact": {
            "name": "AL3 4HE",
        },
        "additionalProperties": [
            {
                "name": "surveyName"
                , "value": "DST2101_AA1"
            },
            {
                "name": "tla",
                "value": "DST"
            },
            {
                "name": "wave",
                "value": "1"
            },
            {
                "name": "priority",
                "value": "1"
            },
            {
                "name": "fieldTeam",
                "value": "The A Team"
            },
        ],
    }

    validate_totalmobile_payload(totalmobile_payload)
    assert ('root', logging.WARNING, "Totalmobile payload was sent without the 'origin' field") in caplog.record_tuples
    assert ('root', logging.WARNING, "Totalmobile payload was sent without the 'duration' field") in caplog.record_tuples


def test_create_job_reference():
    assert create_job_reference("DST2101_AA1", "100100") == "DST2101-AA1.100100"


def test_create_description():
    assert (
            create_description("DST2101_AA1", "100100")
            == """Study: DST2101_AA1
Case ID: 100100"""
            )

def test_an_error_is_logged_when_a_uac_value_is_empty(caplog):
    totalmobile_payload = {
        "additionalProperties": [
            {"name": "study", "value": "DST2101A"},
            {"name": "case_id", "value": "100100"},
            {"name": "uac1", "value": ""},
            {"name": "uac2", "value": ""},
            {"name": "uac3", "value": ""},
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
        "duration": 15,
        "origin": "ONS",
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
        "skills": [{"identity": {"reference": "KTN"}}],
        "workType": "KTN",
    }

    validate_totalmobile_payload(totalmobile_payload)
    assert ('root', logging.WARNING, "Totalmobile payload was sent with an empty 'uac1' field")
    [('root', 30, 'Totalmobile payload was sent with an empty uac1 field'),
     ('root', 30, 'Totalmobile payload was sent with an empty uac2 field'),
     ('root', 30, 'Totalmobile payload was sent with an empty uac3 field')] in caplog.record_tuples
