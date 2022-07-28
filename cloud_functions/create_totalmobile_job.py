import logging
from typing import Dict, List

import flask

from appconfig import Config
from client import OptimiseClient
from cloud_functions.logging import setup_logger

setup_logger()


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
            "dataModelName",
            "qDataBag.TLA",
            "qDataBag.Wave",            
            "qDataBag.Prem1",
            "qDataBag.Prem2",
            "qDataBag.Prem3",
            "qDataBag.District",
            "qDataBag.PostTown",
            "qDataBag.PostCode",
            "qDataBag.TelNo",
            "qDataBag.TelNo2",
            "telNoAppt",
            "hOut",
            "qDataBag.UPRN_Latitude",
            "qDataBag.UPRN_Longitude",            
            "qDataBag.Priority",
            "qDataBag.FieldRegion",
            "qDataBag.FieldTeam",
            "qDataBag.WaveComDTE",
    ]
    missing_fields = __filter_missing_fields(case, REQUIRED_FIELDS)
    if len(missing_fields) >= 1:
        raise Exception(f"Required fields missing from case data: {missing_fields}")


def create_job_reference(questionnaire: str, case_id: str) -> str:
    return f"{questionnaire.replace('_', '-')}.{case_id}"


def create_description(questionnaire: str, case_id: str) -> str:
    return f"Study: {questionnaire}\nCase ID: {case_id}"


def create_job_payload(request_json: Dict) -> Dict:
    questionnaire = request_json["questionnaire"]
    case = request_json["case"]

    logging.info(f"Questionnaire: {questionnaire}")
    logging.info(f"Case: {case}")
    totalmobile_payload = {
        "identity": {
            "reference": create_job_reference(questionnaire, case["qiD.Serial_Number"]),
            },
        "description": create_description(questionnaire, case["qiD.Serial_Number"]),
        "origin": "ONS",
        "duration": 15,
        "workType": case["qDataBag.TLA"],
        "skills": [
            {
                "identity": {
                    "reference": case["qDataBag.TLA"],
                },
            },
        ],
        "dueDate": {
            "end": case["qDataBag.WaveComDTE"],
        },
        "location": {
            "addressDetail": {
                "addressLine1": case["qDataBag.Prem1"],
                "addressLine2": case["qDataBag.Prem2"],
                "addressLine3": case["qDataBag.Prem3"],
                "addressLine4": case["qDataBag.District"],
                "addressLine5": case["qDataBag.PostTown"],
                "postCode": case["qDataBag.PostCode"],
                "coordinates": {
                    "latitude": case["qDataBag.UPRN_Latitude"],
                    "longitude": case["qDataBag.UPRN_Longitude"],
                },
            },
        },
        "contact": {
            "name": case["qDataBag.PostCode"],
        },
        "additionalProperties": [
            {
                "name": "surveyName",
                "value": case["dataModelName"]
            },
            {
                "name": "tla",
                "value": case["qDataBag.TLA"]
            },
            {
                "name": "wave",
                "value": case["qDataBag.Wave"]
            },
            {
                "name": "priority",
                "value": case["qDataBag.Priority"]
            },
            {
                "name": "fieldTeam",
                "value": case["qDataBag.FieldTeam"]
            },
            {
                "name": "uac1",
                "value": case["uac_chunks"]["uac1"]
            },
            {
                "name": "uac2",
                "value": case["uac_chunks"]["uac2"]
            },
            {
                "name": "uac3",
                "value": case["uac_chunks"]["uac3"]
            },
        ],
    }

    validate_totalmobile_payload(totalmobile_payload)
    return totalmobile_payload

def validate_totalmobile_payload(totalmobile_payload):
    if "duration" not in totalmobile_payload:
        logging.warning("Totalmobile payload was sent without the 'duration' field")
    if "origin" not in totalmobile_payload:
        logging.warning("Totalmobile payload was sent without the 'origin' field")
    for property in totalmobile_payload["additionalProperties"]:
        if "uac" in property["name"] and property["value"] == "":
            logging.warning(f"Totalmobile payload was sent with an empty {property['name']} field")


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
        logging.error("Function was not triggered by a valid request")
        raise Exception("Function was not triggered by a valid request")

    validate_request(request_json)

    logging.info(f"Creating Totalmobile job for questionnaire {request_json['questionnaire']} with case ID {request_json['case']['qiD.Serial_Number']}")
    response = optimise_client.create_job(
        request_json["world_id"], create_job_payload(request_json)
    )
    logging.info(f"Response: {response}")
    return "Done"


def __filter_missing_fields(case, REQUIRED_FIELDS) -> List[str]:
    return list(filter(lambda field: field not in case, REQUIRED_FIELDS))
