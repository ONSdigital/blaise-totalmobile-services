import base64
import logging
from behave import given, when, then
from behave.log_capture import LoggingCapture
from app.app import app


@given('there is a questionnaire "{questionnaire}" with case "{case}"')
def step_impl(context, questionnaire, case):
    context.questionnaire_service.add_questionnaire_with_case(questionnaire, case)


@given(u'there is no questionnaire in Blaise for reference "{questionnaire}"')
def step_impl(context, questionnaire):
    #State is reset before every scenario - leaving test empty to ensure no questionnaires are added
    pass


@when('Totalmobile sends an update for reference "{reference}"')
def step_impl(context, reference):
    valid_credentials = base64.b64encode(b"test_username:test_password").decode("utf-8")
    response = context.test_client.post(
        "/bts/submitformresultrequest",
        headers={"Authorization": f"Basic {valid_credentials}"},
        json={
            "Result": {
                "Responses": [
                    {
                        "Responses": [
                            {
                                "Value": "12345",
                                "Element": {
                                    "Reference": "TelNo",
                                },
                            }
                        ],
                    },
                ],
                "Association": {
                    "Reference": reference,
                },
            }
        },
    )
    assert response.status_code == 200, response.status_code


@then('"{message}" is logged as an {error_level} message')
def step_impl(context, message, error_level):
    messages = [
        (record.levelno, record.getMessage()) for record in context.log_capture.buffer
    ]
    mappings = {
        "information" : logging.INFO,
        "error" : logging.ERROR
    }
    assert (mappings[error_level], message) in messages