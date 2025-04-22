import json
from base64 import b64encode
from typing import Dict

import pytest
from werkzeug.security import generate_password_hash

from app.app import setup_app
from client import OptimiseClient


@pytest.fixture
def optimise_client() -> OptimiseClient:
    return OptimiseClient(
        "http://localhost", "Test", "optimise_client_id", "optimise_client_secret"
    )


@pytest.fixture
def mock_auth_response() -> Dict:
    return {"access_token": "foo", "expires_in": 50}


@pytest.fixture
def mock_jobs() -> Dict:
    return {
        "results": [
            {
                "status": "NEW",
                "visitStatus": None,
                "visitComplete": True,
                "committed": False,
                "dispatched": False,
                "dispatchDate": None,
                "pendingRelations": False,
                "schedules": [],
                "jobRelations": [],
                "project": None,
                "identity": {"reference": "LMS2208-EJ1.1"},
                "jobPendingRelations": [],
                "allocatedResource": None,
                "mandatoryResource": None,
                "description": "UAC: \nDue Date: 03/10/2023\nStudy: LMS2208_EJ1\nCase ID: 1",
                "contact": {
                    "title": None,
                    "name": "NP12 4AB",
                    "homePhone": None,
                    "workPhone": None,
                    "mobilePhone": None,
                    "email": None,
                    "url": None,
                    "contactDetail": {
                        "preferredName": None,
                        "contactId": None,
                        "contactIdLabel": None,
                        "dateOfBirth": None,
                        "dateOfDeath": None,
                        "gender": None,
                    },
                },
                "duration": 15,
                "priority": None,
                "bandingGroup": None,
                "emergency": False,
                "specialInstructions": None,
                "clientReference": None,
                "location": {
                    "address": "1 Elm Street, Oak Lane, Springsville, Newport, NP12 4AB",
                    "reference": None,
                    "addressDetail": {
                        "name": None,
                        "houseNumber": None,
                        "addressLine1": "1 Elm Street",
                        "addressLine2": "Oak Lane",
                        "addressLine3": "Springsville",
                        "addressLine4": "Gwent",
                        "addressLine5": "Newport",
                        "postCode": "NP12 4AB",
                        "coordinates": {"latitude": 51.68279, "longitude": -3.18221},
                    },
                },
                "workType": "LMS",
                "value": 0,
                "scheduleDate": {"start": None, "end": None},
                "appointmentDate": {"start": None, "end": None},
                "dueDate": {"start": None, "end": None},
                "origin": "ONS",
                "catalogueReference": None,
                "groupReference": None,
                "skills": [],
                "attributes": [],
                "tasks": [],
                "appointmentPattern": None,
                "preferredResources": [],
                "prohibitedResources": [],
                "additionalProperties": [],
                "_links": [
                    {
                        "rel": "self",
                        "href": "/Test/api/optimise/worlds/7e4beb99-ed79-4179-ab39-ab6600ebd65e/jobs/LMS2208-EJ1.1",
                    }
                ],
            },
            {
                "status": "NEW",
                "visitStatus": None,
                "visitComplete": False,
                "committed": False,
                "dispatched": False,
                "dispatchDate": None,
                "pendingRelations": False,
                "schedules": [],
                "jobRelations": [],
                "project": None,
                "identity": {"reference": "LMS2208-EJ1.10"},
                "jobPendingRelations": [],
                "allocatedResource": None,
                "mandatoryResource": None,
                "description": "UAC: \nDue Date: 03/10/2023\nStudy: LMS2208_EJ1\nCase ID: 10",
                "contact": {
                    "title": None,
                    "name": "NP12 4AB",
                    "homePhone": None,
                    "workPhone": None,
                    "mobilePhone": None,
                    "email": None,
                    "url": None,
                    "contactDetail": {
                        "preferredName": None,
                        "contactId": None,
                        "contactIdLabel": None,
                        "dateOfBirth": None,
                        "dateOfDeath": None,
                        "gender": None,
                    },
                },
                "duration": 15,
                "priority": None,
                "bandingGroup": None,
                "emergency": False,
                "specialInstructions": None,
                "clientReference": None,
                "location": {
                    "address": "1 Elm Street, Oak Lane, Springsville, Newport, NP12 4AB",
                    "reference": None,
                    "addressDetail": {
                        "name": None,
                        "houseNumber": None,
                        "addressLine1": "1 Elm Street",
                        "addressLine2": "Oak Lane",
                        "addressLine3": "Springsville",
                        "addressLine4": "Gwent",
                        "addressLine5": "Newport",
                        "postCode": "NP12 4AB",
                        "coordinates": {"latitude": 51.68279, "longitude": -3.18221},
                    },
                },
                "workType": "LMS",
                "value": 0,
                "scheduleDate": {"start": None, "end": None},
                "appointmentDate": {"start": None, "end": None},
                "dueDate": {"start": None, "end": "2023-10-03T00:00:00"},
                "origin": "ONS",
                "catalogueReference": None,
                "groupReference": None,
                "skills": [],
                "attributes": [],
                "tasks": [],
                "appointmentPattern": None,
                "preferredResources": [],
                "prohibitedResources": [],
                "additionalProperties": [],
                "_links": [
                    {
                        "rel": "self",
                        "href": "/Test/api/optimise/worlds/7e4beb99-ed79-4179-ab39-ab6600ebd65e/jobs/LMS2208-EJ1.10",
                    }
                ],
            },
        ],
        "paging": {
            "pageNo": 0,
            "pageSize": 100,
            "pageCount": 1,
            "totalCount": 95,
            "previous": None,
            "next": None,
        },
        "criteria": {"filter": None, "order": None, "include": None},
    }


