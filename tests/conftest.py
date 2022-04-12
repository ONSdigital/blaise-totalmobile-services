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
        "instrument": "DST2101A",
        "world_id": "test-world-id",
        "case": {
            "qiD.Serial_Number": "100100",
            "qDataBag.Prem1": "prem1",
            "qDataBag.Prem2": "prem2",
            "qDataBag.Prem3": "prem3",
            "qDataBag.PostTown": "PostTown",
            "qDataBag.PostCode": "PostCode",
            "qDataBag.UPRN_Latitude": "UPRN_Latitude",
            "qDataBag.UPRN_Longitude": "UPRN_Longitude",
            "qDataBag.TelNo": "TelNo",
            "qDataBag.TelNo2": "TelNo2",
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
