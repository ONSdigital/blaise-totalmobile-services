import asyncio
from appconfig import Config
from services import totalmobile_service
from typing import List

def get_list_of_active_world_ids(config):
    print("Retrieving world ids")
    return totalmobile_service.get_worlds(config).get_available_ids()


def delete_all_totalmobile_jobs_in_active_worlds(config: Config, world_ids: List[str]) -> str:
    for world_id in world_ids:
        if world_id != "c0ffee00-c8d0-499f-8693-8be6ad1dc6ea":
            print(f"Getting jobs for world id {world_id}")
            jobs = totalmobile_service.get_jobs(config, world_id)
            print(f"Found {len(jobs)} jobs for world id {world_id}")
            for job in jobs:
                try:
                    job_ref = job["identity"]["reference"]
                    print(f"Deleting job id {job_ref}")
                    asyncio.run(totalmobile_service.delete_job(config, world_id, job_ref)) # luls
                except:
                    print(f"Error deleting job id {job_ref}")                
    return "Done"


if __name__ == "__main__":
    config = Config.from_env()
    print(config)
    if config.totalmobile_url.lower().__contains__("dev"):
        list_of_active_world_ids = get_list_of_active_world_ids(config)
        delete_all_totalmobile_jobs_in_active_worlds(config, list_of_active_world_ids)
    else:
        print("no m8")
