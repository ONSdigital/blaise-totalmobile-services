def get_frs_case_unallocation_request():
    return {
        "Reason": None,
        "identity": {
            "guid": None,
            "WorkType": "FRS",
            "user": {
                "IDSpecified": False,
                "name": "Interviewer1",
                "DeviceID": None,
                "UserAttributes": [],
            },
            "Company": "NA",
            "reference": "FRS2405A.9001",
        },
        "PreserveIfNoLinesRemainingSpecified": False,
        "Lines": [],
        "UseSilentPushSpecified": False,
    }


def get_frs_case_unallocation_request_with_reference_from_param(reference: str):
    return {
        "Reason": None,
        "identity": {
            "guid": None,
            "WorkType": "FRS",
            "user": {
                "IDSpecified": False,
                "name": "Callum.Nicholson",
                "DeviceID": None,
                "UserAttributes": [],
            },
            "Company": "NA",
            "reference": reference,
        },
        "PreserveIfNoLinesRemainingSpecified": False,
        "Lines": [],
        "UseSilentPushSpecified": False,
    }


def get_frs_case_unallocation_request_without_reference():
    return {
        "Reason": None,
        "identity": {
            "guid": None,
            "WorkType": "FRS",
            "user": {
                "IDSpecified": False,
                "name": "Interviewer1",
                "DeviceID": None,
                "UserAttributes": [],
            },
            "Company": "NA",
        },
        "PreserveIfNoLinesRemainingSpecified": False,
        "Lines": [],
        "UseSilentPushSpecified": False,
    }
