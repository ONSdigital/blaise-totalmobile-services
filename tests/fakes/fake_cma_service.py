from collections import defaultdict
from typing import Dict, List

from app.exceptions.custom_exceptions import (
    QuestionnaireCaseDoesNotExistError,
    QuestionnaireCaseError,
)


class FakeCMAService:
    def __init__(self):
        self._questionnaires = {}
        self._errors_when_method_is_called = []
        self._get_cases_call_count = defaultdict(lambda: 0)

    def add_questionnaire(self, questionnaire_name: str) -> None:
        self._questionnaires[questionnaire_name] = {}

    def add_case_to_questionnaire(
        self,
        questionnaire: str,
        case_id: str,
    ) -> None:
        self._assert_questionnaire_exists(questionnaire)

        self._questionnaires[questionnaire][case_id] = {
            "primaryKeyValues": {
                "mainSurveyID": "8d02c802-962d-431a-9e8b-715839442480",
                "id": f"{case_id}",
            },
            "fieldData": {
                "mainSurveyID": "8d02c802-962d-431a-9e8b-715839442480",
                "surveyDisplayName": f"{questionnaire}",
                "id": f"{case_id}",
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

    def _assert_questionnaire_exists(self, questionnaire):
        if not self.questionnaire_exists(questionnaire):
            raise QuestionnaireCaseDoesNotExistError(
                f"Questionnaire '{questionnaire}' does not exist"
            )

    def questionnaire_exists(self, questionnaire_name: str) -> bool:
        if "questionnaire_exists" in self._errors_when_method_is_called:
            raise Exception("questionnaire_exists has errored")

        return questionnaire_name in self._questionnaires

    def get_case(self, questionnaire_name: str, case_id: str) -> Dict[str, str]:
        if "get_case" in self._errors_when_method_is_called:
            raise QuestionnaireCaseError("get_case has errored")

        self._assert_case_exists(questionnaire_name, case_id)
        return self._questionnaires[questionnaire_name][case_id]

    def _assert_case_exists(self, questionnaire_name, case_id):
        self._assert_questionnaire_exists(questionnaire_name)
        if case_id not in self._questionnaires[questionnaire_name]:
            raise QuestionnaireCaseDoesNotExistError(
                f"Case '{case_id}' for questionnaire '{questionnaire_name}' does not exist"
            )

    def get_cases(
        self, questionnaire_name: str
    ) -> List[Dict[str, str]]:
        if "get_cases" in self._errors_when_method_is_called:
            raise Exception("get_case has errored")

        self._assert_questionnaire_exists(questionnaire_name)
        self._get_cases_call_count[questionnaire_name] += 1
        cases = self._questionnaires[questionnaire_name]

        return cases.values()

    def get_cases_call_count(self, questionnaire_name: str) -> int:
        return self._get_cases_call_count[questionnaire_name]
