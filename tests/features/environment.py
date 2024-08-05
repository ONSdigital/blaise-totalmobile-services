from werkzeug.security import generate_password_hash

from app.app import setup_app
from services.blaise_case_outcome_service import BlaiseCaseOutcomeService
from services.case_filters.case_filter_wave_1 import CaseFilterWave1
from services.case_filters.case_filter_wave_2 import CaseFilterWave2
from services.case_filters.case_filter_wave_3 import CaseFilterWave3
from services.case_filters.case_filter_wave_4 import CaseFilterWave4
from services.case_filters.case_filter_wave_5 import CaseFilterWave5
from services.lms_eligible__case_service import LMSEligibleCaseService
from services.mappers.blaise_lms_case_mapper_service import BlaiseLMSCaseMapperService
from services.questionnaires.lms_questionnaire_service import LMSQuestionnaireService
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
    context.blaise_outcome_service = BlaiseCaseOutcomeService(context.blaise_service)
    context.questionnaire_service = LMSQuestionnaireService(
        blaise_service=app.blaise_service,
        mapper_service=BlaiseLMSCaseMapperService(),
        eligible_case_service=LMSEligibleCaseService(
            wave_filters=[
                CaseFilterWave1(),
                CaseFilterWave2(),
                CaseFilterWave3(),
                CaseFilterWave4(),
                CaseFilterWave5(),
            ]
        ),
        datastore_service=context.datastore_service,
    )

    context.uac_service = FakeUacService()
    context.cloud_task_service = FakeCloudTaskService()

    app.config["user"] = "test_username"
    app.config["password_hash"] = generate_password_hash("test_password")
    context.test_client = app.test_client()
