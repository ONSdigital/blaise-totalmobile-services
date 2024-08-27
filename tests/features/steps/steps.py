# type: ignore[no-redef]

import base64
import json
import logging
from datetime import datetime

from behave import given, then, when

import cloud_functions.delete_totalmobile_jobs_completed_in_blaise
import cloud_functions.delete_totalmobile_jobs_past_field_period
from services.create.create_totalmobile_jobs_service import CreateTotalmobileJobsService
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_1 import (
    CaseFilterWave1,
)
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_2 import (
    CaseFilterWave2,
)
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_3 import (
    CaseFilterWave3,
)
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_4 import (
    CaseFilterWave4,
)
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_5 import (
    CaseFilterWave5,
)
from services.create.questionnaires.eligibility.lms_eligible_case_service import (
    LMSEligibleCaseService,
)
from services.create.questionnaires.lms_questionnaire_service import (
    LMSQuestionnaireService,
)
from tests.fakes.fake_cloud_task_service import FakeCloudTaskService
from tests.helpers import incoming_request_helper
from tests.helpers.date_helper import get_date_as_totalmobile_formatted_string


@given('the survey type is "{survey_type}"')
def step_impl(context, survey_type):
    if survey_type == "LMS":
        context.questionnaire_service = LMSQuestionnaireService(
            blaise_service=context.blaise_service,
            eligible_case_service=LMSEligibleCaseService(
                wave_filters=[
                    CaseFilterWave1(),
                    CaseFilterWave2(),
                    CaseFilterWave3(),
                    CaseFilterWave4(),
                    CaseFilterWave5(),
                ]
            ),
            datastore_service=context.datastore_service,
            uac_service=context.uac_service,
        )
        context.cloud_task_service = FakeCloudTaskService()


@given('there is a questionnaire "{questionnaire}" with case "{case_id}" in Blaise')
def step_impl(context, questionnaire, case_id):
    context.blaise_service.add_questionnaire(questionnaire)
    context.questionnaire_name = questionnaire

    if not context.table:
        context.blaise_service.add_case_to_questionnaire(questionnaire, case_id)
    else:
        data_fields = {row["field_name"]: row["value"] for row in context.table}
        outcome_code = data_fields["outcome_code"]
        context.blaise_service.add_case_to_questionnaire(
            questionnaire, case_id, outcome_code
        )
    context.case_id = case_id


@given('there is a questionnaire "{questionnaire}" in Blaise')
def step_impl(context, questionnaire):
    context.blaise_service.add_questionnaire(questionnaire)


@given("the case has a complete outcome code")
def step_impl(context):
    context.blaise_service.update_outcome_code_of_case_in_questionnaire(
        context.questionnaire_name, context.case_id, "110"
    )


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
    mappings = {
        "200 OK": 200,
        "400 Bad Request": 400,
        "404 Not Found": 404,
        "500 Internal Server Error": 500,
    }
    assert (
        context.response.status_code == mappings[response]
    ), f"Context response is {context.response.status_code}, response is {mappings[response]}"


@given('case "{case_id}" for questionnaire "{questionnaire}" has been completed')
def step_impl(context, case_id, questionnaire):
    case_completed_outcome_code = "110"
    context.blaise_service.add_questionnaire(questionnaire)
    context.blaise_service.add_case_to_questionnaire(questionnaire, case_id)
    context.blaise_service.update_outcome_code_of_case_in_questionnaire(
        questionnaire, case_id, case_completed_outcome_code
    )


@given('case "{case_id}" for questionnaire "{questionnaire}" has not been completed')
def step_impl(context, case_id, questionnaire):
    case_not_completed_outcome_code = "0"
    context.blaise_service.add_questionnaire(questionnaire)
    context.blaise_service.add_case_to_questionnaire(questionnaire, case_id)
    context.blaise_service.update_outcome_code_of_case_in_questionnaire(
        questionnaire, case_id, case_not_completed_outcome_code
    )


@given('there is an incomplete job in Totalmobile with reference "{reference:S}"')
def step_impl(context, reference):
    context.totalmobile_service.add_job(reference, "Region 1")


@given(
    'there is an incomplete job in Totalmobile in region {region} with reference "{reference:S}"'
)
def step_impl(context, region, reference):
    context.totalmobile_service.add_job(reference, region)


@given(
    'there is an incomplete job in Totalmobile with reference "{reference:S}" assigned to "{resource:S}"'
)
def step_impl(context, reference, resource):
    context.totalmobile_service.add_job(
        reference, "Region 1", allocated_resource_reference=resource
    )


@given('job reference "{reference}" has a dueDate that ends in {days} days')
def step_impl(context, reference, days):
    due_date_string = get_date_as_totalmobile_formatted_string(int(days))
    context.totalmobile_service.update_due_date(reference, "Region 1", due_date_string)