@pytest.fixture
def mock_empty_jobs() -> Dict:
    return {"results": [{}]}


@pytest.fixture
def mock_empty_jobs_multi_page() -> Dict:
    return {
        "results": [{}],
        "paging": {"next": "worlds/test/jobs?pageSize=1000&pageNo=2"},
    }


@pytest.fixture
def mock_create_job_task() -> Dict:
    return {
        "questionnaire": "DST2101_AA1",
        "world_id": "test-world-id",
        "case_id": "100100",
        "payload": {},
    }


@pytest.fixture
def app():
    return setup_app()


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
      "result": {
        "user": {
          "ID": 1234,
          "name": "blah",
          "userattributes": [
            {
              "name": "AuthNo",
              "value": "1234"
            }
          ]
        },
        "date": "2022-01-01T10:00:10.00",
        "form": {
          "reference": "Interview - Full"
        },
        "association": {
          "worktype": "SS",
          "reference": "FRS2504A.1001",
          "propertyreference": "1001",
          "clientreference": ""
        },
        "responses": [
          {
            "instance": 0,
            "responses": [
              {
                "value": "",
                "description": null,
                "element": {
                  "reference": "BLAH",
                  "text": "blah",
                  "enrichContentspecified": false
                }
              }
            ],
            "element": {
              "reference": "Warning",
              "text": "Warning",
              "enrichContentSpecified": false
            }
          },
          {
            "instance": 0,
            "responses": [
              {
                "value": "2022-01-01T10:10:00.000+00:00",
                "description": null,
                "element": {
                  "reference": "InterviewDateTime",
                  "text": "Date and Time Interviewed:",
                  "enrichcontentspecified": false
                }
              },
              {
                "value": "410",
                "description": null,
                "element": {
                  "reference": "Primary_Outcome",
                  "text": "410",
                  "enrichcontentspecified": false
                }
              },
              {
                "value": "DST",
                "description": null,
                "element": {
                  "reference": "SurveyType",
                  "text": "Survey Type:",
                  "enrichcontentspecified": false
                }
              }
            ],
            "element": {
              "reference": "SA",
              "text": "Interview Full",
              "enrichContentspecified": false
            }
          }
        ],
        "resultguid": "1234-1234-1234-1234"
      }
    }
    """
    )


@pytest.fixture
def create_visit_request_sample():
    return json.loads(
        """
    {
    "visit": {
        "identity": {
            "Guid": "3fe4dc64-d07c-ef11-9c38-7c1e52036bea",
            "WorkType": "FRS",
            "user": {
                "ID": 1239,
                "IDSpecified": true,
                "name": "Interviewer1",
                "DeviceID": null,
                "UserAttributes": [
                    {
                        "Name": "BlaiseLogin",
                        "Value": "cal"
                    },
                    {
                        "Name": "Region",
                        "Value": "Wales"
                    },
                    {
                        "Name": "Region",
                        "Value": "South East"
                    },
                    {
                        "Name": "Skill",
                        "Value": "FRS"
                    }
                ]
            },
            "Company": "NA",
            "reference": "FRS2405A.500101"
        },
        "ClientReference": null,
        "Description": "blah",
        "property": {
            "Guid": null,
            "Type": "JM_PROPERTY",
            "Reference": null,
            "ParentReference": null,
            "Name": null,
            "Title": null,
            "address": {
                "Name": null,
                "lines": [
                    "prem1",
                    "prem2",
                    "prem3",
                    "district",
                    "posttown"
                ],
                "HouseNo": null,
                "postcode": "postcode",
                "GeoX": 51.566,
                "GeoXSpecified": true,
                "GeoY": -3.026,
                "GeoYSpecified": true,
                "URL": null
            },
            "Phone": null,
            "WorkPhone": null,
            "MobilePhone": null,
            "Email": null,
            "URL": null,
            "Assets": [],
            "ExtendedProperties": {
                "PreferredName": null,
                "ID": null,
                "IDLabel": null,
                "DateOfBirthSpecified": false,
                "DateOfDeathSpecified": false,
                "Gender": null
            }
        },
        "Supervisor": null,
        "Status": "NEW",
        "StatusChangeDateSpecified": false,
        "CreatedDate": "2024-09-27T13:59:56.8872461+01:00",
        "CreatedDateSpecified": true,
        "RetrievedSpecified": false,
        "RetrievedDateSpecified": false,
        "PrintedDateSpecified": false,
        "ReceivedDateSpecified": false,
        "ResponseDateSpecified": false,
        "RequiredDate": "2025-01-01T00:00:00",
        "RequiredDateSpecified": true,
        "CompleteSpecified": false,
        "CompletedDateSpecified": false,
        "Appointment": null,
        "Schedule": {
            "StartDate": "2024-09-27T00:20:00",
            "EndDate": "2024-09-27T00:35:00"
        },
        "Priority": null,
        "Origin": "ResManager",
        "SpecialInstructions": null,
        "AdditionalProperties": [
            {
                "Name": "tla",
                "Value": "FRS",
                "AdditionalProperties": []
            },
            {
                "Name": "rand",
                "Value": "1",
                "AdditionalProperties": []
            },
            {
                "Name": "fieldRegion",
                "Value": "Region 1",
                "AdditionalProperties": []
            },
            {
                "Name": "fieldTeam",
                "Value": "fieldteam",
                "AdditionalProperties": []
            },
            {
                "Name": "postCode",
                "Value": "postcode",
                "AdditionalProperties": []
            },
            {
                "Name": "HasMultiResourceRelatedJobs",
                "Value": "False",
                "AdditionalProperties": []
            }
        ],
        "CatalogueReference": null,
        "Lines": [],
        "Tasks": [],
        "HasPendingTasks": false,
        "Actual": null,
        "Duration": 15,
        "DurationSpecified": true
      }
    }  
    """
    )


@pytest.fixture
def create_visit_request_sample_without_user_blaise_logins():
    return json.loads(
        """
    {
    "visit": {
        "identity": {
            "Guid": "3fe4dc64-d07c-ef11-9c38-7c1e52036bea",
            "WorkType": "FRS",
            "user": {
                "id": null,
                "IDSpecified": true,
                "name": null,
                "DeviceID": null
            },
            "Company": "NA",
            "reference": "IPS2409A.500101"
        },
        "ClientReference": null,
        "Description": "blah",
        "Property": {
            "Guid": null,
            "Type": "JM_PROPERTY",
            "Reference": null,
            "ParentReference": null,
            "Name": null,
            "Title": null,
            "Address": {
                "Name": null,
                "Lines": [
                    "prem1",
                    "prem2",
                    "prem3",
                    "district",
                    "posttown"
                ],
                "HouseNo": null,
                "PostCode": "postcode",
                "GeoX": 51.566,
                "GeoXSpecified": true,
                "GeoY": -3.026,
                "GeoYSpecified": true,
                "URL": null
            },
            "Phone": null,
            "WorkPhone": null,
            "MobilePhone": null,
            "Email": null,
            "URL": null,
            "Assets": [],
            "ExtendedProperties": {
                "PreferredName": null,
                "ID": null,
                "IDLabel": null,
                "DateOfBirthSpecified": false,
                "DateOfDeathSpecified": false,
                "Gender": null
            }
        },
        "Supervisor": null,
        "Status": "NEW",
        "StatusChangeDateSpecified": false,
        "CreatedDate": "2024-09-27T13:59:56.8872461+01:00",
        "CreatedDateSpecified": true,
        "RetrievedSpecified": false,
        "RetrievedDateSpecified": false,
        "PrintedDateSpecified": false,
        "ReceivedDateSpecified": false,
        "ResponseDateSpecified": false,
        "RequiredDate": "2025-01-01T00:00:00",
        "RequiredDateSpecified": true,
        "CompleteSpecified": false,
        "CompletedDateSpecified": false,
        "Appointment": null,
        "Schedule": {
            "StartDate": "2024-09-27T00:20:00",
            "EndDate": "2024-09-27T00:35:00"
        },
        "Priority": null,
        "Origin": "ResManager",
        "SpecialInstructions": null,
        "AdditionalProperties": [
            {
                "Name": "tla",
                "Value": "FRS",
                "AdditionalProperties": []
            },
            {
                "Name": "rand",
                "Value": "1",
                "AdditionalProperties": []
            },
            {
                "Name": "fieldRegion",
                "Value": "Region 1",
                "AdditionalProperties": []
            },
            {
                "Name": "fieldTeam",
                "Value": "fieldteam",
                "AdditionalProperties": []
            },
            {
                "Name": "postCode",
                "Value": "postcode",
                "AdditionalProperties": []
            },
            {
                "Name": "HasMultiResourceRelatedJobs",
                "Value": "False",
                "AdditionalProperties": []
            }
        ],
        "CatalogueReference": null,
        "Lines": [],
        "Tasks": [],
        "HasPendingTasks": false,
        "Actual": null,
        "Duration": 15,
        "DurationSpecified": true
      }
    }  
    """
    )


@pytest.fixture
def create_visit_request_sample_without_reference():
    return json.loads(
        """
    {
    "visit": {
        "identity": {
            "Guid": "3fe4dc64-d07c-ef11-9c38-7c1e52036bea",
            "WorkType": "FRS",
            "user": {
                "id": null,
                "IDSpecified": true,
                "Name": "Callum.Nicholson",
                "DeviceID": null
            },
            "Company": "NA"
        },
        "ClientReference": null,
        "Description": "blah",
        "Property": {
            "Guid": null,
            "Type": "JM_PROPERTY",
            "Reference": null,
            "ParentReference": null,
            "Name": null,
            "Title": null,
            "Address": {
                "Name": null,
                "Lines": [
                    "prem1",
                    "prem2",
                    "prem3",
                    "district",
                    "posttown"
                ],
                "HouseNo": null,
                "PostCode": "postcode",
                "GeoX": 51.566,
                "GeoXSpecified": true,
                "GeoY": -3.026,
                "GeoYSpecified": true,
                "URL": null
            },
            "Phone": null,
            "WorkPhone": null,
            "MobilePhone": null,
            "Email": null,
            "URL": null,
            "Assets": [],
            "ExtendedProperties": {
                "PreferredName": null,
                "ID": null,
                "IDLabel": null,
                "DateOfBirthSpecified": false,
                "DateOfDeathSpecified": false,
                "Gender": null
            }
        },
        "Supervisor": null,
        "Status": "NEW",
        "StatusChangeDateSpecified": false,
        "CreatedDate": "2024-09-27T13:59:56.8872461+01:00",
        "CreatedDateSpecified": true,
        "RetrievedSpecified": false,
        "RetrievedDateSpecified": false,
        "PrintedDateSpecified": false,
        "ReceivedDateSpecified": false,
        "ResponseDateSpecified": false,
        "RequiredDate": "2025-01-01T00:00:00",
        "RequiredDateSpecified": true,
        "CompleteSpecified": false,
        "CompletedDateSpecified": false,
        "Appointment": null,
        "Schedule": {
            "StartDate": "2024-09-27T00:20:00",
            "EndDate": "2024-09-27T00:35:00"
        },
        "Priority": null,
        "Origin": "ResManager",
        "SpecialInstructions": null,
        "AdditionalProperties": [
            {
                "Name": "tla",
                "Value": "FRS",
                "AdditionalProperties": []
            },
            {
                "Name": "rand",
                "Value": "1",
                "AdditionalProperties": []
            },
            {
                "Name": "fieldRegion",
                "Value": "Region 1",
                "AdditionalProperties": []
            },
            {
                "Name": "fieldTeam",
                "Value": "fieldteam",
                "AdditionalProperties": []
            },
            {
                "Name": "postCode",
                "Value": "postcode",
                "AdditionalProperties": []
            },
            {
                "Name": "HasMultiResourceRelatedJobs",
                "Value": "False",
                "AdditionalProperties": []
            }
        ],
        "CatalogueReference": null,
        "Lines": [],
        "Tasks": [],
        "HasPendingTasks": false,
        "Actual": null,
        "Duration": 15,
        "DurationSpecified": true
      }
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
            "nodes": [{"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Inactive"}],
        },
        {
            "name": "DST2108W",
            "id": "1336fd28-22f0-421e-ab0f-cd7b050e8ccf",
            "serverParkName": "gusty",
            "installDate": "2022-04-25T14:57:23.262323+01:00",
            "status": "Active",
            "dataRecordCount": 0,
            "hasData": False,
            "nodes": [{"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Active"}],
        },
        {
            "name": "LMS2111Z",
            "id": "2052300a-39be-4dfb-99b5-a2eb0d47e141",
            "serverParkName": "gusty",
            "installDate": "2022-06-22T12:47:50.3668548+01:00",
            "status": "Active",
            "dataRecordCount": 50,
            "hasData": False,
            "nodes": [{"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Active"}],
        },
        {
            "name": "OPN2203H",
            "id": "ae4e2b84-1187-48f4-bfef-3f4b2d5ec629",
            "serverParkName": "gusty",
            "installDate": "2022-06-22T12:45:26.2286747+01:00",
            "status": "Active",
            "dataRecordCount": 0,
            "hasData": False,
            "nodes": [{"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Active"}],
        },
        {
            "name": "NWO2204a",
            "id": "cd4095cf-ffa4-47db-97f2-96cf1cc992b3",
            "serverParkName": "gusty",
            "installDate": "2022-04-27T15:24:01.316053+01:00",
            "status": "Active",
            "dataRecordCount": 0,
            "hasData": False,
            "nodes": [{"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Active"}],
        },
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
            "nodes": [{"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Inactive"}],
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
            "nodes": [{"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Inactive"}],
        }
    ]


