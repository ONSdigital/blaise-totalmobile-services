import json
import pytest

from unittest import mock

from run import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    app.call_history_client = mock.MagicMock()
    return app.test_client()


@pytest.fixture
def upload_visit_status_request_sample():
    return json.loads("""
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
    """)


@pytest.fixture
def submit_form_result_request_sample():
    return json.loads("""
    {
      "Result": {
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
        "Date": "2022-03-15T11:20:04.25",
        "Form": {
          "Reference": "Interview - Full",
          "Version": 8
        },
        "Association": {
          "WorkType": "SS",
          "Reference": "SLC-12345-678-910",
          "PropertyReference": "1234567 1",
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
                  "Reference": "TEA",
                  "Text": "This is a final call result If you complete this, you will not be able to edit it at a later date.",
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
                "Value": "2022-03-15T11:19:00.000+00:00",
                "Description": null,
                "Element": {
                  "Reference": "InterviewDateTime",
                  "Text": "Date and Time Interviewed:",
                  "EnrichContentSpecified": false
                }
              },
              {
                "Value": "Nothing left ",
                "Description": null,
                "Element": {
                  "Reference": "WhatLeft",
                  "Text": "What did you leave?",
                  "EnrichContentSpecified": false
                }
              },
              {
                "Value": "SLC",
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
        "ResultGuid": "f00-ba7"
      }
    }
    """)


@pytest.fixture
def complete_visit_request_sample():
    return json.loads("""
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
    """)
