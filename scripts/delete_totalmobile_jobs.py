from appconfig import Config
from services import totalmobile_service


def get_list_of_active_world_ids(config):
    return totalmobile_service.get_worlds(config).get_available_ids()


def delete_all_totalmobile_jobs_in_active_worlds(config: Config, world_ids: List[str]) -> str:
    for world_id in world_ids:
        jobs = totalmobile_service.get_jobs(config, world_id)
        for job in jobs:
            totalmobile_service.delete_job(config, world_id.id, job["results"][0]["identity"]["reference"])
    return "Done"


if __name__ == "__main__":
    config = Config.from_env()

    list_of_active_world_ids = get_list_of_active_world_ids(config)
    delete_all_totalmobile_jobs_in_active_worlds(config, list_of_active_world_ids)
