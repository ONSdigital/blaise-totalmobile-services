import base64
import logging
from behave import given, when, then
from behave.log_capture import LoggingCapture
from app.app import app


@given('there is a questionnaire "{questionnaire}" with case "{case}"')
def step_impl(context, questionnaire, case):
    context.questionnaire_service.add_questionnaire_with_case(questionnaire, case)


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
    assert response.status_code == 500, response.status_code


@then('"{message}" is logged as an information message')
def step_impl(context, message):
    messages = [
        (record.levelno, record.getMessage()) for record in context.log_capture.buffer
    ]
    assert (logging.INFO, message) in messages
