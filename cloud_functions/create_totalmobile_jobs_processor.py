import logging
from typing import Optional

import flask

from client.errors import BadRequest
from cloud_functions.logging import setup_logger
from models.cloud_tasks.totalmobile_job_request_model import TotalmobileJobRequestModel
from services.totalmobile_service import TotalmobileService

setup_logger()


def get_duplicate_job_message(err: BadRequest) -> Optional[str]:
    if (
        not isinstance(err.error_details, dict)
        or "jobEntity" not in err.error_details
        or not isinstance(err.error_details["jobEntity"], list)
        or len(err.error_details["jobEntity"]) == 0
        or not err.error_details["jobEntity"][0].startswith(
            "Job already exists with Reference"
        )
    ):
        return None
    return err.error_details["jobEntity"][0]


def create_totalmobile_jobs_processor(
    request: flask.Request, totalmobile_service: TotalmobileService
) -> str:
    request_json = request.get_json()

    if request_json is None:
        logging.error("Function was not triggered by a valid request")
        raise Exception("Function was not triggered by a valid request")

    logging.info(f"Totalmobile job request {request_json}")

    totalmobile_job = TotalmobileJobRequestModel.import_job(request_json)

    logging.info(
        f"Creating Totalmobile job for questionnaire {totalmobile_job.questionnaire} with case ID {totalmobile_job.case_id}"
    )
    try:
        response = totalmobile_service.create_job(totalmobile_job)
        logging.info(f"Response: {response}")
    except BadRequest as err:
        duplicate_error_message = get_duplicate_job_message(err)
        if duplicate_error_message is None:
            raise err
        logging.warning(duplicate_error_message)
    return "Done"
