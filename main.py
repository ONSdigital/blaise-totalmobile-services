import os

import flask
from dotenv import load_dotenv

import cloud_functions.create_totalmobile_jobs_trigger
import cloud_functions.create_questionnaire_case_tasks
import cloud_functions.create_totalmobile_jobs_processor
import cloud_functions.delete_totalmobile_jobs_completed_in_blaise
from app.app import load_config, setup_app
from appconfig import Config
from client import OptimiseClient
from cloud_functions.logging import setup_logger
from services.blaise_service import BlaiseService
from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService
from services.totalmobile_service import TotalmobileService


def create_totalmobile_jobs_processor(request: flask.Request) -> str:
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
    return (
        cloud_functions.create_questionnaire_case_tasks.create_questionnaire_case_tasks(
            request, config, totalmobile_service
        )
    )


def create_totalmobile_jobs_trigger(_event, _context) -> str:
    return (
        cloud_functions.check_questionnaire_release_date.create_totalmobile_jobs_trigger()
    )


def delete_totalmobile_jobs_completed_in_blaise(_event, _context) -> str:
    config = Config.from_env()
    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
    totalmobile_service = TotalmobileService(optimise_client)
    blaise_service = BlaiseService(config)
    delete_jobs_service = DeleteTotalmobileJobsService(
        totalmobile_service, blaise_service
    )
    return cloud_functions.delete_totalmobile_jobs_completed_in_blaise.delete_totalmobile_jobs_completed_in_blaise(
        delete_jobs_service
    )


if os.path.isfile("./.env"):
    print("Loading environment variables from dotenv file")
    load_dotenv()

app = setup_app()
load_config(app)


if __name__ == "__main__":
    setup_logger()
    print("Running Flask application")
    app.run(host="0.0.0.0", port=5011)
