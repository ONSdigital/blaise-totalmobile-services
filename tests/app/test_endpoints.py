import json
import logging
from unittest import mock

import blaise_restapi

from app.exceptions.custom_exceptions import (
    CaseAllocationException,
    CaseResetFailedException,
    QuestionnaireDoesNotExistError,
)
from services.case_instruction_service import CMACaseInstructionService


def assert_security_headers_are_present(response):
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["Strict-Transport-Security"] == "max-age=86400"
    assert response.headers["Cache-Control"] == "no-store"
    assert response.headers["Pragma"] == "no-cache"
    assert response.headers["Content-Security-Policy"] == "default-src 'self'"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_health_check(client):
    response = client.get("/bts/V1/health")
    assert json.loads(response.get_data(as_text=True)) == {"healthy": True}
    assert response.status_code == 200
    assert_security_headers_are_present(response)


@mock.patch("app.endpoints.submit_form_result_request_handler")
def test_submit_form_result_request(mock_handler, client, test_auth_header):
    response = client.post("/bts/submitformresultrequest", headers=test_auth_header)
    assert response.status_code == 200
    assert response.text == "ok"
    mock_handler.assert_called()
    assert_security_headers_are_present(response)


def test_submit_form_result_request_returns_401_without_auth(
    client, submit_form_result_request_sample
):

    response = client.post(
        "/bts/submitformresultrequest",
        json=submit_form_result_request_sample,
    )
    assert response.status_code == 401


@mock.patch("app.endpoints.create_visit_request_handler")
def test_create_visit_request(
    mock_handler, client, test_auth_header, create_visit_request_sample
):
    response = client.post(
        "/bts/createvisitrequest",
        json=create_visit_request_sample,
        headers=test_auth_header,
    )
    assert response.status_code == 200
    assert response.text == "ok"
    mock_handler.assert_called()
    assert_security_headers_are_present(response)


@mock.patch("services.create.cma.allocate_cma_case_service")
def test_create_visit_request_returns_404_if_questionnaire_is_not_found(
    service_handler, client, test_auth_header, create_visit_request_sample, caplog
):
    service_handler.create_case.side_effect = QuestionnaireDoesNotExistError
    # act
    with caplog.at_level(logging.ERROR):
        response = client.post(
            "/bts/createvisitrequest",
            json=create_visit_request_sample,
            headers=test_auth_header,
        )

    # assert
    assert response.status_code == 404
    assert response.text == "Questionnaire does not exist in Blaise"
    assert (
        "root",
        logging.ERROR,
        f"Could not find Questionnaire FRS2405A in Blaise",
    ) in caplog.record_tuples


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_for_server_park")
@mock.patch.object(blaise_restapi.Client, "get_multikey_case")
@mock.patch.object(blaise_restapi.Client, "create_multikey_case")
def test_create_visit_request_returns_500_if_multikey_case_creation_fails(
    mock_rest_api_create_case,
    mock_rest_api_get_case,
    mock_rest_api_get_questionnaire,
    mock_frs_questionnaire_from_blaise,
    client,
    test_auth_header,
    create_visit_request_sample,
    caplog,
):
    questionnaire = mock_frs_questionnaire_from_blaise
    mock_rest_api_get_questionnaire.return_value = questionnaire
    mock_rest_api_get_case.return_value = False
    mock_rest_api_create_case.side_effect = ValueError(
        "Some error occured in blaise rest API while creating multikey case!"
    )

    # act
    with caplog.at_level(logging.ERROR):
        response = client.post(
            "/bts/createvisitrequest",
            json=create_visit_request_sample,
            headers=test_auth_header,
        )

    assert response.status_code == 500
    assert response.text == "Case allocation has failed"
    # assert
    assert (
        "root",
        logging.ERROR,
        f"Could not create a case for User Interviewer1 "
        f"within Questionnaire FRS2405A with case_id 500101 in CMA_Launcher...",
    ) in caplog.record_tuples


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_for_server_park")
@mock.patch.object(blaise_restapi.Client, "get_multikey_case")
@mock.patch.object(blaise_restapi.Client, "patch_multikey_case_data")
def test_create_visit_request_returns_500_with_case_reallocation_exception_if_multikey_case_update_fails(
    mock_rest_api_update_case,
    mock_rest_api_get_case,
    mock_rest_api_get_questionnaire,
    mock_frs_questionnaire_from_blaise,
    mock_frs_case_already_set_to_default_from_cma_launcher,
    client,
    test_auth_header,
    create_visit_request_sample,
    caplog,
):
    questionnaire = mock_frs_questionnaire_from_blaise
    mock_rest_api_get_questionnaire.return_value = questionnaire
    mock_rest_api_get_case.return_value = (
        mock_frs_case_already_set_to_default_from_cma_launcher
    )
    mock_rest_api_update_case.side_effect = ValueError(
        "Some error occured in blaise rest API while creating multikey case!"
    )

    # act
    with caplog.at_level(logging.ERROR):
        response = client.post(
            "/bts/createvisitrequest",
            json=create_visit_request_sample,
            headers=test_auth_header,
        )

    assert response.status_code == 500
    assert response.text == "Case reallocation has failed"
    # assert
    assert (
        "root",
        logging.ERROR,
        f"Reallocation failed. Failed in allocating Case 500101 to User: Interviewer1",
    ) in caplog.record_tuples


def test_create_visit_request_returns_401_without_auth(
    client, create_visit_request_sample
):

    response = client.post("/bts/createvisitrequest", json=create_visit_request_sample)
    assert response.status_code == 401


