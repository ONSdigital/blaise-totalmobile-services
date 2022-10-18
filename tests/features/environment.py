from werkzeug.security import generate_password_hash

from app.app import setup_app
from services.eligible_case_service import EligibleCaseService
from services.questionnaire_service import QuestionnaireService
from tests.fakes.fake_blaise_service import FakeBlaiseService
from tests.fakes.fake_cloud_task_service import FakeCloudTaskService
from tests.fakes.fake_datastore_service import FakeDatastoreService
from tests.fakes.fake_totalmobile_service import FakeTotalmobileService
from tests.fakes.fake_uac_service import FakeUacService


def before_scenario(context, scenario):
    app = setup_app()
    app.blaise_service = FakeBlaiseService()
    app.totalmobile_service = FakeTotalmobileService()

    context.blaise_service = app.blaise_service
    context.totalmobile_service = app.totalmobile_service
    context.datastore_service = FakeDatastoreService()
    context.questionnaire_service = QuestionnaireService(
        app.blaise_service,
        EligibleCaseService(),
        context.datastore_service
    )

    context.uac_service = FakeUacService()
    context.cloud_task_service = FakeCloudTaskService()

    app.config["user"] = "test_username"
    app.config["password_hash"] = generate_password_hash("test_password")
    context.test_client = app.test_client()
