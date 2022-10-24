import concurrent.futures
from itertools import repeat
from typing import Dict, List

from appconfig import Config
from client import OptimiseClient
from services.totalmobile_service import TotalmobileService


def __remove_default_world_id(list_of_active_world_ids: List[str]) -> List[str]:
    print("Removing the default world id from the retrieved world ids")
    default_world_id = "c0ffee00-c8d0-499f-8693-8be6ad1dc6ea"
    return [
        world_id
        for world_id in list_of_active_world_ids
        if world_id != default_world_id
    ]


def __get_active_world_ids(totalmobile_service_local: TotalmobileService) -> List[str]:
    print("Retrieving world ids")
    return __remove_default_world_id(
        totalmobile_service_local.get_world_model().get_available_ids()
    )

def __get_cases(
    totalmobile_service_local: TotalmobileService, world_ids: List[str]
) -> List[Dict[str, str]]:
    list_of_cases = []
    for world_id in world_ids:
        jobs = totalmobile_service_local.get_jobs_filtered(world_id)
        for job in jobs:
            _dict = {job["identity"]["reference"]:job["status"]}
            list_of_cases.append(_dict)
    return list_of_cases

if __name__ == "__main__":
    config = Config.from_env()
    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
    totalmobile_service = TotalmobileService(optimise_client)

    if "dev" in config.totalmobile_url.lower():
        active_world_ids = __get_active_world_ids(totalmobile_service)
        list_of_cases = __get_cases(totalmobile_service, active_world_ids)
        print(len(list_of_cases))
        # for i in list_of_cases:
        #     print(i)