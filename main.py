import os

import flask
from dotenv import load_dotenv

import cloud_functions.check_questionnaire_release_date
import cloud_functions.create_questionnaire_case_tasks
import cloud_functions.create_totalmobile_job
import cloud_functions.delete_totalmobile_jobs_completed_in_blaise
from app.app import load_config, setup_app
from appconfig import Config
from client import OptimiseClient
from cloud_functions.logging import setup_logger
from services.totalmobile_service import TotalmobileService


def create_totalmobile_job(request: flask.Request) -> str:
    config = Config.from_env()
    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
    totalmobile_service = TotalmobileService(optimise_client)
    return cloud_functions.create_totalmobile_job.create_totalmobile_job(
        request, totalmobile_service
    )


def create_questionnaire_case_tasks(request: flask.Request) -> str:
    config = Config.from_env()
    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
    totalmobile_service = TotalmobileService(optimise_client)
    return cloud_functions.create_questionnaire_case_tasks.create_questionnaire_case_tasks(
        request, config, totalmobile_service
    )


def check_questionnaire_release_date(_event, _context) -> str:
    return (
        cloud_functions.check_questionnaire_release_date.check_questionnaire_release_date()
    )


def delete_totalmobile_jobs_completed_in_blaise(_event, _context) -> str:
    return cloud_functions.delete_totalmobile_jobs_completed_in_blaise.delete_totalmobile_jobs_completed_in_blaise()


if os.path.isfile("./.env"):
    print("Loading environment variables from dotenv file")
    load_dotenv()

app = setup_app()
load_config(app)


if __name__ == "__main__":
    setup_logger()
    print("Running Flask application")
    app.run(host="0.0.0.0", port=5011)
