from typing import Dict, List, Optional
from urllib.error import HTTPError
from app.app import setup_app
from werkzeug.security import generate_password_hash

from services.blaise_service import QuestionnaireCaseDoesNotExistError


def before_scenario(context, scenario):
    app = setup_app()
    app.questionnaire_service = MockQuestionnaireService()
    context.questionnaire_service = app.questionnaire_service

    app.config["user"] = "test_username"
    app.config["password_hash"] = generate_password_hash("test_password")
    context.test_client = app.test_client()


class MockQuestionnaireService(): 
    def __init__(self):
        self.questionnaires: Dict[str, List[str]] = {}

    def add_case_to_questionnaire(self, questionnaire, case):
        self.questionnaires[questionnaire].append(case)
    
    def add_questionnaire(self, questionnaire):
        self.questionnaires[questionnaire] = []

    def update_case_field(self, questionnaire_name, case_id, field_id, field_value, config):
        if not (questionnaire_name in self.questionnaires and case_id in self.questionnaires[questionnaire_name]): 
            raise HTTPError("https://mock-questionnaire-service", 500, "Couldn't find questionnaire case", {}, None)
    
    def check_questionnaire_exists(self, questionnaire_name, config):
        return questionnaire_name in self.questionnaires
    
    def get_case(self, questionnaire_name, case_id, config):
        if not (questionnaire_name in self.questionnaires and case_id in self.questionnaires[questionnaire_name]):
            raise QuestionnaireCaseDoesNotExistError()
        return {}