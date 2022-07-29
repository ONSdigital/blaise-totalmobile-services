import json
from base64 import b64encode
from calendar import c
from typing import Dict
from unittest import mock

import pytest
from werkzeug.security import generate_password_hash

from app.app import app as flask_app
from client import OptimiseClient


@pytest.fixture
def optimise_client() -> OptimiseClient:
    return OptimiseClient("http://localhost", "Test", "", "")


@pytest.fixture
def mock_auth_response() -> Dict:
    return {"access_token": "foo", "expires_in": 50}


@pytest.fixture
def mock_jobs() -> Dict:
    return {"results": [{}]}


@pytest.fixture
def mock_jobs_multi_page() -> Dict:
    return {
        "results": [{}],
        "paging": {"next": "worlds/test/jobs?pageSize=1000&pageNo=2"},
    }


@pytest.fixture
def mock_create_job_task() -> Dict:
    return {
        "questionnaire": "DST2101_AA1",
        "world_id": "test-world-id",
        "case": {
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
            "qDataBag.UPRN_Latitude": "51.748930",
            "qDataBag.UPRN_Longitude": "-0.346820",
            "qDataBag.Priority": "1",
            "qDataBag.FieldRegion": "",
            "qDataBag.FieldTeam": "The A Team",
            "qDataBag.WaveComDTE": "2020-11-17",
            "uac_chunks": {
                "uac1": "8176",
                "uac2": "4726",
                "uac3": "3993"
            },
        },
    }


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def test_password():
    return "test-password"


@pytest.fixture
def test_username():
    return "test-username"


@pytest.fixture
def client(app, test_username, test_password):
    app.config["user"] = test_username
    app.config["password_hash"] = generate_password_hash(test_password)
    return app.test_client()


@pytest.fixture
def test_auth_header(test_username, test_password):
    credentials = b64encode(f"{test_username}:{test_password}".encode()).decode("utf-8")
    return {"Authorization": f"Basic {credentials}"}


@pytest.fixture
def upload_visit_status_request_sample():
    return json.loads(
        """
    {
        "Lines": [
            -1,
            -2
        ],
        "Identity": {
            "Guid": "f00-ba7",
            "WorkType": "SS",
            "User": {
                "ID": 9999,
                "IDSpecified": true,
                "Name": "jane.doe",
                "DeviceID": "f00-ba7",
                "UserAttributes": [
                    {
                        "Name": "AuthNo",
                        "Value": "1111"
                    },
                    {
                        "Name": "Region",
                        "Value": "South West"
                    },
                    {
                        "Name": "Team",
                        "Value": "South West 7"
                    },
                    {
                        "Name": "Skill",
                        "Value": "Survey"
                    }
                ]
            },
            "Company": "NA",
            "Reference": "SLC-12345-678-910"
        },
        "Date": "2022-03-15T09:57:34.265563+00:00",
        "ProcessReference": "*TELCALL",
        "ReasonCode": null,
        "ReasonDescription": null,
        "Notes": null,
        "FromStatus": "APPOINT",
        "ToStatus": "TELCALL",
        "Actual": null,
        "Action": 0,
        "ActionSpecified": true,
        "Metadata": [

        ]
    }
    """
    )


