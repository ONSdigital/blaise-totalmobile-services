from flask import Flask

from app.auth import auth
from app.config import Config
from app.endpoints import incoming
from appconfig.config import Config as AppConfig
from services.blaise_service import RealBlaiseService
from services.cma_blaise_service import CMABlaiseService
from services.create.uac.uac_service import UacService
from services.case_instruction_service import CaseInstructionService


def load_config(application):
    config = Config.from_env()
    application.config["user"] = config.user
    application.config["password_hash"] = config.password_hash


def setup_app():
    application = Flask(__name__)
    application.auth = auth
    application.register_blueprint(incoming)
    app_config = AppConfig.from_env()
    application.app_config = app_config
    application.blaise_service = RealBlaiseService(app_config)
    application.cma_blaise_service = CMABlaiseService(app_config)
    application.case_instruction_service = CaseInstructionService(application.cma_blaise_service)
    application.uac_service = UacService(app_config)
    return application
