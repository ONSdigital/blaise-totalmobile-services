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


def __map_world_id_to_job_reference(
    totalmobile_service_local: TotalmobileService, world_ids: List[str]
) -> List[Dict[str, str]]:
    list_of_jobs = []
    for world_id in world_ids:
        print(f"Retrieving job references for {world_id}")
        jobs = totalmobile_service_local.get_jobs(world_id)
        print(f"Retrieved {len(jobs)} for {world_id}")
        for job in jobs:
            my_dict = {"world_id": world_id, "reference": job["identity"]["reference"]}
            list_of_jobs.append(my_dict)
    print(
        f"Found a total of {len(list_of_jobs)} Totalmobile jobs across {len(world_ids)} worlds"
    )
    return list_of_jobs


def __delete_job(
    totalmobile_service_local: TotalmobileService, job: Dict[str, str]
) -> None:
    try:
        totalmobile_service_local.delete_job(job["world_id"], job["reference"])
        print(f"Deleted job id {job['reference']} from world {job['world_id']}")
    except Exception as e:
        print(
            f"Could not delete job id {job['reference']} from world {job['world_id']}"
        )
        print(e)


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
        list_of_world_ids_and_job_references = __map_world_id_to_job_reference(
            totalmobile_service, active_world_ids
        )

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(
                __delete_job,
                repeat(totalmobile_service),
                list_of_world_ids_and_job_references,
            )
        print("Done!")
    else:
        print("Did not run 'delete_job' as 'totalmobile_url' was not pointing to 'dev'")
        exit(1)

# TODO:
# add custom exceptions to catch when a case has a status of 'completed'
# map 'Region 1' etc. for logging? - better than '1234 12134 132423' in the logs?
