import asyncio
from datetime import timedelta
from typing import Any, Coroutine, Dict, List
from uuid import uuid4

import blaise_restapi
import flask
from google.cloud import tasks_v2
from google.protobuf.duration_pb2 import Duration

from appconfig import Config
from client.optimise import OptimiseClient
from models.totalmobile_job_model import TotalmobileJobModel


def __filter_missing_fields(case, REQUIRED_FIELDS) -> List[str]:
    return list(filter(lambda field: field not in case, REQUIRED_FIELDS))


def validate_request(request_json: Dict) -> None:
    REQUIRED_FIELDS = ["instrument"]
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


def retrieve_case_data(instrument_name: str, config: Config) -> List[Dict[str, str]]:
    restapi_client = blaise_restapi.Client(config.blaise_api_url)

    instrument_data = restapi_client.get_instrument_data(
        config.blaise_server_park,
        instrument_name,
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
            "hOut",
            "srvStat",
            "qiD.Serial_Number",
        ],
    )
    return instrument_data["reportingData"]


def filter_cases(cases: List[Dict[str, str]]) -> List[Dict[str, str]]:
    filtered_cases = []
    for case in cases:
        if case["srvStat"] != "3" and case["hOut"] not in ["360", "390"]:
            filtered_cases.append(case)
    return filtered_cases


def map_totalmobile_job_models(
    cases: List[Dict[str, str]], world_id: str, instrument_name: str
) -> List[TotalmobileJobModel]:
    return [TotalmobileJobModel(instrument_name, world_id, case) for case in cases]


def create_task_name(job_model: TotalmobileJobModel) -> str:
    return (
        f"{job_model.instrument}-{job_model.case['qiD.Serial_Number']}-{str(uuid4())}"
    )


def prepare_tasks(
    job_models: List[TotalmobileJobModel],
) -> List[tasks_v2.CreateTaskRequest]:
    config = Config.from_env()

    duration = Duration()
    duration.FromTimedelta(timedelta(minutes=30))

    task_requests = []
    for job_model in job_models:
        request = tasks_v2.CreateTaskRequest(
            parent=config.totalmobile_jobs_queue_id,
            task=tasks_v2.Task(
                name=f"{config.totalmobile_jobs_queue_id}/tasks/{create_task_name(job_model)}",
                http_request=tasks_v2.HttpRequest(
                    http_method="POST",
                    url=f"https://{config.region}-{config.gcloud_project}.cloudfunctions.net/{config.totalmobile_job_cloud_function}",
                    body=job_model.json().encode(),
                    headers={
                        "Content-Type": "application/json",
                    },
                    oidc_token={"service_account_email": config.cloud_function_sa},
                ),
                dispatch_deadline=duration,
            ),
        )
        task_requests.append(request)
    return task_requests


def create_tasks(
    task_requests: List[tasks_v2.CreateTaskRequest], task_client
) -> List[Coroutine[Any, Any, tasks_v2.Task]]:
    return [task_client.create_task(request) for request in task_requests]


async def run(task_requests: List[tasks_v2.CreateTaskRequest]) -> None:
    task_client = tasks_v2.CloudTasksAsyncClient()
    await asyncio.gather(*create_tasks(task_requests, task_client))


def create_case_tasks_for_instrument(request: flask.Request) -> str:
    config = Config.from_env()

    request_json = request.get_json()
    if request_json is None:
        raise Exception("Function was not triggered by a valid request")
    validate_request(request_json)

    instrument_name = request_json["instrument"]
    world_id = retrieve_world_id(config)

    cases = retrieve_case_data(instrument_name, config)
    filtered_cases = filter_cases(cases)

    totalmobile_job_models = map_totalmobile_job_models(
        filtered_cases, world_id, instrument_name
    )
    task_requests = prepare_tasks(totalmobile_job_models)

    asyncio.run(run(task_requests))
    return "Done"
