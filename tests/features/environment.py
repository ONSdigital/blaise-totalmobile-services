from werkzeug.security import generate_password_hash

from app.app import setup_app
from tests.fakes.fake_blaise_service import FakeBlaiseService


def before_scenario(context, scenario):
    app = setup_app()
    app.blaise_service = FakeBlaiseService()
    context.blaise_service = app.blaise_service

    app.config["user"] = "test_username"
    app.config["password_hash"] = generate_password_hash("test_password")
    context.test_client = app.test_client()
