from typing import Dict, List

import flask

from appconfig import Config
from client import OptimiseClient


def validate_request(request_json: Dict) -> None:
    REQUIRED_FIELDS = ["questionnaire", "case", "world_id"]
    missing_fields = __filter_missing_fields(request_json, REQUIRED_FIELDS)
    if len(missing_fields) >= 1:
        raise Exception(
            f"Required fields missing from request payload: {missing_fields}"
        )
    validate_case_data(request_json["case"])


def validate_case_data(case: Dict) -> None:
    REQUIRED_FIELDS = [
        "qiD.Serial_Number",
        "qDataBag.Prem1",
        "qDataBag.Prem2",
        "qDataBag.Prem3",
        "qDataBag.PostTown",
        "qDataBag.PostCode",
        # "qDataBag.UPRN_Latitude", This field aren't strictly required but do make the world better...
        # "qDataBag.UPRN_Longitude", This field aren't strictly required but do make the world better...
        "qDataBag.TelNo",
        "qDataBag.TelNo2",
    ]
    missing_fields = __filter_missing_fields(case, REQUIRED_FIELDS)
    if len(missing_fields) >= 1:
        raise Exception(f"Required fields missing from case data: {missing_fields}")


def job_reference(questionnaire: str, case_id: str) -> str:
    return f"{questionnaire.replace('_', '-')}.{case_id}"


def description(questionnaire: str, case_id: str) -> str:
    return f"Study: {questionnaire}\nCase ID: {case_id}\n\nIf you need to provide a UAC please contact SEL"


def create_job_payload(request_json: Dict) -> Dict:
    questionnaire = request_json["questionnaire"]
    case = request_json["case"]

    return {
        "identity": {"reference": job_reference(questionnaire, case["qiD.Serial_Number"])},  # we must control this so we can link it back to blaise
        "origin": "ONS",
        "clientReference": "2",  # num of non contacts allowed, misused field? appears at top of the app
        "duration": 30,  # could this differ depending on survey and work type etc?
        "description": description(questionnaire, case["qiD.Serial_Number"]),
        "workType": "KTN",  # probably shouldn't be hardcoded, will likely support more work types in the future...
        "skills": [{"identity": {"reference": "KTN"}}],  # probably shouldn't be hardcoded, will likely support more skills in the future...
        "dueDate": {
            "start": "",  # !?
            "end": "",  # !?
        },
        "location": {
            "address": f"{case.get('qDataBag.Prem1')}, {case.get('qDataBag.Prem2')}, {case.get('qDataBag.PostTown')}",
            "reference": case["qiD.Serial_Number"],
            "addressDetail": {
                "name": f"{case.get('qDataBag.Prem1')}, {case.get('qDataBag.Prem2')}, {case.get('qDataBag.PostTown')}",
                "addressLine2": case.get("qDataBag.Prem1"),
                "addressLine3": case.get("qDataBag.Prem2"),
                "addressLine4": case.get("qDataBag.PostTown"),
                "postCode": case.get("qDataBag.PostCode"),
                "coordinates": {
                    "latitude": case.get("qDataBag.UPRN_Latitude"),
                    "longitude": case.get("qDataBag.UPRN_Longitude"),
                },
            },
        },
        "contact": {
            "name": case.get("qDataBag.PostCode"),  # postcode as name, misused field?
            "homePhone": case.get("qDataBag.TelNo"),
            "mobilePhone": case.get("qDataBag.TelNo2"),
            "contactDetail": {  # misused fields?
                "contactId": questionnaire[:3],  # survey tla
                "contactIdLabel": questionnaire[-1],  # wave - lms specific!
                "preferredName": questionnaire[4:7],  # 3 digit field period..!?
            },
        },
        "additionalProperties": [
            {"name": "study", "value": questionnaire},
            {"name": "case_id", "value": case["qiD.Serial_Number"]},
        ],
    }


def create_totalmobile_job(request: flask.Request) -> str:
    config = Config.from_env()

    config.validate()

    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )

    request_json = request.get_json()

    if request_json is None:
        raise Exception("Function was not triggered by a valid request")

    validate_request(request_json)

    response = optimise_client.create_job(
        request_json["world_id"], create_job_payload(request_json)
    )
    print(response)
    return "Done"


def __filter_missing_fields(case, REQUIRED_FIELDS) -> List[str]:
    return list(filter(lambda field: field not in case, REQUIRED_FIELDS))
