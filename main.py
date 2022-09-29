import os

import flask
from dotenv import load_dotenv

import cloud_functions.create_totalmobile_jobs_processor
import cloud_functions.create_totalmobile_jobs_trigger
import cloud_functions.delete_totalmobile_jobs_completed_in_blaise
from app.app import load_config, setup_app
from appconfig import Config
from client import OptimiseClient
from cloud_functions.logging import setup_logger
from services.eligible_case_service import EligibleCaseService
from services.blaise_service import BlaiseService
from services.datastore_service import DatastoreService
from services.delete_totalmobile_jobs_service import DeleteTotalmobileJobsService
from services.questionnaire_service import QuestionnaireService
from services.totalmobile_service import TotalmobileService
from services.uac_service import UacService


def create_totalmobile_jobs_trigger(_event, _context) -> str:
    config = Config.from_env()
    questionnaire_service = QuestionnaireService(
        config,
        blaise_service=BlaiseService(config),
        eligible_case_service=EligibleCaseService(),
        uac_service=UacService(config),
        datastore_service=DatastoreService()
    )
    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
    totalmobile_service = TotalmobileService(optimise_client)

    return (
        cloud_functions.create_totalmobile_jobs_trigger.create_totalmobile_jobs_trigger(
            config, totalmobile_service, questionnaire_service
        )
    )


def create_totalmobile_jobs_processor(request: flask.Request) -> str:
    config = Config.from_env()
    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
    totalmobile_service = TotalmobileService(optimise_client)
    return cloud_functions.create_totalmobile_jobs_processor.create_totalmobile_jobs_processor(
        request, totalmobile_service
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
