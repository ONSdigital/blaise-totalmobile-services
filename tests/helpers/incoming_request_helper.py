def get_populated_update_case_request_for_contact_made(
        reference="LMS2101-AA1.90001",
        outcome_code=300,
        contact_name="Duncan Bell",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123"
):
    return {
        "result": {
            "user": {
                "id": 1191,
                "name": "richmond.rice",
                "deviceID": "NOKIA8.35G9b080ab9-33a4-4824-b882-6019732b9dfa"
            },
            "date": "2022-08-23T15: 54: 23.323",
            "form": {
                "reference": "LMS-Contact Made No Visit",
                "version": 10
            },
            "association": {
                "workType": "LMS",
                "reference": reference,
                "propertyReference": "zz00zzons",
                "clientReference": ""
            },
            "responses": [
                {
                    "instance": 0,
                    "responses": [
                        {
                            "value": "300-10",
                            "element": {
                                "reference": "Secondary_Outcome",
                                "text": "Contact Made Detail"
                            }
                        },
                        {
                            "value": outcome_code,
                            "element": {
                                "reference": "Primary_Outcome",
                                "text": "Primary Outcome (Hidden)"
                            }
                        }
                    ],
                    "element": {
                        "reference": "LMS_CMNV",
                        "text": "Contact Made No Visits"
                    }
                },
                {
                    "instance": 0,
                    "responses": [
                        {
                            "value": contact_name,
                            "element": {
                                "reference": "Contact_Name",
                                "text": "Name:"
                            }
                        },
                        {
                            "value": home_phone_number,
                            "element": {
                                "reference": "Contact_Tel1",
                                "text": "Tel no 1:"
                            }
                        },
                        {
                            "value": mobile_phone_number,
                            "element": {
                                "reference": "Contact_Tel2",
                                "text": "Tel no 2:"
                            }
                        }
                    ],
                    "element": {
                        "reference": "LMS_CD",
                        "text": "Contact Details"
                    }
                }
            ],
            "resultGuid": "428f2b9f-ee9d-43cc-ba59-afa4fcd31529"
        }
    }


def get_populated_update_case_refusal_request(
        reference="LMS2101-AA1.90001",
        outcome_code=460
):
    return {
        "result": {
            "user": {
                "id": 1191,
                "name": "richmond.rice",
                "deviceID": "NOKIA8.35G9b080ab9-33a4-4824-b882-6019732b9dfa"
            },
            "date": "2022-08-25T11:00:28.7",
            "form": {
                "reference": "LMS-Refusal",
                "version": 36
            },
            "association": {
                "workType": "LMS",
                "reference": reference,
                "propertyReference": "postcodeprem1",
                "clientReference": ""
            },
            "responses": [
                {
                    "instance": 0,
                    "responses": [
                        {
                            "value": "460",
                            "element": {
                                "reference": "Secondary_Outcome",
                                "text": "Refusal Reason"
                            }
                        },
                        {
                            "value": outcome_code,
                            "element": {
                                "reference": "Primary_Outcome",
                                "text": "Primary Outcome (Hidden)"
                            }
                        }
                    ],
                    "element": {
                        "reference": "LMS_Refusal",
                        "text": "Refusal"
                    }
                },
                {
                    "instance": 0,
                    "responses": [
                        {
                            "value": "",
                            "element": {
                                "reference": "Important_Advice",
                                "text": "IMPORTANT: Recording this outcome will remove the case from the workload and will not be included in future Waves"
                            }
                        },
                        {
                            "value": "Reason not known",
                            "description": "Reason not known",
                            "element": {
                                "reference": "Outright_Refusal_Reason",
                                "text": "Select one of the options below"
                            }
                        }
                    ],
                    "element": {
                        "reference": "Outright_Refusal",
                        "text": "Outright Refusal"
                    }
                }
            ],
            "resultGuid": "8b0c2c69-9b2c-4fa3-8825-e3f3a2743e50"
        }
    }


def get_update_case_request_without_association_element():
    update_request = get_populated_update_case_request_for_contact_made()
    del update_request["result"]["association"]
    return update_request


def get_update_case_request_without_reference_element():
    update_request = get_populated_update_case_request_for_contact_made()
    del update_request["result"]["association"]["reference"]
    return update_request
