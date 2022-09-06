from werkzeug.security import generate_password_hash

from app.app import setup_app
from tests.mocks.mock_blaise_service import MockBlaiseService


def before_scenario(context, scenario):
    app = setup_app()
    app.blaise_service = MockBlaiseService()
    context.blaise_service = app.blaise_service

    app.config["user"] = "test_username"
    app.config["password_hash"] = generate_password_hash("test_password")
    context.test_client = app.test_client()