@pytest.fixture
def mock_frs_questionnaire_from_blaise():
    return {
        "name": "FRS2405A",
        "id": "a0e2f264-14e4-4151-b12d-bb3331674624",
        "serverParkName": "gusty",
        "installDate": "2024-10-01T09:46:24.7460966+01:00",
        "status": "Inactive",
        "dataRecordCount": 0,
        "hasData": False,
        "nodes": [{"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Inactive"}],
    }


@pytest.fixture
def mock_frs_allocated_case_from_cma_launcher():
    return {
        "primaryKeyValues": {
            "mainSurveyID": "a0e2f264-14e4-4151-b12d-bb3331674624",
            "id": "500101",
        },
        "fieldData": {
            "mainSurveyID": "a0e2f264-14e4-4151-b12d-bb3331674624",
            "surveyDisplayName": "FRS2405A",
            "id": "100100",
            "cmA_Supervisor": "",
            "cmA_ForWhom": "User1",
            "cmA_InPossession": "User1",
            "cmA_Location": "CLIENT",
            "cmA_Status": "",
            "cmA_CaseClosed": "",
            "cmA_HappeningsStr": "",
            "cmA_HappeningsLbl": "",
            "cmA_HappeningsCod": "",
            "cmA_AllowSpawning": "",
            "cmA_IsDonorCase": "",
            "cmA_GroupType": "",
            "cmA_GroupID": "a0e2f264-14e4-4151-b12d-bb3331674624Case1",
            "cmA_GroupSort": "",
            "cmA_GroupStatus": "",
            "cmA_GroupSummary": "",
            "cmA_SpawnCount": "",
            "cmA_StartDate": "",
            "cmA_EndDate": "11-11-2024",
            "cmA_CmdLineForEdit": "",
            "cmA_PreLoadForEdit": "",
            "cmA_Process.CreatedDT": "",
            "cmA_Process.LastChangedDT": "",
            "cmA_Process.GeoLocation": "",
            "cmA_Process.FirstDownloaded.When": "20241007 09:58:40",
            "cmA_Process.FirstDownloaded.User": "User1",
            "cmA_Process.FirstUploaded.When": "",
            "cmA_Process.FirstUploaded.User": "",
            "cmA_Process.LastDownloaded.When": "20241007 09:58:40",
            "cmA_Process.LastDownloaded.User": "User1",
            "cmA_Process.LastUploaded.When": "",
            "cmA_Process.LastUploaded.User": "",
            "cmA_Process.LastAttempt.When": "",
            "cmA_Process.LastAttempt.User": "",
            "cmA_Process.FirstInterviewTime.When": "",
            "cmA_Process.FirstInterviewTime.User": "",
            "cmA_Process.LastInterviewTime.When": "",
            "cmA_Process.LastInterviewTime.User": "",
            "cmA_Process.LastInterviewEndTime": "",
            "cmA_Process.TotalInterviewTimeUsed": "",
            "cmA_Appointment.AppDate": "",
            "cmA_Appointment.AppTime": "",
            "cmA_Appointment.WhenMade.When": "",
            "cmA_Appointment.WhenMade.User": "",
            "cmA_TimeZone": "",
            "cmA_Data.SurveyUploadFailed": "",
            "cmA_Data.Survey": "",
            "cmA_Data.AttemptsCount": "",
            "cmA_Data.Attempts": "",
            "cmA_AttemptsRoute": "",
            "cmA_AttemptsGUID": "",
            "cmA_ContactImage": "",
            "cmA_GeoLocation": "",
            "cmA_ContactInfoGUID": "",
            "cmA_ContactData": "",
            "cmA_DetailsTemplate": "",
            "cmA_CustomUse": "",
            "contactInfoShort": "",
            "lastChangedCI.When": "",
            "lastChangedCI.User": "",
            "caseNote": "",
            "lastChangedNote.When": "",
            "lastChangedNote.User": "",
        },
    }


