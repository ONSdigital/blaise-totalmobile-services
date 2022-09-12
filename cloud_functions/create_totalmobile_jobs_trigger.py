import asyncio
import logging
from datetime import datetime
from typing import List
from uuid import uuid4

from google.cloud import datastore

from appconfig import Config
from cloud_functions.functions import prepare_tasks, run
from cloud_functions.logging import setup_logger
from models.cloud_tasks.questionnaire_case_cloud_task_model import (
    QuestionnaireCaseTaskModel,
)

setup_logger()


def create_questionnaire_case_task_name(job_model: QuestionnaireCaseTaskModel) -> str:
    return f"{job_model.questionnaire}-{str(uuid4())}"


def map_questionnaire_case_task_models(
    questionnaires: List[str],
) -> List[QuestionnaireCaseTaskModel]:
    return [
        QuestionnaireCaseTaskModel(questionnaire_name)
        for questionnaire_name in questionnaires
    ]


def get_questionnaires_with_release_date_of_today() -> list:
    records = get_datastore_records()
    today = datetime.today().strftime("%d/%m/%Y")
    return [
        record["questionnaire"]
        for record in records
        if record["tmreleasedate"].strftime("%d/%m/%Y") == today
    ]


def get_datastore_records() -> list:
    datastore_client = datastore.Client()
    query = datastore_client.query(kind="TmReleaseDate")
    return list(query.fetch())


def __filter_missing_fields(case, REQUIRED_FIELDS) -> List[str]:
    return list(filter(lambda field: field not in case, REQUIRED_FIELDS))


def validate_request(request_json: Dict) -> None:
    REQUIRED_FIELDS = ["questionnaire"]
    missing_fields = __filter_missing_fields(request_json, REQUIRED_FIELDS)
    if len(missing_fields) >= 1:
        raise Exception(
            f"Required fields missing from request payload: {missing_fields}"
        )


def get_cases_with_valid_world_ids(
    filtered_cases: List[BlaiseCaseInformationModel], world_model: TotalmobileWorldModel
) -> List[BlaiseCaseInformationModel]:
    cases_with_valid_world_ids = []
    for case in filtered_cases:
        if case.field_region == "":
            logging.warning("Case rejected. Missing Field Region")
        elif world_model.get_world_id(case.field_region) is None:
            logging.warning(f"Unsupported world: {case.field_region}")
        else:
            cases_with_valid_world_ids.append(case)
    return cases_with_valid_world_ids


def map_totalmobile_job_models(
    cases: List[BlaiseCaseInformationModel],
    world_model: TotalmobileWorldModel,
    questionnaire_name: str,
) -> List[TotalmobileJobRequestModel]:
    return [
        TotalmobileJobRequestModel(
            questionnaire_name,
            world_model.get_world_id(case.field_region),
            case.case_id,
            TotalMobileOutgoingJobPayloadModel.import_case(
                questionnaire_name, case
            ).to_payload(),
        )
        for case in cases
    ]


def run_async_tasks(tasks: List[Tuple[str, bytes]], queue_id: str, cloud_function: str):
    task_requests = prepare_tasks(
        tasks=tasks, queue_id=queue_id, cloud_function_name=cloud_function
    )

    asyncio.run(run(task_requests))

def create_questionnaire_case_tasks(
    request: flask.Request, config: Config, totalmobile_service: TotalmobileService
) -> str:
    questionnaire_service = QuestionnaireService(
        config,
        blaise_service=BlaiseService(config),
        eligible_case_service=eligible_case_service,
        uac_service=UacService(config),
    )

    logging.info("Started creating questionnaire case tasks")

    request_json = request.get_json()
    if request_json is None:
        logging.info("Function was not triggered by a valid request")
        raise Exception("Function was not triggered by a valid request")
    validate_request(request_json)

    questionnaire_name = request_json["questionnaire"]
    wave = questionnaire_service.get_wave_from_questionnaire_name(questionnaire_name)
    if wave != "1":
        logging.info(
            f"questionnaire name {questionnaire_name} does not end with a valid wave, currently only wave 1 is supported"
        )
        raise Exception(
            f"questionnaire name {questionnaire_name} does not end with a valid wave, currently only wave 1 is supported"
        )

    logging.info(f"Creating case tasks for questionnaire {questionnaire_name}")

    eligible_cases = questionnaire_service.get_eligible_cases(questionnaire_name)
    logging.info(
        f"Retrieved {len(eligible_cases)} cases for questionnaire {questionnaire_name}"
    )

    if len(eligible_cases) == 0:
        logging.info(
            f"Exiting as no eligible cases to send for questionnaire {questionnaire_name}"
        )
        return f"Exiting as no eligible cases to send for questionnaire {questionnaire_name}"
    logging.info(f"{len(eligible_cases)} eligible cases found")

    world_model = totalmobile_service.get_world_model()
    logging.info(f"Retrieved world id model")

    cases_with_valid_world_ids = get_cases_with_valid_world_ids(
        eligible_cases, world_model
    )
    logging.info(f"Finished searching for cases with valid world ids")

    totalmobile_job_models = map_totalmobile_job_models(
        cases_with_valid_world_ids, world_model, questionnaire_name
    )
    logging.info(
        f"Finished mapping Totalmobile jobs for questionnaire {questionnaire_name}"
    )

    tasks = [
        (job_model.create_task_name(), job_model.json().encode())
        for job_model in totalmobile_job_models
    ]
    logging.info(
        f"Creating {len(tasks)} cloud tasks for questionnaire {questionnaire_name}"
    )

    run_async_tasks(
        tasks=tasks,
        queue_id=config.totalmobile_jobs_queue_id,
        cloud_function=config.totalmobile_job_cloud_function,
    )
    logging.info("Finished creating questionnaire case tasks")
    return "Done"

def create_totalmobile_jobs_trigger() -> str:

    logging.info("Checking for questionnaire release dates")

    questionnaires_with_release_date_of_today = (
        get_questionnaires_with_release_date_of_today()
    )

    if questionnaires_with_release_date_of_today == []:
        logging.info("There are no questionnaires with a release date of today")
        return "There are no questionnaires with a release date of today"

    for questionnaire in questionnaires_with_release_date_of_today:
        logging.info(f"Questionnaire {questionnaire} has a release date of today")

    questionnaire_case_task_models = map_questionnaire_case_task_models(
        questionnaires_with_release_date_of_today
    )

    tasks = [
        (create_questionnaire_case_task_name(job_model), job_model.json().encode())
        for job_model in questionnaire_case_task_models
    ]

    config = Config.from_env()

    questionnaire_task_requests = prepare_tasks(
        tasks=tasks,
        queue_id=config.totalmobile_jobs_queue_id,
        cloud_function_name=config.totalmobile_job_cloud_function,
    )

    asyncio.run(run(questionnaire_task_requests))

    return "Done"
