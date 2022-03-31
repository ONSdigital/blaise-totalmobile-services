from typing import Dict, List
import flask
from appconfig import Config
from client import OptimiseClient


def validate_request(request_json: Dict) -> None:
    REQUIRED_FIELDS = ["instrument", "case", "world_id"]
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
        "qDataBag.UPRN_Latitude",
        "qDataBag.UPRN_Longitude",
        "qDataBag.TelNo",
        "qDataBag.TelNo2",
    ]
    missing_fields = __filter_missing_fields(case, REQUIRED_FIELDS)
    if len(missing_fields) >= 1:
        raise Exception(f"Required fields missing from case data: {missing_fields}")


def job_reference(instrument: str, case_id: str) -> str:
    return f"{instrument.replace('_', '-')}.{case_id}"


def create_job_payload(request_json: Dict) -> Dict:
    instrument = request_json["instrument"]
    case = request_json["case"]

    return {
        "identity": {"reference": job_reference(instrument, case["qiD.Serial_Number"])},
        "origin": "ONS",
        "clientReference": "2",  # num of no contacts allowed
        "duration": 30,
        "description": "test-job",
        "workType": "KTN",
        "skills": [{"identity": {"reference": "KTN"}}],
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
            "name": case.get("qDataBag.PostCode"),
            "homePhone": case.get("qDataBag.TelNo"),
            "mobilePhone": case.get("qDataBag.TelNo2"),
            "contactDetail": {
                "contactId": instrument[:3],  # survey tla
                "contactIdLabel": instrument[-1],  # wave - lms specific!
                "preferredName": instrument[4:7],  # 3 digit field period..!?
            },
        },
        "attributes": [
            {"name": "study", "value": instrument},
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
