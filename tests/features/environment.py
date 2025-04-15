from unittest.mock import MagicMock

from werkzeug.security import generate_password_hash

from app.app import setup_app
from services.case_instruction_service import CaseInstructionService
from services.cma_blaise_service import CMABlaiseService
from services.delete.blaise_case_outcome_service import BlaiseCaseOutcomeService
from services.delete.delete_cma_case_service import DeleteCMACaseService
from tests.fakes.fake_blaise_service import FakeBlaiseService
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
    define_mock_data_for_cma(context)


def configure_app_authentication(app):
    app.config.update(
        {
            "user": "test_username",
            "password_hash": generate_password_hash("test_password"),
        }
    )


def assign_fake_services_to_app(app):
    app.blaise_service = FakeBlaiseService()
    app.uac_service = FakeUacService()
    app.totalmobile_service = FakeTotalmobileService()
    app.cma_blaise_service = MagicMock(spec=CMABlaiseService)


def assign_additional_services_to_context(context):
    context.datastore_service = FakeDatastoreService()
    context.blaise_outcome_service = BlaiseCaseOutcomeService(context.blaise_service)

    context.mock_cma_blaise_service = MagicMock(spec=CMABlaiseService)
    context.mock_delete_service = DeleteCMACaseService(
        cma_blaise_service=context.mock_cma_blaise_service,
        case_instruction_service=MagicMock(spec=CaseInstructionService),
    )


def assign_app_service_to_context(context):
    context.blaise_service = context.app.blaise_service
    context.uac_service = context.app.uac_service
    context.totalmobile_service = context.app.totalmobile_service
    context.mock_cma_blaise_service = context.app.cma_blaise_service


def define_mock_data_for_cma(context):
    context.questionnaire_data = {
        "name": "FRS2504a",
        "id": "8d02c802-962d-431a-9e8b-715839442480",
        "serverParkName": "gusty",
        "installDate": "2025-02-27T11:47:28.1314856+00:00",
        "status": "Active",
        "dataRecordCount": 0,
        "hasData": False,
        "blaiseVersion": "5.14.6.3686",
        "fieldPeriod": "2025-02-01T00:00:00",
        "surveyTla": "FRS",
        "nodes": [{"nodeName": "blaise-gusty-mgmt", "nodeStatus": "Active"}],
    }
    context.cma_case = {
        "primaryKeyValues": {
            "mainSurveyID": "a0e2f264-14e4-4151-b12d-bb3331674624",
            "id": "100010",
        },
        "fieldData": {
            "mainSurveyID": "a0e2f264-14e4-4151-b12d-bb3331674624",
            "surveyDisplayName": "FRS2504a",
            "id": "100010",
            "cmA_Supervisor": "",
            "cmA_ForWhom": "",
            "cmA_InPossession": "",
            "cmA_Location": "SERVER",
            "cmA_Status": "",
            "cmA_CaseClosed": "",
            "cmA_HappeningsStr": "",
            "cmA_HappeningsLbl": "",
            "cmA_HappeningsCod": "",
            "cmA_AllowSpawning": "",
            "cmA_IsDonorCase": "",
            "cmA_GroupType": "",
            "cmA_GroupID": "",
            "cmA_GroupSort": "",
            "cmA_GroupStatus": "",
            "cmA_GroupSummary": "",
            "cmA_SpawnCount": "",
            "cmA_StartDate": "",
            "cmA_EndDate": "11-11-2024",
            "cmA_CmdLineForEdit": "",
            "cmA_PreLoadForEdit": "",
            "cmA_Process.CreatedDT": "",
            "cmA_Process.LastChangedDT": "",
            "cmA_Process.GeoLocation": "",
            "cmA_Process.FirstDownloaded.When": "",
            "cmA_Process.FirstDownloaded.User": "",
            "cmA_Process.FirstUploaded.When": "",
            "cmA_Process.FirstUploaded.User": "",
            "cmA_Process.LastDownloaded.When": "",
            "cmA_Process.LastDownloaded.User": "",
            "cmA_Process.LastUploaded.When": "",
            "cmA_Process.LastUploaded.User": "",
            "cmA_Process.LastAttempt.When": "",
            "cmA_Process.LastAttempt.User": "",
            "cmA_Process.FirstInterviewTime.When": "",
            "cmA_Process.FirstInterviewTime.User": "",
            "cmA_Process.LastInterviewTime.When": "",
            "cmA_Process.LastInterviewTime.User": "",
            "cmA_Process.LastInterviewEndTime": "",
            "cmA_Process.TotalInterviewTimeUsed": "",
            "cmA_Appointment.AppDate": "",
            "cmA_Appointment.AppTime": "",
            "cmA_Appointment.WhenMade.When": "",
            "cmA_Appointment.WhenMade.User": "",
            "cmA_TimeZone": "",
            "cmA_Data.SurveyUploadFailed": "",
            "cmA_Data.Survey": "",
            "cmA_Data.AttemptsCount": "",
            "cmA_Data.Attempts": "",
            "cmA_AttemptsRoute": "",
            "cmA_AttemptsGUID": "",
            "cmA_ContactImage": "",
            "cmA_GeoLocation": "",
            "cmA_ContactInfoGUID": "",
            "cmA_ContactData": "",
            "cmA_DetailsTemplate": "",
            "cmA_CustomUse": "",
            "contactInfoShort": "",
            "lastChangedCI.When": "",
            "lastChangedCI.User": "",
            "caseNote": "",
            "lastChangedNote.When": "",
            "lastChangedNote.User": "",
        },
    }
