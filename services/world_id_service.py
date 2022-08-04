from appconfig import Config
from services import totalmobile_restapi_service


def get_world_ids(config: Config):
    worlds = totalmobile_restapi_service.get_worlds(config)
    return {world["identity"]["reference"]: world["id"] for world in worlds}


