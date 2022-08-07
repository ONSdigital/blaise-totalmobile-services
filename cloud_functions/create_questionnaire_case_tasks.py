import asyncio
import logging
from typing import Dict, List, Tuple
from uuid import uuid4

import flask

from appconfig import Config
from cloud_functions.logging import setup_logger
from cloud_functions.functions import prepare_tasks, run
from models.totalmobile_job_model import TotalmobileJobModel
from models.questionnaire_case_model import QuestionnaireCaseModel
from services import questionnaire_service, world_id_service

setup_logger()


def __filter_missing_fields(case, REQUIRED_FIELDS) -> List[str]:
    return list(filter(lambda field: field not in case, REQUIRED_FIELDS))


def validate_request(request_json: Dict) -> None:
    REQUIRED_FIELDS = ["questionnaire"]
    missing_fields = __filter_missing_fields(request_json, REQUIRED_FIELDS)
    if len(missing_fields) >= 1:
        raise Exception(
            f"Required fields missing from request payload: {missing_fields}"
        )


def get_cases_with_valid_world_ids(filtered_cases: List[QuestionnaireCaseModel], world_ids) -> List[str]:
    cases_with_valid_world_ids = []
    for case in filtered_cases:
        if case.field_region == "":
            logging.warning("Case rejected. Missing Field Region")
        elif case.field_region not in world_ids:
            logging.warning(f"Unsupported world: {case.field_region}")
        else:
            cases_with_valid_world_ids.append(case)
    return cases_with_valid_world_ids


def map_totalmobile_job_models(
        cases: List[QuestionnaireCaseModel], world_ids: List[str], questionnaire_name: str
) -> List[TotalmobileJobModel]:
    return [TotalmobileJobModel(questionnaire_name, world_id, case.to_dict()) for case, world_id in zip(cases, world_ids)]


def create_task_name(job_model: TotalmobileJobModel) -> str:
    return (
        f"{job_model.questionnaire}-{job_model.case['qiD.Serial_Number']}-{str(uuid4())}"
    )


def run_async_tasks(tasks: List[Tuple[str, str]], queue_id: str, cloud_function: str):
    task_requests = prepare_tasks(
        tasks=tasks,
        queue_id=queue_id,
        cloud_function_name=cloud_function
    )

    asyncio.run(run(task_requests))


def create_questionnaire_case_tasks(request: flask.Request, config: Config) -> str:
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
            f"questionnaire name {questionnaire_name} does not end with a valid wave, currently only wave 1 is supported")
        raise Exception(
            f"questionnaire name {questionnaire_name} does not end with a valid wave, currently only wave 1 is supported")

    logging.info(f"Creating case tasks for questionnaire {questionnaire_name}")

    eligible_cases = questionnaire_service.get_eligible_cases(questionnaire_name, config)
    logging.info(f"Retrieved {len(eligible_cases)} cases for questionnaire {questionnaire_name}")

    if len(eligible_cases) == 0:
        logging.info(f"Exiting as no eligible cases to send for questionnaire {questionnaire_name}")
        return f"Exiting as no eligible cases to send for questionnaire {questionnaire_name}"
    logging.info(f"{len(eligible_cases)} eligible cases found")

    world_ids = world_id_service.get_world_ids(config)
    logging.info(f"Retrieved world ids")

    cases_with_valid_world_ids = get_cases_with_valid_world_ids(eligible_cases, world_ids)
    logging.info(f"Finished searching for cases with valid world ids")

    totalmobile_job_models = map_totalmobile_job_models(
        cases_with_valid_world_ids, world_ids, questionnaire_name
    )
    logging.info(f"Finished mapping Totalmobile jobs for questionnaire {questionnaire_name}")

    tasks = [
        (create_task_name(job_model), job_model.json().encode())
        for job_model in totalmobile_job_models
    ]
    logging.info(f"Creating {len(tasks)} cloud tasks for questionnaire {questionnaire_name}")

    run_async_tasks(tasks=tasks, queue_id=config.totalmobile_jobs_queue_id,
                    cloud_function=config.totalmobile_job_cloud_function)
    logging.info("Finished creating questionnaire case tasks")
    return "Done"
