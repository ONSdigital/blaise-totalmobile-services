# type: ignore[no-redef]

import base64
import logging

from behave import given, then, when

from tests.helpers import incoming_request_helper


@given('there is a questionnaire "{questionnaire}" with case "{case_id}" in Blaise')
def step_impl(context, questionnaire, case_id):
    context.blaise_service.add_questionnaire(questionnaire)
    context.questionnaire_name = questionnaire

    context.blaise_service.add_case_to_questionnaire(questionnaire, case_id)
    context.case_id = case_id


@given("the case has an outcome code of {outcome_code}")
def step_impl(context, outcome_code):
    context.blaise_service.update_outcome_code_of_case_in_questionnaire(
        context.questionnaire_name, context.case_id, outcome_code
    )


@given("the case has no pre-existing call history")
def step_impl(context):
    context.blaise_service.set_case_has_call_history(
        False, context.questionnaire_name, context.case_id
    )


@given("the case has call history")
def step_impl(context):
    context.blaise_service.set_case_has_call_history(
        True, context.questionnaire_name, context.case_id
    )


@given('there is no questionnaire "{questionnaire}" in Blaise')
def step_impl(context, questionnaire):
    # State is reset before every scenario - leaving test empty to ensure no questionnaires are added
    pass


@given('there is a questionnaire "{questionnaire}" in Blaise')
def step_impl(context, questionnaire):
    context.blaise_service.add_questionnaire(questionnaire)


@given('there is no case "{case_id}" for questionnaire "{questionnaire}" in Blaise')
def step_impl(context, questionnaire, case_id):
    # State is reset before every scenario - leaving test empty to ensure no questionnaires/cases are added
    pass


@when('Totalmobile sends an update for reference "{reference}"')
def step_impl(context, reference):
    valid_credentials = base64.b64encode(b"test_username:test_password").decode("utf-8")
    fields = {}
    if context.table:
        fields = {row["field_name"]: row["value"] for row in context.table}
        fields["outcome_code"] = int(fields["outcome_code"])

    request = (
        incoming_request_helper.get_populated_update_case_request_for_contact_made(
            reference=reference, **fields
        )
    )

    response = context.test_client.post(
        "/bts/submitformresultrequest",
        headers={"Authorization": f"Basic {valid_credentials}"},
        json=request,
    )

    context.response = response


@when(
    'Totalmobile sends an update for reference "{reference}" with an outcome of 300 but no contact information'
)
def step_impl(context, reference):
    valid_credentials = base64.b64encode(b"test_username:test_password").decode("utf-8")
    request = (
        incoming_request_helper.get_populated_update_case_request_for_contact_made(
            reference=reference,
            outcome_code=300,
            contact_name=None,
            home_phone_number=None,
            mobile_phone_number=None,
        )
    )

    response = context.test_client.post(
        "/bts/submitformresultrequest",
        headers={"Authorization": f"Basic {valid_credentials}"},
        json=request,
    )

    context.response = response


@when("Totalmobile sends an update with a missing reference")
def step_impl(context):
    valid_credentials = base64.b64encode(b"test_username:test_password").decode("utf-8")
    response = context.test_client.post(
        "/bts/submitformresultrequest",
        headers={"Authorization": f"Basic {valid_credentials}"},
        json=incoming_request_helper.get_update_case_request_without_reference_element(),
    )
    context.response = response


@when("Totalmobile sends an update with a malformed reference {reference}")
def step_impl(context, reference):
    valid_credentials = base64.b64encode(b"test_username:test_password").decode("utf-8")
    response = context.test_client.post(
        "/bts/submitformresultrequest",
        headers={"Authorization": f"Basic {valid_credentials}"},
        json=incoming_request_helper.get_update_case_request_with_malformed_reference_element(
            reference=reference
        ),
    )
    context.response = response


@when("Totalmobile sends an update with a malformed payload")
def step_impl(context):
    valid_credentials = base64.b64encode(b"test_username:test_password").decode("utf-8")
    response = context.test_client.post(
        "/bts/submitformresultrequest",
        headers={"Authorization": f"Basic {valid_credentials}"},
        json=incoming_request_helper.get_malformed_update_case_request(),
    )
    context.response = response


@then('the case "{case_id}" for questionnaire "{questionnaire}" has been updated with')
def step_impl(context, questionnaire, case_id):
    fields_to_update = {row["field_name"]: row["value"] for row in context.table}
    actual_fields_updated = context.blaise_service.get_updates(questionnaire, case_id)
    for item in fields_to_update.keys():
        assert (
            item in actual_fields_updated
        ), f"{item} should be in {actual_fields_updated}"
        assert actual_fields_updated[item] == fields_to_update[item]


@then(
    'the case "{case_id}" for questionnaire "{questionnaire}" has been updated with call history'
)
def step_impl(context, questionnaire, case_id):
    fields_to_update = {row["field_name"]: row["value"] for row in context.table}
    actual_fields_updated = context.blaise_service.get_updates(questionnaire, case_id)
    for item in fields_to_update.keys():
        assert item in actual_fields_updated
        assert actual_fields_updated[item] == fields_to_update[item]


@then('the case "{case_id}" for questionnaire "{questionnaire}" has not been updated')
def step_impl(context, questionnaire, case_id):
    assert not context.blaise_service.case_has_been_updated(
        questionnaire, case_id
    ), "Update case should not have been called"


@then('"{message}" is logged as an {error_level} message')
def step_impl(context, message, error_level):
    messages = [
        (record.levelno, record.getMessage()) for record in context.log_capture.buffer
    ]
    mappings = {"information": logging.INFO, "error": logging.ERROR}
    assert (
        mappings[error_level],
        message,
    ) in messages, f"Could not find {mappings[error_level]}, {message} in {messages}"


@then('a "{response}" response is sent back to Totalmobile')
def step_impl(context, response):
    mappings = {"200 OK": 200, "400 Bad Request": 400, "404 Not Found": 404}
    assert (
        context.response.status_code == mappings[response]
    ), f"Context response is {context.response.status_code}, response is {mappings[response]}"


@given('a respondent has completed case "{case_id}" online for questionnaire "{questionnaire}"')
def step_impl(context, case_id, questionnaire):
    completed_case = "110"

    context.blaise_service.add_questionnaire(questionnaire)
    context.blaise_service.add_case_to_questionnaire(case_id)
    context.blaise_service.update_outcome_code_of_case_in_questionnaire(questionnaire, case_id, completed_case)


@given('there is a job in Totalmobile with reference "{reference}"')
def step_impl(context, reference):
    context.totalmobile_service.add_job(reference)


@when("delete jobs is run")
def step_impl(context):
    # TODO
    raise NotImplementedError(u'STEP: When delete jobs is run')


@then('the Totalmobile job with reference "{reference}" is deleted')
def step_impl(context, reference):
    assert context.totalmobile_service.job_exists(reference) is False


@then('a "204" response is received from Totalmobile')
def step_impl(context):
    # TODO
    raise NotImplementedError(u'STEP: And a "204" response is received from Totalmobile')