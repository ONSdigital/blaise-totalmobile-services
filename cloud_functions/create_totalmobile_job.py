import logging
import flask

from appconfig import Config
from client import OptimiseClient
from cloud_functions.logging import setup_logger
from models.totalmobile_job_model import TotalmobileJobModel

setup_logger()


# def validate_request(request_json: Dict) -> None:
#     REQUIRED_FIELDS = ["questionnaire", "case", "world_id"]
#     missing_fields = __filter_missing_fields(request_json, REQUIRED_FIELDS)
#     if len(missing_fields) >= 1:
#         raise Exception(
#             f"Required fields missing from request payload: {missing_fields}"
#         )
#     validate_case_data(request_json["case"])

#
# def validate_case_data(case: Dict) -> None:
#     REQUIRED_FIELDS = [
#         "qiD.Serial_Number",
#         "dataModelName",
#         "qDataBag.TLA",
#         "qDataBag.Wave",
#         "qDataBag.Prem1",
#         "qDataBag.Prem2",
#         "qDataBag.Prem3",
#         "qDataBag.District",
#         "qDataBag.PostTown",
#         "qDataBag.PostCode",
#         "qDataBag.TelNo",
#         "qDataBag.TelNo2",
#         "telNoAppt",
#         "hOut",
#         "qDataBag.UPRN_Latitude",
#         "qDataBag.UPRN_Longitude",
#         "qDataBag.Priority",
#         "qDataBag.FieldRegion",
#         "qDataBag.FieldTeam",
#         "qDataBag.WaveComDTE",
#     ]
#     missing_fields = __filter_missing_fields(case, REQUIRED_FIELDS)
#     if len(missing_fields) >= 1:
#         raise Exception(f"Required fields missing from case data: {missing_fields}")

# def validate_totalmobile_payload(totalmobile_payload):
#     if "duration" not in totalmobile_payload:
#         logging.warning("Totalmobile payload was sent without the 'duration' field")
#     if "origin" not in totalmobile_payload:
#         logging.warning("Totalmobile payload was sent without the 'origin' field")
#     for property in totalmobile_payload["additionalProperties"]:
#         if "uac" in property["name"] and property["value"] == "":
#             logging.warning(f"Totalmobile payload was sent with an empty {property['name']} field")


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

    logging.info(f"Totalmobile job request {request_json}")

    totalmobile_job = TotalmobileJobModel.import_job(request_json)

    logging.info(
        f"Creating Totalmobile job for questionnaire {totalmobile_job.questionnaire} with case ID {totalmobile_job.case_id}")
    response = optimise_client.create_job(
        totalmobile_job.world_id,
        totalmobile_job.payload
    )
    logging.info(f"Response: {response}")
    return "Done"


# def __filter_missing_fields(case, REQUIRED_FIELDS) -> List[str]:
#     return list(filter(lambda field: field not in case, REQUIRED_FIELDS))