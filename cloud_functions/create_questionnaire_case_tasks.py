import asyncio
import logging
from typing import Dict, List, Tuple
from uuid import uuid4

import blaise_restapi
import flask

from appconfig import Config
from client.optimise import OptimiseClient
from cloud_functions.logging import setup_logger
from cloud_functions.functions import prepare_tasks, run
from models.totalmobile_job_model import TotalmobileJobModel

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


def retrieve_world_id(config: Config) -> str:
    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
    world = "Region 1"
    return optimise_client.get_world(world)["id"]


def retrieve_case_data(questionnaire_name: str, config: Config) -> List[Dict[str, str]]:
    restapi_client = blaise_restapi.Client(config.blaise_api_url)

    questionnaire_data = restapi_client.get_questionnaire_data(
        config.blaise_server_park,
        questionnaire_name,
        [
            "qDataBag.UPRN_Latitude",
            "qDataBag.UPRN_Longitude",
            "qDataBag.Prem1",
            "qDataBag.Prem2",
            "qDataBag.Prem3",
            "qDataBag.PostTown",
            "qDataBag.PostCode",
            "qDataBag.TelNo",
            "qDataBag.TelNo2",
            "TelNoAppt",
            "hOut",
            "qiD.Serial_Number",
            "qDataBag.Wave",
            "qDataBag.Priority",
            "QDataBag.FieldRegion"
        ],
    )
    return questionnaire_data["reportingData"]


def filter_cases(cases: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return [
        case
        for case in cases
        if (case["qDataBag.TelNo"] == "" and case["qDataBag.TelNo2"] == "" and case["TelNoAppt"] == ""
            and case["qDataBag.Wave"] == "1" and case["qDataBag.Priority"] in ["1","2","3","4","5"] 
            and case["hOut"] in [0, 310]) 
        ]


def get_wave_from_questionnaire_name(questionnaire_name: str):
    if questionnaire_name[0:3] != "LMS":
        raise Exception(f"Invalid format for questionnaire name: {questionnaire_name}")
    return questionnaire_name[-1]


def map_totalmobile_job_models(
    cases: List[Dict[str, str]], world_id: str, questionnaire_name: str
) -> List[TotalmobileJobModel]:
    return [TotalmobileJobModel(questionnaire_name, world_id, case) for case in cases]


def create_task_name(job_model: TotalmobileJobModel) -> str:
    return (
        f"{job_model.questionnaire}-{job_model.case['qiD.Serial_Number']}-{str(uuid4())}"
    )


def run_async_tasks(tasks: List[Tuple[str,str]], queue_id: str, cloud_function: str):
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
    wave = get_wave_from_questionnaire_name(questionnaire_name)
    if wave != "1":
        logging.info("Invalid wave: currently only wave 1 supported")
        raise Exception("Invalid wave: currently only wave 1 supported")

    logging.debug(f"Creating case tasks for questionnaire: {questionnaire_name}")
    world_id = retrieve_world_id(config)
    logging.debug(f"Retrieved world_id: {world_id}")

    cases = retrieve_case_data(questionnaire_name, config)
    logging.debug(f"Retrieved {len(cases)} cases")
    filtered_cases = filter_cases(cases)
    logging.debug(f"Filtered {len(filtered_cases)} cases")

    totalmobile_job_models = map_totalmobile_job_models(
        filtered_cases, world_id, questionnaire_name
    )

    tasks = [
        (create_task_name(job_model), job_model.json().encode())
        for job_model in totalmobile_job_models
    ]

    run_async_tasks(tasks=tasks, queue_id=config.totalmobile_jobs_queue_id, 
    cloud_function_name=config.totalmobile_job_cloud_function)
    logging.info("Finished creating questionnaire case tasks")
    return "Done"
