def get_populated_update_case_request(
        reference="LMS2101-AA1.90001",
        outcome_code="300",
        contact_name="Duncan Bell",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123"
):
    return {
        "Result": {
            "User": {
                "ID": 263,
                "IDSpecified": True,
                "Name": "Test.INT.NW2.01",
                "DeviceID": "DUNCANFIELDSIPHONEc2e1238c-12d4-4e3a-962b-9c95a8be",
                "UserAttributes": [
                    {
                        "Name": "AuthNo",
                        "Value": "INT.NW2.01"
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
                        "Value": "North West 2"
                    }
                ]
            },
            "Date": "2022-08-15T11:31:09.94",
            "Form": {
                "Reference": "LMS-Contact Made No Visit",
                "Version": 1
            },
            "Association": {
                "WorkType": "LMS",
                "Reference": reference,
                "PropertyReference": "L98BN68OnsStreet",
                "ClientReference": ""
            },
            "Responses": [
                {
                    "Instance": 0,
                    "Responses": [
                        {
                            "Value": "300-10",
                            "Description": None,
                            "Element": {
                                "Reference": "Secondary_Outcome",
                                "Text": "Contact Made Detail",
                                "EnrichContentSpecified": False
                            }
                        },
                        {
                            "Value": outcome_code,
                            "Description": None,
                            "Element": {
                                "Reference": "Primary_Outcome",
                                "Text": "Primary Outcome (Hidden)",
                                "EnrichContentSpecified": False
                            }
                        }
                    ],
                    "Element": {
                        "Reference": "LMS_CMNV",
                        "Text": "Contact Made No Visits",
                        "EnrichContentSpecified": False
                    }
                },
                {
                    "Instance": 0,
                    "Responses": [
                        {
                            "Value": contact_name,
                            "Description": None,
                            "Element": {
                                "Reference": "Contact_Name",
                                "Text": "Name:",
                                "EnrichContentSpecified": False
                            }
                        },
                        {
                            "Value": home_phone_number,
                            "Description": None,
                            "Element": {
                                "Reference": "Contact_Tel1",
                                "Text": "Tel no 1:",
                                "EnrichContentSpecified": False
                            }
                        },
                        {
                            "Value": mobile_phone_number,
                            "Description": None,
                            "Element": {
                                "Reference": "Contact_Tel2",
                                "Text": "Tel no 2:",
                                "EnrichContentSpecified": None
                            }
                        }
                    ],
                    "Element": {
                        "Reference": "LMS_CD",
                        "Text": "Contact Details",
                        "EnrichContentSpecified": None
                    }
                }
            ],
            "ResultGuid": "f1bbda42-f21f-4775-8e34-c474119028ef"
        }
    }


def get_update_case_request_without_association_element():
    update_request = get_populated_update_case_request()
    del update_request["Result"]["Association"]
    return update_request


def get_update_case_request_without_reference_element():
    update_request = get_populated_update_case_request()
    del update_request["Result"]["Association"]["Reference"]
    return update_request
