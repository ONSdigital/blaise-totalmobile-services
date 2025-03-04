from werkzeug.security import generate_password_hash
from app.app import setup_app
from services.delete.blaise_case_outcome_service import BlaiseCaseOutcomeService
from tests.fakes.fake_blaise_service import FakeBlaiseService
from tests.fakes.fake_cma_service import FakeCMAService
from tests.fakes.fake_datastore_service import FakeDatastoreService
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService
from tests.fakes.fake_uac_service import FakeUacService


def before_scenario(context, _scenario):
    """Entrypoint"""
    context.app = setup_test_app()
    setup_context(context)


def setup_test_app():
    app = setup_app()

    assign_fake_services_to_app(app)
    configure_app_authentication(app)

    return app


def setup_context(context):
    context.test_client = context.app.test_client()

    assign_app_service_to_context(context)
    assign_additional_services_to_context(context)


def configure_app_authentication(app):
    app.config.update(
        {
            "user": "test_username",
            "password_hash": generate_password_hash("test_password"),
        }
    )


def assign_fake_services_to_app(app):
    app.blaise_service = FakeBlaiseService()
    app.cma_service = FakeCMAService()
    app.uac_service = FakeUacService()
    app.totalmobile_service = FakeTotalmobileService()


def assign_additional_services_to_context(context):
    context.datastore_service = FakeDatastoreService()
    context.blaise_outcome_service = BlaiseCaseOutcomeService(context.blaise_service)


def assign_app_service_to_context(context):
    context.blaise_service = context.app.blaise_service
    context.cma_service = context.app.cma_service
    context.uac_service = context.app.uac_service
    context.totalmobile_service = context.app.totalmobile_service
