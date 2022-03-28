from datetime import timedelta
from typing import List, Dict
from google.protobuf.duration_pb2 import Duration
from appconfig import Config
from uuid import uuid4
from models.totalmobile_job_model import TotalmobileJobModel
from google.cloud import tasks_v2
from client.optimise import OptimiseClient


import blaise_restapi
import json


def retrieve_case_data(questionnaire_name: str, config: Config) -> Dict[str, str]:
    restapi_client = blaise_restapi.Client(config.blaise_api_url)

    instrument_data = restapi_client.get_instrument_data(
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
            "hOut",
            "srvStat",
            "qiD.Serial_Number",
        ],
    )
    return instrument_data["reportingData"]


def retrieve_world_id(config: Config) -> str:
    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
    world = "Region 1"
    return optimise_client.get_world(world)["id"]


def create_task_name(job_model: TotalmobileJobModel) -> str:
    return f"{job_model.questionnaire_name}-{job_model.case_data['qiD.Serial_Number']}-{str(uuid4())}"


def map_totalmobile_job_models(cases: Dict[str, str], world_id: str, questionnaire_name: str) -> list[TotalmobileJobModel]:
    jobs = []
    for case in cases:
        jobs.append(TotalmobileJobModel(questionnaire_name, world_id, case))
    return jobs


def prepare_tasks(*job_models: TotalmobileJobModel) -> List[tasks_v2.CreateTaskRequest]:
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
                    body=json.dumps(job_model.case_data).encode(),
                    headers={
                        "Content-Type": "application/json",
                    },
                ),
                dispatch_deadline=duration,
            ),
        )
        task_requests.append(request)
    return task_requests

def create_case_tasks_for_questionnaire(questionnaire_name: str) -> None:
    # TODO
    # filter on business logic for week 1 and week 2 criteria
    # push to queue

    config = Config.from_env()
    world_id = retrieve_world_id(config)

    cases = retrieve_case_data(questionnaire_name, config)
    filtered_cases = cases

    totalmobile_job_models = map_totalmobile_job_models(cases, world_id, questionnaire_name)
    total_mobile_job_tasks = prepare_tasks(totalmobile_job_models)
