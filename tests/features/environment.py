from app.app import app, setup_app
from werkzeug.security import generate_password_hash

setup_app(app)

def before_scenario(context, scenario):
    context.questionnaire_service = MockQuestionnaireService()
    app.config["user"] = "test_username"
    app.config["password_hash"] = generate_password_hash("test_password")
    context.test_client = app.test_client()


class MockQuestionnaireService():
    def add_questionnaire_with_case(self, questionnaire, case):
        pass