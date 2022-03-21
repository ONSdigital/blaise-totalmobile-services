from config.config import Config


def load_config(application):
    application.configuration = Config.from_env()
    application.configuration.log()
