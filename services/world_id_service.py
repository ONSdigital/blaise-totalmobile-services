from appconfig import Config
from models.totalmobile_world_model import TotalmobileWorldModel
from services import totalmobile_restapi_service


def get_world(config: Config):
    worlds = totalmobile_restapi_service.get_worlds(config)
    return TotalmobileWorldModel.import_world_ids(worlds)

