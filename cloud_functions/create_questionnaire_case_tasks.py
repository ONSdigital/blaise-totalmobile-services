import asyncio
import logging
from typing import Dict, List, Tuple, Union
from uuid import uuid4

import flask

from appconfig import Config
from client.optimise import OptimiseClient
from cloud_functions.logging import setup_logger
from cloud_functions.functions import prepare_tasks, run
from models.totalmobile_job_model import TotalmobileJobModel
from models.questionnaire_case_model import QuestionnaireCaseModel, UacChunks
from services import questionnaire_service

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


def get_world_ids(config: Config, filtered_cases: List[QuestionnaireCaseModel]) -> List[str]:
    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
    logging.info("Looking up world ids")
    worlds = optimise_client.get_worlds()

    world_map_with_world_ids = {world["identity"]["reference"]: world["id"] for world in worlds}

    cases_with_valid_world_ids = []
    world_ids = []
    for case in filtered_cases:
        if case.field_region == "":
            logging.warning("Case rejected. Missing Field Region")
        elif case.field_region not in world_map_with_world_ids:
            logging.warning(f"Unsupported world: {case.field_region}")
        else:
            cases_with_valid_world_ids.append(case)
            world_ids.append(world_map_with_world_ids[case.field_region])
    return world_ids, cases_with_valid_world_ids


def filter_cases(cases: List[QuestionnaireCaseModel]) -> List[QuestionnaireCaseModel]:
    return [
        case
        for case in cases
        if (
            case.telephone_number_1 == ""
            and case.telephone_number_2 == ""
            and case.appointment_telephone_number == ""
            and case.wave == "1"
            and case.priority in ["1", "2", "3", "4", "5"]
            and case.outcome_code in ["", "0", "310"])
    ]


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


def append_uacs_to_retained_case(filtered_cases: List[QuestionnaireCaseModel], case_uac_data: Dict[str, str]) -> List[QuestionnaireCaseModel]:
    cases_with_uacs_appended = []
    for filtered_case in filtered_cases:
        if filtered_case.serial_number not in case_uac_data:
            logging.warning(f"Serial number {filtered_case.serial_number} not found in BUS")
            cases_with_uacs_appended.append(filtered_case)
        else:
            filtered_case.uac_chunks = UacChunks(
                uac1 = case_uac_data[filtered_case.serial_number]["uac_chunks"]["uac1"],
                uac2 = case_uac_data[filtered_case.serial_number]["uac_chunks"]["uac2"],
                uac3 = case_uac_data[filtered_case.serial_number]["uac_chunks"]["uac3"],
            )
            cases_with_uacs_appended.append(filtered_case)
    return cases_with_uacs_appended


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

    cases = questionnaire_service.get_questionnaire_cases(questionnaire_name, config)
    logging.info(f"Retrieved {len(cases)} cases for questionnaire {questionnaire_name}")

    if len(cases) == 0:
        logging.info(f"Exiting as no cases to send for questionnaire {questionnaire_name}")
        return (f"Exiting as no cases to send for questionnaire {questionnaire_name}")

    retained_cases = filter_cases(cases)
    if len(retained_cases) == 0:
        logging.info(f"Exiting as no cases to send after filtering for questionnaire {questionnaire_name}")
        return (f"Exiting as no cases to send after filtering for questionnaire {questionnaire_name}")
    logging.info(f"Retained {len(retained_cases)} cases after filtering")

    questionnaire_uac_data = questionnaire_service.get_questionnaire_uacs(config, questionnaire_name)
    cases_with_uacs_appended = append_uacs_to_retained_case(retained_cases, questionnaire_uac_data)
    logging.info("Finished appending UACs to case data")

    world_ids, cases_with_valid_world_ids = get_world_ids(config, cases_with_uacs_appended)
    logging.info(f"Retrieved world ids")

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
