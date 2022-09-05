from flask import Flask

from app.auth import auth
from app.config import Config
from app.endpoints import incoming
from services import eligible_case_service, uac_service
from services.blaise_service import BlaiseService
from services.questionnaire_service import QuestionnaireService


def load_config(application):
    config = Config.from_env()
    application.config["user"] = config.user
    application.config["password_hash"] = config.password_hash


def setup_app():
    application = Flask(__name__)
    application.auth = auth
    application.register_blueprint(incoming)
    config = Config.from_env()
    application.questionnaire_service = QuestionnaireService(
        config,
        blaise_service=BlaiseService(),
        eligible_case_service=eligible_case_service,
        uac_service=uac_service,
    )
    return application
