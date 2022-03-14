import os
from optimise import OptimiseClient
import flask

totalmobile_url = os.environ["TOTALMOBILE_URL"]
totalmobile_instance = os.environ["TOTALMOBILE_INSTANCE"]
totalmobile_client_id = os.environ["TOTALMOBILE_CLIENT_ID"]
totalmobile_client_secret = os.environ["TOTALMOBILE_CLIENT_SECRET"]


def TestTMCreateJob(request: flask.Request) -> str:
    optimise_client = OptimiseClient(
        totalmobile_url,
        totalmobile_instance,
        totalmobile_client_id,
        totalmobile_client_secret,
    )

    request_json = request.get_json()

    if request_json is None:
        raise Exception("Function was not triggered by a valid request")

    instrument = request_json["instrument"]
    case = request_json["case"]
    world_id = request_json["world_id"]

    response = optimise_client.create_job(
        world_id,
        {
            "identity": {"reference": f"{instrument[:3]}{case['qiD.Serial_Number']}"},
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
                "address": f"{case['qDataBag.Prem1']}, {case['qDataBag.Prem2']}, {case['qDataBag.PostTown']}",
                "reference": case["qiD.Serial_Number"],
                "addressDetail": {
                    "name": f"{case['qDataBag.Prem1']}, {case['qDataBag.Prem2']}, {case['qDataBag.PostTown']}",
                    "addressLine2": case["qDataBag.Prem1"],
                    "addressLine3": case["qDataBag.Prem2"],
                    "addressLine4": case["qDataBag.PostTown"],
                    "postCode": case["qDataBag.PostCode"],
                    "coordinates": {
                        "latitude": case["qDataBag.UPRN_Latitude"],
                        "longitude": case["qDataBag.UPRN_Longitude"],
                    },
                },
            },
            "contact": {
                "name": case["qDataBag.PostCode"],
                "homePhone": case["qDataBag.TelNo"],
                "mobilePhone": case["qDataBag.TelNo2"],
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
        },
    )
    print(response.json())
    print(response.status_code)
    if response.status_code != 201:
        raise Exception(f"Error response {response.status_code}: {response.text}")
    return "Done"
