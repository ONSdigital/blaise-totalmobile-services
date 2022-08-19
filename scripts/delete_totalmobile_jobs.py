from appconfig import Config
from concurrent import futures
from services import totalmobile_service
from typing import List, Dict


def remove_default_world_id_from_the_list_of_active_world_ids(list_of_active_world_ids: List[str]) -> List[str]:
    print("Removing the default world id from retrieved world ids")
    default_world_id = "c0ffee00-c8d0-499f-8693-8be6ad1dc6ea"
    return [world_id for world_id in list_of_active_world_ids if world_id != default_world_id]


def get_list_of_active_world_ids(config: Config) -> List[str]:
    print("Retrieving world ids")
    return remove_default_world_id_from_the_list_of_active_world_ids(
        totalmobile_service.get_worlds(config).get_available_ids()
    )


def get_list_of_world_ids_and_job_references(config: Config, world_ids: List[str]) -> List[Dict[str, str]]:
    list_of_jobs = []
    for world_id in world_ids:
        print(f"Retrieving job references for {world_id}")
        jobs = totalmobile_service.get_jobs(config, world_id)
        print(f"Retrieved {len(jobs)} for {world_id}")
        for job in jobs:
            my_dict = {"world_id": world_id, "reference": job["identity"]["reference"]}
            list_of_jobs.append(my_dict)
    print(f"Found a total of {len(list_of_jobs)} jobs across {len(world_ids)} worlds")
    return list_of_jobs


def delete_job(config: Config, job: Dict[str, str]) -> None:
    try:
        print(f"Deleting job id {job['reference']} from world {job['world_id']}")
        totalmobile_service.delete_job(config, job["world_id"], job["reference"])
    except:
        print(
            f"Could not delete job id {job['reference']} from world {job['world_id']} as it has a status of 'completed'"
        )


if __name__ == "__main__":
    config = Config.from_env()
    print(config)

    if config.totalmobile_url.lower().__contains__("dev"):
        list_of_active_world_ids = get_list_of_active_world_ids(config)
        list_of_jobs = get_list_of_world_ids_and_job_references(config, list_of_active_world_ids)

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(delete_job, config, list_of_jobs)
        print("Done!")
    else:
        print("Did not delete Totalmobile jobs as 'Totalmobile URL' was not pointing at 'dev'")
