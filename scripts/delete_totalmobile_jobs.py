import concurrent.futures
from itertools import repeat
from typing import Dict, List

from factories.service_instance_factory import ServiceInstanceFactory
from services.totalmobile_service import RealTotalmobileService


def __get_active_world_ids(
    totalmobile_service_local: RealTotalmobileService,
) -> List[str]:
    print("Retrieving world IDs")
    return totalmobile_service_local.get_world_model().get_available_ids()


def __map_world_id_to_job_reference(
    totalmobile_service_local: RealTotalmobileService, world_ids: List[str]
) -> List[Dict[str, str]]:
    list_of_jobs = []
    for world_id in world_ids:
        print(f"Retrieving jobs for world ID {world_id}")
        jobs = totalmobile_service_local.get_jobs(world_id)
        print(f"Retrieved {len(jobs)} jobs for world ID {world_id}")
        for job in jobs:
            if job["visitComplete"] is not True:
                my_dict = {
                    "world_id": world_id,
                    "job_reference": job["identity"]["reference"],
                }
                list_of_jobs.append(my_dict)
    print(
        f"Found a total of {len(list_of_jobs)} uncompleted jobs across {len(world_ids)} worlds"
    )
    return list_of_jobs


def __delete_job(
    totalmobile_service_local: RealTotalmobileService, job: Dict[str, str]
) -> None:
    # Exclude deletion from the "default" world
    if job["world_id"] == "c0ffee00-c8d0-499f-8693-8be6ad1dc6ea":
        print(
            f"Skipping deletion for job id {job['job_reference']} from world {job['world_id']}"
        )
        return
    try:
        totalmobile_service_local.delete_job(job["world_id"], job["job_reference"], "0")
        print(f"Deleted job id {job['job_reference']} from world {job['world_id']}")
    except Exception as e:
        print(
            f"Could not delete job id {job['job_reference']} from world {job['world_id']}"
        )
        print(e)


if __name__ == "__main__":
    service_instance_factory = ServiceInstanceFactory()

    totalmobile_service = service_instance_factory.create_totalmobile_service()

    if "dev" in service_instance_factory.config.totalmobile_url.lower():
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