@pytest.fixture
def submit_form_result_request_sample():
    return json.loads(
        """
    {
      "Result": {
        "User": {
          "ID": 1234,
          "Name": "blah",
          "UserAttributes": [
            {
              "Name": "AuthNo",
              "Value": "1234"
            }
          ]
        },
        "Date": "2022-01-01T10:00:10.00",
        "Form": {
          "Reference": "Interview - Full"
        },
        "Association": {
          "WorkType": "SS",
          "Reference": "DST2111Z-1001011",
          "PropertyReference": "1001011",
          "ClientReference": ""
        },
        "Responses": [
          {
            "Instance": 0,
            "Responses": [
              {
                "Value": "",
                "Description": null,
                "Element": {
                  "Reference": "BLAH",
                  "Text": "blah",
                  "EnrichContentSpecified": false
                }
              }
            ],
            "Element": {
              "Reference": "Warning",
              "Text": "Warning",
              "EnrichContentSpecified": false
            }
          },
          {
            "Instance": 0,
            "Responses": [
              {
                "Value": "2022-01-01T10:10:00.000+00:00",
                "Description": null,
                "Element": {
                  "Reference": "InterviewDateTime",
                  "Text": "Date and Time Interviewed:",
                  "EnrichContentSpecified": false
                }
              },
              {
                "Value": "07000000000",
                "Description": null,
                "Element": {
                  "Reference": "TelNo",
                  "Text": "What is your telephone number?",
                  "EnrichContentSpecified": false
                }
              },
              {
                "Value": "DST",
                "Description": null,
                "Element": {
                  "Reference": "SurveyType",
                  "Text": "Survey Type:",
                  "EnrichContentSpecified": false
                }
              }
            ],
            "Element": {
              "Reference": "SA",
              "Text": "Interview Full",
              "EnrichContentSpecified": false
            }
          }
        ],
        "ResultGuid": "1234-1234-1234-1234"
      }
    }
    """
    )


@pytest.fixture
def complete_visit_request_sample():
    return json.loads(
        """
    {
      "SystemDate": "2022-03-15T11:20:04.307495+00:00",
      "SystemDateSpecified": true,
      "IsFullyComplete": true,
      "Lines": [

      ],
      "Appointment": {
        "Date": "2022-03-15T10:00:00",
        "Slot": "",
        "Schedule": {
          "StartDate": "2022-03-15T10:00:00",
          "EndDate": "2022-03-15T11:00:00"
        },
        "KeptSpecified": false,
        "ReasonCode": null,
        "Narrative": null
      },
      "Tasks": [
        {
          "FormIdentity": {
            "Reference": "First Visit",
            "Version": 0
          },
          "FormResultGuid": "f11-ba8",
          "LineNo": -1,
          "Type": 0,
          "Description": "Property Details",
          "Complete": true,
          "Notes": null,
          "Location": null,
          "Status": 2,
          "AdditionalProperties": [

          ],
          "DependencyGroup": null,
          "DependencyExpression": null,
          "LastUpdatedDateTime": "2022-03-15T11:19:39.426074+00:00",
          "LastUpdatedDateTimeSpecified": true,
          "Title": null
        },
        {
          "FormIdentity": {
            "Reference": "Correct Address",
            "Version": 0
          },
          "FormResultGuid": "f00-ba7",
          "LineNo": -2,
          "Type": 0,
          "Description": "Validate Address",
          "Complete": true,
          "Notes": null,
          "Location": null,
          "Status": 2,
          "AdditionalProperties": [

          ],
          "DependencyGroup": null,
          "DependencyExpression": null,
          "LastUpdatedDateTime": "2022-03-15T11:19:46.632285+00:00",
          "LastUpdatedDateTimeSpecified": true,
          "Title": null
        }
      ],
      "Identity": {
        "Guid": "f00-ba7",
        "WorkType": "SS",
        "User": {
          "ID": 9999,
          "IDSpecified": true,
          "Name": "jane.doe",
          "DeviceID": "f00-ba7",
          "UserAttributes": [
            {
              "Name": "AuthNo",
              "Value": "1111"
            },
            {
              "Name": "Region",
              "Value": "South West"
            },
            {
              "Name": "Skill",
              "Value": "Survey"
            },
            {
              "Name": "Team",
              "Value": "South West 7"
            }
          ]
        },
        "Company": "NA",
        "Reference": "SLC-12345-678-910"
      },
      "Date": "2022-03-15T11:20:04.307495+00:00",
      "ProcessReference": "TELINTFULL",
      "ReasonCode": null,
      "ReasonDescription": null,
      "Notes": null,
      "FromStatus": "TELCALL",
      "ToStatus": "INTERVIEWF",
      "Actual": null,
      "Action": 4,
      "ActionSpecified": true,
      "Metadata": [

      ]
    }
    """
    )


