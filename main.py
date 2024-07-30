import logging
import os

import flask
from dotenv import load_dotenv

import cloud_functions.create_totalmobile_jobs_processor
import cloud_functions.create_totalmobile_jobs_trigger
import cloud_functions.delete_totalmobile_jobs_completed_in_blaise
import cloud_functions.delete_totalmobile_jobs_past_field_period
from app.app import load_config, setup_app
from appconfig import Config
from client import OptimiseClient
from client.messaging import MessagingClient
from cloud_functions.logging import setup_logger
from services.blaise_case_outcome_service import BlaiseCaseOutcomeService
from services.blaise_service import RealBlaiseService
from services.case_filters.case_filter_wave_1 import CaseFilterWave1
from services.case_filters.case_filter_wave_2 import CaseFilterWave2
from services.case_filters.case_filter_wave_3 import CaseFilterWave3
from services.case_filters.case_filter_wave_4 import CaseFilterWave4
from services.case_filters.case_filter_wave_5 import CaseFilterWave5
from services.cloud_task_service import CloudTaskService
from services.create_totalmobile_jobs_service import CreateTotalmobileJobsService
from services.datastore_service import DatastoreService
from services.eligible_case_service import EligibleCaseService
from services.eligible_frs_case_service import EligibleFRSCaseService
from services.frs_questionnaire_service import FRSQuestionnaireService
from services.questionnaire_service import QuestionnaireService
from services.totalmobile_service import RealTotalmobileService
from services.uac_service import UacService


def _create_totalmobile_service(config: Config) -> RealTotalmobileService:
    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
    messaging_client = MessagingClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
    return RealTotalmobileService(optimise_client, messaging_client)


def create_totalmobile_jobs_trigger(_event, _context) -> str:
    config = Config.from_env()

    lms_questionnaire_service = QuestionnaireService(
        blaise_service=RealBlaiseService(config),
        eligible_case_service=EligibleCaseService(
            wave_filters=[
                CaseFilterWave1(),
                CaseFilterWave2(),
                CaseFilterWave3(),
                CaseFilterWave4(),
                CaseFilterWave5(),
            ]
        ),
        datastore_service=DatastoreService(),
    )

    frs_questionnaire_service = FRSQuestionnaireService(
        blaise_service=RealBlaiseService(config),
        eligible_case_service=EligibleFRSCaseService(),
        datastore_service=DatastoreService(),
    )

    totalmobile_service = _create_totalmobile_service(config)
    uac_service = UacService(config=config)
    cloud_task_service = CloudTaskService(
        config=config, task_queue_id=config.create_totalmobile_jobs_task_queue_id
    )



        # get a list of all questionnaires that have a release date of today
        # get eligible cases for each questionnaire
        # map eligible cases to totalmobile job model
        # create cloud task for each totalmobile job model


    cloud_functions.create_totalmobile_jobs_trigger.create_totalmobile_jobs_trigger(
                create_totalmobile_jobs_service=CreateTotalmobileJobsService(
                    totalmobile_service=totalmobile_service,
                    questionnaire_service=lms_questionnaire_service,
                    uac_service=uac_service,
                    cloud_task_service=cloud_task_service,
                )
            )    

    return "done"
    

def create_totalmobile_jobs_processor(request: flask.Request) -> str:
    config = Config.from_env()
    totalmobile_service = _create_totalmobile_service(config)
    return cloud_functions.create_totalmobile_jobs_processor.create_totalmobile_jobs_processor(
        request=request, totalmobile_service=totalmobile_service
    )


def delete_totalmobile_jobs_completed_in_blaise(_request: flask.Request) -> str:
    config = Config.from_env()
    totalmobile_service = _create_totalmobile_service(config=config)
    blaise_outcome_service = BlaiseCaseOutcomeService(
        blaise_service=RealBlaiseService(config=config)
    )

    return cloud_functions.delete_totalmobile_jobs_completed_in_blaise.delete_totalmobile_jobs_completed_in_blaise(
        blaise_outcome_service=blaise_outcome_service,
        totalmobile_service=totalmobile_service,
    )


def delete_totalmobile_jobs_past_field_period(_request: flask.Request) -> str:
    config = Config.from_env()
    totalmobile_service = _create_totalmobile_service(config=config)
    blaise_outcome_service = BlaiseCaseOutcomeService(
        blaise_service=RealBlaiseService(config=config)
    )

    return cloud_functions.delete_totalmobile_jobs_past_field_period.delete_totalmobile_jobs_past_field_period(
        blaise_outcome_service=blaise_outcome_service,
        totalmobile_service=totalmobile_service,
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