@pytest.fixture
def mock_frs_case_already_set_to_default_from_cma_launcher():
    return {
        "primaryKeyValues": {
            "mainSurveyID": "a0e2f264-14e4-4151-b12d-bb3331674624",
            "id": "500101",
        },
        "fieldData": {
            "mainSurveyID": "a0e2f264-14e4-4151-b12d-bb3331674624",
            "surveyDisplayName": "FRS2405A",
            "id": "500101",
            "cmA_Supervisor": "",
            "cmA_ForWhom": "",
            "cmA_InPossession": "",
            "cmA_Location": "SERVER",
            "cmA_Status": "",
            "cmA_CaseClosed": "",
            "cmA_HappeningsStr": "",
            "cmA_HappeningsLbl": "",
            "cmA_HappeningsCod": "",
            "cmA_AllowSpawning": "",
            "cmA_IsDonorCase": "",
            "cmA_GroupType": "",
            "cmA_GroupID": "a0e2f264-14e4-4151-b12d-bb3331674624Case1",
            "cmA_GroupSort": "",
            "cmA_GroupStatus": "",
            "cmA_GroupSummary": "",
            "cmA_SpawnCount": "",
            "cmA_StartDate": "",
            "cmA_EndDate": "11-11-2024",
            "cmA_CmdLineForEdit": "",
            "cmA_PreLoadForEdit": "",
            "cmA_Process.CreatedDT": "",
            "cmA_Process.LastChangedDT": "",
            "cmA_Process.GeoLocation": "",
            "cmA_Process.FirstDownloaded.When": "20241007 09:58:40",
            "cmA_Process.FirstDownloaded.User": "User1",
            "cmA_Process.FirstUploaded.When": "",
            "cmA_Process.FirstUploaded.User": "",
            "cmA_Process.LastDownloaded.When": "20241007 09:58:40",
            "cmA_Process.LastDownloaded.User": "User1",
            "cmA_Process.LastUploaded.When": "",
            "cmA_Process.LastUploaded.User": "",
            "cmA_Process.LastAttempt.When": "",
            "cmA_Process.LastAttempt.User": "",
            "cmA_Process.FirstInterviewTime.When": "",
            "cmA_Process.FirstInterviewTime.User": "",
            "cmA_Process.LastInterviewTime.When": "",
            "cmA_Process.LastInterviewTime.User": "",
            "cmA_Process.LastInterviewEndTime": "",
            "cmA_Process.TotalInterviewTimeUsed": "",
            "cmA_Appointment.AppDate": "",
            "cmA_Appointment.AppTime": "",
            "cmA_Appointment.WhenMade.When": "",
            "cmA_Appointment.WhenMade.User": "",
            "cmA_TimeZone": "",
            "cmA_Data.SurveyUploadFailed": "",
            "cmA_Data.Survey": "",
            "cmA_Data.AttemptsCount": "",
            "cmA_Data.Attempts": "",
            "cmA_AttemptsRoute": "",
            "cmA_AttemptsGUID": "",
            "cmA_ContactImage": "",
            "cmA_GeoLocation": "",
            "cmA_ContactInfoGUID": "",
            "cmA_ContactData": "",
            "cmA_DetailsTemplate": "",
            "cmA_CustomUse": "",
            "contactInfoShort": "",
            "lastChangedCI.When": "",
            "lastChangedCI.User": "",
            "caseNote": "",
            "lastChangedNote.When": "",
            "lastChangedNote.User": "",
        },
    }