@given('case "{case_id}" for questionnaire "{questionnaire}" does not exist in Blaise')
def step_impl(context, case_id, questionnaire):
    context.blaise_service.add_questionnaire(questionnaire)
    context.blaise_service.add_case_to_questionnaire(questionnaire, "0")
    context.blaise_service.update_outcome_code_of_case_in_questionnaire(
        questionnaire, "0", 110
    )


@when("delete_totalmobile_jobs_completed_in_blaise is run")
def step_impl(context):
    cloud_functions.delete_totalmobile_jobs_completed_in_blaise.delete_totalmobile_jobs_completed_in_blaise(
        blaise_outcome_service=context.blaise_outcome_service,
        totalmobile_service=context.totalmobile_service,
    )


@when("delete_totalmobile_jobs_past_field_period is run")
def step_impl(context):
    cloud_functions.delete_totalmobile_jobs_past_field_period.delete_totalmobile_jobs_past_field_period(
        blaise_outcome_service=context.blaise_outcome_service,
        totalmobile_service=context.totalmobile_service,
    )


@then('the Totalmobile job with reference "{reference}" is recalled from "{resource}"')
def step_impl(context, reference, resource):
    assert context.totalmobile_service.job_has_been_recalled(
        resource, reference
    ), f"The job {reference} has not been recalled from {resource}"


@then('the Totalmobile job with reference "{reference}" is deleted')
def step_impl(context, reference):
    assert not context.totalmobile_service.job_exists(
        reference
    ), "The job should not exist in Totalmobile but does"


@then('the Totalmobile job with reference "{reference}" is not deleted')
def step_impl(context, reference):
    assert context.totalmobile_service.job_exists(
        reference
    ), "The job should exist in Totalmobile but does not"


@then(
    '"{reason}" is provided as the reason for deleting job with reference "{reference}"'
)
def step_impl(context, reason, reference):
    assert context.totalmobile_service.deleted_with_reason(
        reference, reason
    ), "The job should have been deleted with the correct reason"


@given("the Totalmobile service errors when retrieving jobs")
def step_impl(context):
    context.totalmobile_service.method_throws_exception("get_jobs_model")


@given("the Totalmobile service errors when deleting jobs")
def step_impl(context):
    context.totalmobile_service.method_throws_exception("delete_job")


@given("the Blaise service errors when retrieving cases")
def step_impl(context):
    context.blaise_service.method_throws_exception("get_cases")


@given("the Blaise service errors when retrieving case")
def step_impl(context):
    context.blaise_service.method_throws_exception("get_case")


@given("there is a {questionnaire_name} with a totalmobile release date of today")
def step_impl(context, questionnaire_name):
    context.blaise_service.add_questionnaire(questionnaire_name)
    context.datastore_service.add_record(questionnaire_name, datetime.today())


@given("case {case_id} for {questionnaire_name} has the following data")
def step_impl(context, case_id, questionnaire_name):
    context.blaise_service.add_questionnaire(questionnaire_name)
    context.questionnaire_name = questionnaire_name

    data_fields: dict = {row["field_name"]: row["value"] for row in context.table}
    outcome_code = int(data_fields["outcome_code"])
    rotational_outcome_code = (
        0 if not data_fields.get("qRotate.RHOut") else int(data_fields["qRotate.RHOut"])
    )
    context.blaise_service.add_case_to_questionnaire(
        questionnaire=questionnaire_name,
        case_id=case_id,
        outcome_code=outcome_code,
        wave=int(data_fields["qDataBag.Wave"]),
        field_case=data_fields["qDataBag.FieldCase"],
        telephone_number_1=data_fields["qDataBag.TelNo"],
        telephone_number_2=data_fields["qDataBag.TelNo2"],
        appointment_telephone_number=data_fields["telNoAppt"],
        field_region=data_fields["qDataBag.FieldRegion"],
        rotational_knock_to_nudge_indicator=data_fields.get("qRotate.RDMktnIND"),
        rotational_outcome_code=rotational_outcome_code,
    )
    context.case_id = case_id


@when("create_totalmobile_jobs is run")
def step_impl(context):
    create_totalmobile_jobs_service = CreateTotalmobileJobsService(
        totalmobile_service=context.totalmobile_service,
        questionnaire_service=context.questionnaire_service,
        cloud_task_service=context.cloud_task_service,
    )

    return create_totalmobile_jobs_service.create_totalmobile_jobs()


@then(
    "a cloud task is created for case {case_id} in questionnaire {questionnaire_name} with the reference {tm_job_ref}"
)
def step_impl(context, case_id, questionnaire_name, tm_job_ref: str):
    task_request_models = context.cloud_task_service.get_task_request_models()

    assert len(task_request_models) == 1
    task_body_json = json.loads(task_request_models[0].task_body)

    assert task_body_json["questionnaire"] == questionnaire_name
    assert task_body_json["case_id"] == case_id
    assert task_body_json["payload"]["identity"]["reference"] == tm_job_ref


@then("no cloud tasks are created")
def step_impl(context):
    task_request_models = context.cloud_task_service.get_task_request_models()

    assert not task_request_models
