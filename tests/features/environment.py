from werkzeug.security import generate_password_hash

from app.app import setup_app
from services.delete.blaise_case_outcome_service import BlaiseCaseOutcomeService
from services.delete.mappers.blaise_delete_case_imapper_service import (
    BlaiseDeleteCaseMapperService,
)
from tests.fakes.fake_blaise_service import FakeBlaiseService
from tests.fakes.fake_datastore_service import FakeDatastoreService
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService
from tests.fakes.fake_uac_service import FakeUacService


def before_scenario(context, _scenario):
    app = setup_test_app()
    context = setup_context(app, context)


def setup_test_app():
    app = setup_app()

    app.blaise_service = FakeBlaiseService()
    app.uac_service = FakeUacService()
    app.totalmobile_service = FakeTotalmobileService()

    app.config["user"] = "test_username"
    app.config["password_hash"] = generate_password_hash("test_password")

    return app


def setup_context(app, context):
    context = setup_test_services(app, context)
    context.test_client = app.test_client()
    context.app = app

    return context


def setup_test_services(app, context):
    context.blaise_service = app.blaise_service
    context.uac_service = app.uac_service
    context.totalmobile_service = app.totalmobile_service

    context.datastore_service = FakeDatastoreService()
    context.blaise_outcome_service = BlaiseCaseOutcomeService(
        context.blaise_service, BlaiseDeleteCaseMapperService()
    )

    return context