@pytest.fixture
def mock_frs_unallocated_case_reset_to_defaults_from_cma_launcher():
    return {
        "primaryKeyValues": {
            "mainSurveyID": "a0e2f264-14e4-4151-b12d-bb3331674624",
            "id": "100100",
        },
        "fieldData": {
            "mainSurveyID": "a0e2f264-14e4-4151-b12d-bb3331674624",
            "surveyDisplayName": "FRS2405A",
            "id": "100100",
            "cmA_Supervisor": "",
            "cmA_ForWhom": "",
            "cmA_InPossession": "",
            "cmA_Location": "SERVER",
            "cmA_Status": "",
            "cmA_CaseClosed": "",
            "cmA_HappeningsStr": "",
            "cmA_HappeningsLbl": "",
            "cmA_HappeningsCod": "",
            "cmA_AllowSpawning": "",
            "cmA_IsDonorCase": "",
            "cmA_GroupType": "",
            "cmA_GroupID": "a0e2f264-14e4-4151-b12d-bb3331674624Case1",
            "cmA_GroupSort": "",
            "cmA_GroupStatus": "",
            "cmA_GroupSummary": "",
            "cmA_SpawnCount": "",
            "cmA_StartDate": "",
            "cmA_EndDate": "11-11-2024",
            "cmA_CmdLineForEdit": "",
            "cmA_PreLoadForEdit": "",
            "cmA_Process.CreatedDT": "",
            "cmA_Process.LastChangedDT": "",
            "cmA_Process.GeoLocation": "",
            "cmA_Process.FirstDownloaded.When": "20241007 09:58:40",
            "cmA_Process.FirstDownloaded.User": "User1",
            "cmA_Process.FirstUploaded.When": "",
            "cmA_Process.FirstUploaded.User": "",
            "cmA_Process.LastDownloaded.When": "20241007 09:58:40",
            "cmA_Process.LastDownloaded.User": "User1",
            "cmA_Process.LastUploaded.When": "",
            "cmA_Process.LastUploaded.User": "",
            "cmA_Process.LastAttempt.When": "",
            "cmA_Process.LastAttempt.User": "",
            "cmA_Process.FirstInterviewTime.When": "",
            "cmA_Process.FirstInterviewTime.User": "",
            "cmA_Process.LastInterviewTime.When": "",
            "cmA_Process.LastInterviewTime.User": "",
            "cmA_Process.LastInterviewEndTime": "",
            "cmA_Process.TotalInterviewTimeUsed": "",
            "cmA_Appointment.AppDate": "",
            "cmA_Appointment.AppTime": "",
            "cmA_Appointment.WhenMade.When": "",
            "cmA_Appointment.WhenMade.User": "",
            "cmA_TimeZone": "",
            "cmA_Data.SurveyUploadFailed": "",
            "cmA_Data.Survey": "",
            "cmA_Data.AttemptsCount": "",
            "cmA_Data.Attempts": "",
            "cmA_AttemptsRoute": "",
            "cmA_AttemptsGUID": "",
            "cmA_ContactImage": "",
            "cmA_GeoLocation": "",
            "cmA_ContactInfoGUID": "",
            "cmA_ContactData": "",
            "cmA_DetailsTemplate": "",
            "cmA_CustomUse": "",
            "contactInfoShort": "",
            "lastChangedCI.When": "",
            "lastChangedCI.User": "",
            "caseNote": "",
            "lastChangedNote.When": "",
            "lastChangedNote.User": "",
        },
    }


