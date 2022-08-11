import base64
import logging
from behave import given, when, then
from behave.log_capture import LoggingCapture


@given('there is a questionnaire "{questionnaire}" with case "{case}" in Blaise')
def step_impl(context, questionnaire, case):
    context.questionnaire_service.add_questionnaire(questionnaire)
    context.questionnaire_service.add_case_to_questionnaire(questionnaire, case)


@given(u'there is no questionnaire "{questionnaire}" in Blaise')
def step_impl(context, questionnaire):
    #State is reset before every scenario - leaving test empty to ensure no questionnaires are added
    pass

@given(u'there is a questionnaire "{questionnaire}" in Blaise')
def step_impl(context, questionnaire):
    context.questionnaire_service.add_questionnaire(questionnaire)

@given(u'there is no case "{case}" for questionnaire "{questionnaire}" in Blaise')
def step_impl(context, questionnaire, case):
    #State is reset before every scenario - leaving test empty to ensure no questionnaires/cases are added
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
    context.response = response

@when(u'Totalmobile sends an update with missing reference')
def step_impl(context):
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
                },
            }
        },
    )
    context.response = response

@then('"{message}" is logged as an {error_level} message')
def step_impl(context, message, error_level):
    messages = [
        (record.levelno, record.getMessage()) for record in context.log_capture.buffer
    ]
    mappings = {
        "information" : logging.INFO,
        "error" : logging.ERROR
    }
    assert (mappings[error_level], message) in messages, f"Could not find {mappings[error_level]}, {message} in {messages}"

@then(u'a "{response}" response is sent back to Totalmobile')
def step_impl(context, response):
    mappings = {
        "200 OK" : 200,
        "400 Bad Request" : 400,
        "404 Not Found" : 404
    }
    assert context.response.status_code == mappings[response], f"Context response is {context.response.status_code}, response is {mappings[response]}"