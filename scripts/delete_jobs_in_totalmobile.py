from appconfig import Config
from services import totalmobile_service


if __name__ == "__main__":
    world_ids = totalmobile_service.get_worlds(config)

    for world_id in world_ids:
        jobs = totalmobile_service.get_jobs(world_id)
        for job in jobs:
            totalmobile_service.delete_job(job, world_id)