@pytest.fixture
def force_recall_visit_request_payload():
    return json.loads(
        """
    {
    "reason": null,
    "identity": {
        "guid": null,
        "workType": "FRS",
        "user": {
            "IDSpecified": false,
            "name": "Interviewer1",
            "DeviceID": null,
            "userAttributes": []
        },
        "Company": "NA",
        "reference": "FRS2405A.9002"
    },
    "PreserveIfNoLinesRemainingSpecified": false,
    "lines": ["prem1", "prem2", "prem3", "district", "posttown"],
    "UseSilentPushSpecified": false
    }
    """
    )


@pytest.fixture
def force_recall_visit_request_payload_with_null_reference():
    return json.loads(
        """
    {
    "reason": null,
    "identity": {
        "guid": null,
        "workType": "FRS",
        "user": {
            "IDSpecified": false,
            "name": "Callum.Nicholson",
            "DeviceID": null,
            "userAttributes": []
        },
        "Company": "NA",
        "reference": null
    },
    "PreserveIfNoLinesRemainingSpecified": false,
    "Lines": [],
    "UseSilentPushSpecified": false
    }
    """
    )


@pytest.fixture
def force_recall_visit_request_payload_without_reference():
    return json.loads(
        """
    {
    "reason": null,
    "identity": {
        "guid": null,
        "workType": "FRS",
        "user": {
            "IDSpecified": false,
            "name": "Callum.Nicholson",
            "DeviceID": null,
            "userAttributes": []
        },
        "Company": "NA"
    },
    "PreserveIfNoLinesRemainingSpecified": false,
    "Lines": [],
    "UseSilentPushSpecified": false
    }
    """
    )
