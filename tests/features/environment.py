from typing import Any, Dict, List, Optional

from werkzeug.security import generate_password_hash

from app.app import setup_app
from app.exceptions.custom_exceptions import QuestionnaireDoesNotExistError
from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from services.blaise_service import QuestionnaireCaseDoesNotExistError
from tests.helpers import get_blaise_case_model_helper


def before_scenario(context, scenario):
    app = setup_app()
    app.questionnaire_service = MockQuestionnaireService()
    context.questionnaire_service = app.questionnaire_service

    app.config["user"] = "test_username"
    app.config["password_hash"] = generate_password_hash("test_password")
    context.test_client = app.test_client()


class MockQuestionnaireService:
    def __init__(self):
        self.questionnaires: Dict[str, List[BlaiseCaseInformationModel]] = {}
        self.update_case_request: Optional[Dict[str, Any]] = None

    # functions for setting up data
    def add_case_to_questionnaire(self, questionnaire, case_id):
        case_model = get_blaise_case_model_helper.get_populated_case_model(
            case_id=case_id, questionnaire_name=questionnaire
        )
        self.questionnaires[questionnaire].append(case_model)

    def get_case_from_questionnaire(self, questionnaire, case_id):
        if not (questionnaire in self.questionnaires):
            raise QuestionnaireDoesNotExistError()

        for case in self.questionnaires[questionnaire]:
            if case.case_id == case_id:
                return case

        raise QuestionnaireCaseDoesNotExistError()

    def update_outcome_code_of_case_in_questionnaire(
        self, questionnaire, case_id, outcome_code
    ):
        case_model = self.get_case_from_questionnaire(questionnaire, case_id)
        case_model.outcome_code = int(outcome_code)

    def set_case_has_call_history(self, has_case_history, questionnaire, case_id):
        case_model = self.get_case_from_questionnaire(questionnaire, case_id)
        case_model.has_call_history = has_case_history

    def add_questionnaire(self, questionnaire):
        self.questionnaires[questionnaire] = []

    # service function mocks
    def questionnaire_exists(self, questionnaire_name):
        return questionnaire_name in self.questionnaires

    def get_case(self, questionnaire_name, case_id):
        return self.get_case_from_questionnaire(questionnaire_name, case_id)

    def update_case(self, questionnaire_name, case_id, data_fields):
        self.update_case_request = {
            "data_fields": data_fields,
            "questionnaire_name": questionnaire_name,
            "case_id": case_id,
        }
