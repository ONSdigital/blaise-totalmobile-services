from werkzeug.security import generate_password_hash

from app.app import setup_app
from tests.fakes.fake_blaise_service import FakeBlaiseService
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService


def before_scenario(context, scenario):
    app = setup_app()
    app.blaise_service = FakeBlaiseService()
    app.totalmobile_service = FakeTotalmobileService()

    context.blaise_service = app.blaise_service
    context.totalmobile_service = app.totalmobile_service

    app.config["user"] = "test_username"
    app.config["password_hash"] = generate_password_hash("test_password")
    context.test_client = app.test_client()
