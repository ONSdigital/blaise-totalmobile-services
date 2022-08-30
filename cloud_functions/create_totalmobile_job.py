import logging

import flask

from cloud_functions.logging import setup_logger
from models.cloud_tasks.totalmobile_outgoing_job_model import TotalmobileJobModel
from services.totalmobile_service import TotalmobileService

setup_logger()


def create_totalmobile_job(
    request: flask.Request, totalmobile_service: TotalmobileService
) -> str:
    request_json = request.get_json()

    if request_json is None:
        logging.error("Function was not triggered by a valid request")
        raise Exception("Function was not triggered by a valid request")

    logging.info(f"Totalmobile job request {request_json}")

    totalmobile_job = TotalmobileJobModel.import_job(request_json)

    logging.info(
        f"Creating Totalmobile job for questionnaire {totalmobile_job.questionnaire} with case ID {totalmobile_job.case_id}"
    )
    response = totalmobile_service.create_job(totalmobile_job)
    logging.info(f"Response: {response}")
    return "Done"
