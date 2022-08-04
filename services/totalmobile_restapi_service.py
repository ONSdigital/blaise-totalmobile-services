from appconfig import Config
from client.optimise import OptimiseClient


def get_worlds(config: Config):
    optimise_client = OptimiseClient(
        config.totalmobile_url,
        config.totalmobile_instance,
        config.totalmobile_client_id,
        config.totalmobile_client_secret,
    )

    return optimise_client.get_worlds()


