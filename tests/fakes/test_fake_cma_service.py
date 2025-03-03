import pytest

from app.exceptions.custom_exceptions import QuestionnaireCaseDoesNotExistError
from tests.fakes.fake_cma_service import FakeCMAService


@pytest.fixture()
def service() -> FakeCMAService:
    return FakeCMAService()


def test_questionnaire_exists(service: FakeCMAService):
    service.add_questionnaire("FRS11111")
    service.add_questionnaire("FRS22222")

    assert service.questionnaire_exists("FRS11111")
    assert service.questionnaire_exists("FRS22222")
    assert not service.questionnaire_exists("FRS88888")
    assert not service.questionnaire_exists("FRS99999")


def test_add_case_when_questionnaire_does_not_exist(service: FakeCMAService):
    with pytest.raises(
        QuestionnaireCaseDoesNotExistError,
        match=f"Questionnaire 'unknown' does not exist",
    ):
        service.add_case_to_questionnaire("unknown", "12345")


def test_get_case_when_questionnaire_does_not_exist(service: FakeCMAService):
    with pytest.raises(
        QuestionnaireCaseDoesNotExistError,
        match=f"Questionnaire 'unknown' does not exist",
    ):
        service.get_case("unknown", "12345")


def test_get_case_when_case_does_not_exist(service: FakeCMAService):
    service.add_questionnaire("FRS22222")
    with pytest.raises(
        QuestionnaireCaseDoesNotExistError,
        match=f"Case '12345' for questionnaire 'FRS22222' does not exist",
    ):
        service.get_case("FRS22222", "12345")


def test_get_case_when_case_exists(service: FakeCMAService):
    service.add_questionnaire("FRS12345")
    service.add_case_to_questionnaire("FRS12345", "99999")

    case = service.get_case("FRS12345", "99999")
    assert case == {
            "primaryKeyValues": {
                "mainSurveyID": "8d02c802-962d-431a-9e8b-715839442480",
                "id": "99999",
            },
            "fieldData": {
                "mainSurveyID": "8d02c802-962d-431a-9e8b-715839442480",
                "surveyDisplayName": "FRS12345",
                "id": "99999",
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
                "cmA_EndDate": "31-03-2024",
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


def test_get_cases_called_count(service: FakeCMAService):
    # arrange
    service.add_questionnaire("FRS12345")
    service.add_questionnaire("FRS56789")
    service.add_questionnaire("FRS22468")

    # act
    service.get_cases("FRS12345")
    service.get_cases("FRS12345")
    service.get_cases("FRS56789")

    # assert
    assert service.get_cases_call_count("FRS12345") == 2
    assert service.get_cases_call_count("FRS56789") == 1
    assert service.get_cases_call_count("FRS22468") == 0