@pytest.fixture
def mock_worlds(mock_world):
    return [mock_world]


@pytest.fixture
def mock_world():
    return {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "identity": {"reference": "test"},
        "type": "foo",
    }


@pytest.fixture
def mock_questionnaires_from_blaise():
    return [
        {
            "name": "LMS2101_AA1",
            "id": "05cf69af-3a4e-47df-819a-928350fdda5a",
            "serverParkName": "gusty",
            "installDate": "2022-07-01T09:46:24.7460966+01:00",
            "status": "Inactive",
            "dataRecordCount": 0,
            "hasData": False,
            "nodes": [
                {
                    "nodeName": "blaise-gusty-mgmt",
                    "nodeStatus": "Inactive"
                }
            ]
        },
        {
            "name": "DST2108W",
            "id": "1336fd28-22f0-421e-ab0f-cd7b050e8ccf",
            "serverParkName": "gusty",
            "installDate": "2022-04-25T14:57:23.262323+01:00",
            "status": "Active",
            "dataRecordCount": 0,
            "hasData": False,
            "nodes": [
                {
                    "nodeName": "blaise-gusty-mgmt",
                    "nodeStatus": "Active"
                }
            ]
        },
        {
            "name": "LMS2111Z",
            "id": "2052300a-39be-4dfb-99b5-a2eb0d47e141",
            "serverParkName": "gusty",
            "installDate": "2022-06-22T12:47:50.3668548+01:00",
            "status": "Active",
            "dataRecordCount": 50,
            "hasData": False,
            "nodes": [
                {
                    "nodeName": "blaise-gusty-mgmt",
                    "nodeStatus": "Active"
                }
            ]
        },
        {
            "name": "OPN2203H",
            "id": "ae4e2b84-1187-48f4-bfef-3f4b2d5ec629",
            "serverParkName": "gusty",
            "installDate": "2022-06-22T12:45:26.2286747+01:00",
            "status": "Active",
            "dataRecordCount": 0,
            "hasData": False,
            "nodes": [
                {
                    "nodeName": "blaise-gusty-mgmt",
                    "nodeStatus": "Active"
                }
            ]
        },
        {
            "name": "NWO2204a",
            "id": "cd4095cf-ffa4-47db-97f2-96cf1cc992b3",
            "serverParkName": "gusty",
            "installDate": "2022-04-27T15:24:01.316053+01:00",
            "status": "Active",
            "dataRecordCount": 0,
            "hasData": False,
            "nodes": [
                {
                    "nodeName": "blaise-gusty-mgmt",
                    "nodeStatus": "Active"
                }
            ]
        }
    ]


@pytest.fixture
def mock_lms_only_questionnaire_from_blaise():
    return [
        {
            "name": "LMS2101_AA1",
            "id": "05cf69af-3a4e-47df-819a-928350fdda5a",
            "serverParkName": "gusty",
            "installDate": "2022-07-01T09:46:24.7460966+01:00",
            "status": "Inactive",
            "dataRecordCount": 0,
            "hasData": False,
            "nodes": [
                {
                    "nodeName": "blaise-gusty-mgmt",
                    "nodeStatus": "Inactive"
                }
            ]
        }
    ]


@pytest.fixture
def mock_dst_only_questionnaire_from_blaise():
    return [
        {
            "name": "DST2101_AA1",
            "id": "05cf69af-3a4e-47df-819a-928350fdda5a",
            "serverParkName": "gusty",
            "installDate": "2022-07-01T09:46:24.7460966+01:00",
            "status": "Inactive",
            "dataRecordCount": 0,
            "hasData": False,
            "nodes": [
                {
                    "nodeName": "blaise-gusty-mgmt",
                    "nodeStatus": "Inactive"
                }
            ]
        }
    ]
