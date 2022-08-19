from appconfig import Config
from client.optimise import OptimiseClient
from models.totalmobile_outgoing_job_model import TotalmobileJobModel
from models.totalmobile_world_model import TotalmobileWorldModel
from typing import Dict



def get_worlds(config: Config) -> TotalmobileJobModel:
    optimise_client = get_client(config)
    worlds = optimise_client.get_worlds()
    return TotalmobileWorldModel.import_worlds(worlds)


def create_job(config: Config, job: TotalmobileJobModel):
    optimise_client = get_client(config)
    return optimise_client.create_job(
        job.world_id,
        job.payload
    )


def delete_job(config: Config, world_id: str, job: str):
    optimise_client = get_client(config)
    return optimise_client.delete_job(world_id, job)


def get_jobs(config: Config, world_id: str) -> Dict[str, str]:
    optimise_client = get_client(config)
    return optimise_client.get_jobs(world_id)


def get_client(config: Config):
    return OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )
