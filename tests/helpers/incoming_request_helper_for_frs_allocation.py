def get_frs_case_allocation_request():
    return {
        "visit": {
        "identity": {
            "guid": "3ec86664-396c-ef11-9c35-6045bdd094a7",
            "WorkType": "FRS",
            "user": {
                "ID": 365,
                "IDSpecified": True,
                "name": "Test.INT.Wales1.01",
                "DeviceID": None,
                "userAttributes": [
                    {
                        "Name": "AuthNo",
                        "Value": "INT.Wales1.01"
                    },
                    {
                        "Name": "BlaiseLogin",
                        "Value": "test"
                    },
                    {
                        "Name": "Region",
                        "Value": "Wales"
                    },
                    {
                        "Name": "Region",
                        "Value": "North West"
                    },
                    {
                        "Name": "Skill",
                        "Value": "LMS"
                    },
                    {
                        "Name": "Team",
                        "Value": "North West 1"
                    },
                    {
                        "Name": "Team",
                        "Value": "Wales 1"
                    }
                ]
            },
            "Company": "NA",
            "reference": "FRS2405A.800001"
        },
        "ClientReference": None,
        "Description": "UAC 3600 1234 1200 Due date 30/12/2023 Study LMS2311_PT1 Case ID11000000",
        "Property": {
            "Guid": None,
            "Type": "JM_PROPERTY",
            "Reference": None,
            "ParentReference": None,
            "Name": "CF83 8QQ",
            "Title": None,
            "Address": {
                "Name": None,
                "Lines": [
                    "1 WandW Street",
                    "Caerphilly",
                    "CF83 8QQ",
                    "Caerphilly"
                ],
                "HouseNo": None,
                "PostCode": "CF83 8QQ",
                "GeoX": 51.59534,
                "GeoXSpecified": True,
                "GeoY": -3.15364,
                "GeoYSpecified": True,
                "URL": None
            },
            "Phone": None,
            "WorkPhone": None,
            "MobilePhone": None,
            "Email": None,
            "URL": None,
            "Assets": [],
            "ExtendedProperties": {
                "PreferredName": None,
                "ID": None,
                "IDLabel": None,
                "DateOfBirthSpecified": False,
                "DateOfDeathSpecified": False,
                "Gender": "Wales & West 1"
            }
        },
        "Supervisor": None,
        "Status": "NEW",
        "StatusChangeDateSpecified": False,
        "CreatedDate": "2024-09-06T11:18:47.3932903+01:00",
        "CreatedDateSpecified": True,
        "RetrievedSpecified": False,
        "RetrievedDateSpecified": False,
        "PrintedDateSpecified": False,
        "ReceivedDateSpecified": False,
        "ResponseDateSpecified": False,
        "RequiredDate": "2023-12-30T00:00:00",
        "RequiredDateSpecified": True,
        "CompleteSpecified": False,
        "CompletedDateSpecified": False,
        "Appointment": None,
        "Schedule": {
            "StartDate": "2024-09-06T02:20:00",
            "EndDate": "2024-09-06T02:35:00"
        },
        "Priority": "Medium",
        "Origin": "ResManager",
        "SpecialInstructions": None,
        "AdditionalProperties": [
            {
                "Name": "HasMultiResourceRelatedJobs",
                "Value": "False",
                "AdditionalProperties": []
            }
        ],
        "CatalogueReference": None,
        "Lines": [],
        "Tasks": [],
        "HasPendingTasks": False,
        "Actual": None,
        "Duration": 15,
        "DurationSpecified": True
        }
    }
    

def get_frs_case_allocation_request_without_reference():
    return {
        "visit": {
        "identity": {
            "guid": "3ec86664-396c-ef11-9c35-6045bdd094a7",
            "WorkType": "FRS",
            "user": {
                "ID": 365,
                "IDSpecified": True,
                "name": "Test.INT.Wales1.01",
                "DeviceID": None,
                "userAttributes": [
                    {
                        "Name": "AuthNo",
                        "Value": "INT.Wales1.01"
                    },
                    {
                        "Name": "BlaiseLogin",
                        "Value": "test"
                    },
                    {
                        "Name": "Region",
                        "Value": "Wales"
                    },
                    {
                        "Name": "Region",
                        "Value": "North West"
                    },
                    {
                        "Name": "Skill",
                        "Value": "LMS"
                    },
                    {
                        "Name": "Team",
                        "Value": "North West 1"
                    },
                    {
                        "Name": "Team",
                        "Value": "Wales 1"
                    }
                ]
            },
            "Company": "NA"
        },
        "ClientReference": None,
        "Description": "UAC 3600 1234 1200 Due date 30/12/2023 Study LMS2311_PT1 Case ID11000000",
        "Property": {
            "Guid": None,
            "Type": "JM_PROPERTY",
            "Reference": None,
            "ParentReference": None,
            "Name": "CF83 8QQ",
            "Title": None,
            "Address": {
                "Name": None,
                "Lines": [
                    "1 WandW Street",
                    "Caerphilly",
                    "CF83 8QQ",
                    "Caerphilly"
                ],
                "HouseNo": None,
                "PostCode": "CF83 8QQ",
                "GeoX": 51.59534,
                "GeoXSpecified": True,
                "GeoY": -3.15364,
                "GeoYSpecified": True,
                "URL": None
            },
            "Phone": None,
            "WorkPhone": None,
            "MobilePhone": None,
            "Email": None,
            "URL": None,
            "Assets": [],
            "ExtendedProperties": {
                "PreferredName": None,
                "ID": None,
                "IDLabel": None,
                "DateOfBirthSpecified": False,
                "DateOfDeathSpecified": False,
                "Gender": "Wales & West 1"
            }
        },
        "Supervisor": None,
        "Status": "NEW",
        "StatusChangeDateSpecified": False,
        "CreatedDate": "2024-09-06T11:18:47.3932903+01:00",
        "CreatedDateSpecified": True,
        "RetrievedSpecified": False,
        "RetrievedDateSpecified": False,
        "PrintedDateSpecified": False,
        "ReceivedDateSpecified": False,
        "ResponseDateSpecified": False,
        "RequiredDate": "2023-12-30T00:00:00",
        "RequiredDateSpecified": True,
        "CompleteSpecified": False,
        "CompletedDateSpecified": False,
        "Appointment": None,
        "Schedule": {
            "StartDate": "2024-09-06T02:20:00",
            "EndDate": "2024-09-06T02:35:00"
        },
        "Priority": "Medium",
        "Origin": "ResManager",
        "SpecialInstructions": None,
        "AdditionalProperties": [
            {
                "Name": "HasMultiResourceRelatedJobs",
                "Value": "False",
                "AdditionalProperties": []
            }
        ],
        "CatalogueReference": None,
        "Lines": [],
        "Tasks": [],
        "HasPendingTasks": False,
        "Actual": None,
        "Duration": 15,
        "DurationSpecified": True
        }
    }


# def get_update_case_request_without_association_element():
#     update_request = get_populated_update_case_request_for_contact_made()
#     del update_request["result"]["association"]
#     return update_request


# def get_update_case_request_without_reference_element():
#     update_request = get_populated_update_case_request_for_contact_made()
#     del update_request["result"]["association"]["reference"]
#     return update_request


# def get_update_case_request_with_malformed_reference_element(
#     reference="LMS2101-AA1:90001",
# ):
#     update_request = get_populated_update_case_request_for_contact_made()
#     update_request["result"]["association"]["reference"] = reference
#     return update_request


# def get_malformed_update_case_request():
#     update_request = get_populated_update_case_request_for_contact_made()
#     del update_request["result"]["responses"]
#     return update_request
