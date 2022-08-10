from typing import Optional
from urllib.error import HTTPError
from app.app import app, setup_app
from werkzeug.security import generate_password_hash

setup_app(app)

def before_scenario(context, scenario):
    context.questionnaire_service = MockQuestionnaireService()
    app.questionnaire_service = context.questionnaire_service
    app.config["user"] = "test_username"
    app.config["password_hash"] = generate_password_hash("test_password")
    context.test_client = app.test_client()


class MockQuestionnaireService(): 
    case: Optional[str] = None
    def add_questionnaire_with_case(self, questionnaire, case):
        self.case = f"{questionnaire}.{case}"

    def update_case_field(self, questionnaire_name, case_id, field_id, field_value, config):
        if self.case != f"{questionnaire_name}.{case_id}": 
            raise HTTPError("https://mock-questionnaire-service", 500, "Couldn't find questionnaire case", {}, None)