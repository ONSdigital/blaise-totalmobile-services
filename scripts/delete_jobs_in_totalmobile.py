from appconfig import Config
from services import totalmobile_service


def delete_all_totalmobile_jobs_in_active_worlds(config: Config) -> str:
    world_ids = totalmobile_service.get_worlds(config)

    for world_id in world_ids:
        jobs = totalmobile_service.get_jobs(config, world_id["id"])
        for job in jobs:
            totalmobile_service.delete_job(config, world_id["id"], job["results"]["identity"]["reference"])
    return "Done"


if __name__ == "__main__":
    config = Config.from_env()
    delete_all_totalmobile_jobs_in_active_worlds(config)