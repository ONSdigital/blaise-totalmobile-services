import flask
import logging
import os

from dotenv import load_dotenv

import cloud_functions.create_totalmobile_jobs_processor
import cloud_functions.create_totalmobile_jobs_trigger
import cloud_functions.delete_totalmobile_jobs_completed_in_blaise
import cloud_functions.delete_totalmobile_jobs_past_field_period
from app.app import load_config, setup_app
from cloud_functions.logging import setup_logger
from factories.service_instance_factory import ServiceInstanceFactory

service_instance_factory = ServiceInstanceFactory()


def create_totalmobile_jobs_trigger(request: flask.Request) -> str:
    try:
        survey_type = request.get_json()["survey_type"]
    except Exception as err:
        logging.error(f"Could not parse JSON request: {err}")
        raise Exception

    if survey_type not in ("LMS", "FRS"):
        logging.error(f"survey_type of '{survey_type}' is invalid")
        raise Exception

    logging.info(f"BTS Create Jobs triggered for survey: '{survey_type}'")
    return cloud_functions.create_totalmobile_jobs_trigger.create_totalmobile_jobs_trigger(
        create_totalmobile_jobs_service=service_instance_factory.create_totalmobile_jobs_service(
            survey_type
        )
    )


def create_totalmobile_jobs_processor(request: flask.Request) -> str:
    return cloud_functions.create_totalmobile_jobs_processor.create_totalmobile_jobs_processor(
        request=request,
        totalmobile_service=service_instance_factory.create_totalmobile_service(),
    )


def delete_totalmobile_jobs_completed_in_blaise(_request: flask.Request) -> str:
    return cloud_functions.delete_totalmobile_jobs_completed_in_blaise.delete_totalmobile_jobs_completed_in_blaise(
        blaise_outcome_service=service_instance_factory.create_blaise_outcome_service(),
        totalmobile_service=service_instance_factory.create_totalmobile_service(),
    )


def delete_totalmobile_jobs_past_field_period(_request: flask.Request) -> str:
    return cloud_functions.delete_totalmobile_jobs_past_field_period.delete_totalmobile_jobs_past_field_period(
        blaise_outcome_service=service_instance_factory.create_blaise_outcome_service(),
        totalmobile_service=service_instance_factory.create_totalmobile_service(),
    )


if os.path.isfile("./.env"):
    print("Loading environment variables from dotenv file")
    load_dotenv()

app = setup_app()
load_config(app)

if __name__ == "__main__":
    setup_logger()
    print("Running Flask application")
    app.run_tasks(host="0.0.0.0", port=5011)
