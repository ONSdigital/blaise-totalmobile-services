from flask import Flask

from app.auth import auth
from app.config import Config
from app.endpoints import incoming
from services.questionnaire_service import QuestionnaireService


def load_config(application):
    config = Config.from_env()
    application.config["user"] = config.user
    application.config["password_hash"] = config.password_hash


def setup_app():
    application = Flask(__name__)
    application.auth = auth
    application.register_blueprint(incoming)
    application.questionnaire_service = QuestionnaireService()
    return application