def test_create_visit_request_returns_400_without_user_blaise_logins(
    client, create_visit_request_sample_without_user_blaise_logins, test_auth_header
):

    response = client.post(
        "/bts/createvisitrequest",
        json=create_visit_request_sample_without_user_blaise_logins,
        headers=test_auth_header,
    )
    assert response.status_code == 400
    assert response.text == "Missing/invalid reference in request"


def test_create_visit_request_returns_400_without_reference(
    client, create_visit_request_sample_without_reference, test_auth_header
):

    response = client.post(
        "/bts/createvisitrequest",
        json=create_visit_request_sample_without_reference,
        headers=test_auth_header,
    )
    assert response.status_code == 400
    assert response.text == "Request appears to be malformed"


@mock.patch("app.endpoints.force_recall_visit_request_handler")
def test_force_recall_visit_request(
    mock_handler, client, force_recall_visit_request_payload, test_auth_header
):
    response = client.post(
        "/bts/forcerecallvisitrequest",
        json=force_recall_visit_request_payload,
        headers=test_auth_header,
    )
    assert response.status_code == 200
    assert response.text == "ok"
    mock_handler.assert_called()
    assert_security_headers_are_present(response)


def test_force_recall_visit_request_returns_401_without_auth(
    client, force_recall_visit_request_payload
):
    response = client.post(
        "/bts/forcerecallvisitrequest",
        json=force_recall_visit_request_payload,
    )
    assert response.status_code == 401


def test_force_recall_visit_request_returns_400_with_null_reference(
    client, force_recall_visit_request_payload_with_null_reference, test_auth_header
):

    response = client.post(
        "/bts/forcerecallvisitrequest",
        json=force_recall_visit_request_payload_with_null_reference,
        headers=test_auth_header,
    )
    assert response.status_code == 400
    assert response.text == "Missing/invalid reference in request"


def test_force_recall_visit_request_returns_400_without_reference(
    client, force_recall_visit_request_payload_without_reference, test_auth_header
):

    response = client.post(
        "/bts/forcerecallvisitrequest",
        json=force_recall_visit_request_payload_without_reference,
        headers=test_auth_header,
    )
    assert response.status_code == 400
    assert response.text == "Request appears to be malformed"


@mock.patch("services.create.cma.allocate_cma_case_service")
def test_force_recall_visit_request_returns_404_if_questionnaire_is_not_found(
    service_handler,
    client,
    test_auth_header,
    force_recall_visit_request_payload,
    caplog,
):
    service_handler.unallocate_case.side_effect = QuestionnaireDoesNotExistError
    # act
    with caplog.at_level(logging.ERROR):
        response = client.post(
            "/bts/forcerecallvisitrequest",
            json=force_recall_visit_request_payload,
            headers=test_auth_header,
        )

    # assert
    assert response.status_code == 404
    assert response.text == "Questionnaire does not exist in Blaise"
    assert (
        "root",
        logging.ERROR,
        "Could not find Questionnaire FRS2405A in Blaise",
    ) in caplog.record_tuples


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_for_server_park")
@mock.patch.object(blaise_restapi.Client, "get_multikey_case")
@mock.patch.object(blaise_restapi.Client, "patch_multikey_case_data")
@mock.patch.object(
    CMACaseInstructionService, "create_new_entry_for_special_instructions"
)
def test_force_recall_visit_request_returns_500_if_resetting_existing_case_to_defaults_fail(
    mock_rest_api_update_case,
    mock_rest_api_get_case,
    mock_rest_api_get_questionnaire,
    mock_frs_allocated_case_from_cma_launcher,
    mock_frs_questionnaire_from_blaise,
    client,
    test_auth_header,
    force_recall_visit_request_payload,
    caplog,
):
    questionnaire = mock_frs_questionnaire_from_blaise
    mock_rest_api_get_questionnaire.return_value = questionnaire
    mock_rest_api_get_case.return_value = mock_frs_allocated_case_from_cma_launcher
    mock_rest_api_update_case.side_effect = CaseResetFailedException

    # act
    with caplog.at_level(logging.ERROR):
        response = client.post(
            "/bts/forcerecallvisitrequest",
            json=force_recall_visit_request_payload,
            headers=test_auth_header,
        )

    assert response.status_code == 500
    assert response.text == "Case resest failed for unallocation"


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_for_server_park")
@mock.patch.object(blaise_restapi.Client, "get_multikey_case")
@mock.patch.object(blaise_restapi.Client, "create_multikey_case")
def test_force_recall_visit_request_returns_500_if_special_instruction_entry_creation_fails(
    mock_rest_api_create_case,
    mock_rest_api_get_case,
    mock_rest_api_get_questionnaire,
    mock_frs_allocated_case_from_cma_launcher,
    mock_frs_questionnaire_from_blaise,
    client,
    test_auth_header,
    force_recall_visit_request_payload,
    caplog,
):
    questionnaire = mock_frs_questionnaire_from_blaise
    mock_rest_api_get_questionnaire.return_value = questionnaire
    mock_rest_api_get_case.return_value = mock_frs_allocated_case_from_cma_launcher
    mock_rest_api_create_case.side_effect = CaseAllocationException

    # act
    with caplog.at_level(logging.ERROR):
        response = client.post(
            "/bts/forcerecallvisitrequest",
            json=force_recall_visit_request_payload,
            headers=test_auth_header,
        )

    assert response.status_code == 500
    assert response.text == "Special Instruction entry creation failed for unallocation"
