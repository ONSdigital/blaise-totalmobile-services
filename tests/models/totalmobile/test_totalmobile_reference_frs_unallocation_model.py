import logging

import pytest

from app.exceptions.custom_exceptions import BadReferenceError, MissingReferenceError
from models.common.totalmobile.totalmobile_reference_frs_unallocation_model import (
    TotalmobileReferenceUnallocationFRSModel,
)
from tests.helpers import incoming_request_helper_for_frs_unallocation


def test_frs_unallocation_model_create_reference_returns_an_expected_reference_when_given_questionnaire_name_and_case_id():
    # arrange
    questionnaire_name = "FRS2410A"
    case_id = "90001"
    interviewer_name = "User1"

    frs_reference_model = TotalmobileReferenceUnallocationFRSModel(
        questionnaire_name, case_id, interviewer_name
    )

    # act
    reference = frs_reference_model.create_frs_reference()

    # assert
    assert reference == "FRS2410A.90001"


@pytest.mark.parametrize(
    "questionnaire_name, case_id, interviewer_name",
    [
        ("", "90001", "User1"),
        ("FRS2405A", "", "User1"),
        ("", "", "User1"),
        (None, None, "User1"),
    ],
)
def test_frs_unallocation_model_raises_a_missing_reference_error_when_given_an_invalid_questionnaire_name_and_or_case_id(
    questionnaire_name,
    case_id,
    interviewer_name,
):
    # arrange
    questionnaire_name = questionnaire_name
    case_id = case_id
    interviewer_name = interviewer_name

    # act & assert
    with pytest.raises(MissingReferenceError):
        TotalmobileReferenceUnallocationFRSModel.from_questionnaire_and_case_and_interviewer(
            questionnaire_name, case_id, interviewer_name
        )


def test_frs_unallocation_model_questionnaire_name_and_case_id_and_interviewer_properties_are_set_correctly_when_given_a_valid_incoming_request():
    # arrange
    incoming_frs_case_unallocation_request = (
        incoming_request_helper_for_frs_unallocation.get_frs_case_unallocation_request()
    )
    reference_model = TotalmobileReferenceUnallocationFRSModel.from_request(
        incoming_frs_case_unallocation_request
    )

    # act & assert
    assert reference_model.questionnaire_name == "FRS2405A"
    assert reference_model.case_id == "9001"
    assert reference_model.interviewer_name == "Interviewer1"


def test_frs_unallocation_model_raises_a_missing_reference_error_if_the_request_does_not_have_expected_root_element():
    # arrange
    incoming_frs_case_unallocation_request = {}

    # act & assert
    with pytest.raises(MissingReferenceError):
        TotalmobileReferenceUnallocationFRSModel.from_request(
            incoming_frs_case_unallocation_request
        )


def test_frs_unallocation_model_raises_a_missing_reference_error_if_the_request_does_not_have_expected_questionnaire_case_reference_element():
    # arrange

    incoming_frs_case_unallocation_request = (
        incoming_request_helper_for_frs_unallocation.get_frs_case_unallocation_request_without_reference()
    )

    # act & assert
    with pytest.raises(MissingReferenceError):
        TotalmobileReferenceUnallocationFRSModel.from_request(
            incoming_frs_case_unallocation_request
        )


@pytest.mark.parametrize(
    "reference",
    [" ", "FRS2407B-90001", "FRS2407B:90001", "FRS2407B.", ".90001"],
)
def test_frs_unallocation_model_raises_a_bad_reference_error_if_the_request_does_not_have_a_correctly_formatted_reference(
    reference, caplog
):
    # arrange
    incoming_frs_case_unallocation_request = incoming_request_helper_for_frs_unallocation.get_frs_case_unallocation_request_with_reference_from_param(
        reference=reference
    )

    # act & assert
    with caplog.at_level(logging.ERROR):
        with pytest.raises(BadReferenceError):
            TotalmobileReferenceUnallocationFRSModel.from_request(
                incoming_frs_case_unallocation_request
            )

    assert (
        "root",
        logging.ERROR,
        f"Unique reference appeared to be malformed in the Totalmobile payload (reference='{reference}')",
    ) in caplog.record_tuples


def test_questionnaire_name_and_case_id_properties_are_set_correctly_when_given_a_valid_reference():
    # arrange
    reference = "FRS2410A.200200"

    # act
    reference_model = TotalmobileReferenceUnallocationFRSModel.get_model_from_reference(
        reference, ""
    )

    # assert
    assert reference_model.questionnaire_name == "FRS2410A"
    assert reference_model.case_id == "200200"


def test_frs_unallocation_model_raises_a_missing_reference_error_if_the_request_does_not_have_user_reference_element(
    caplog,
):
    # arrange

    incoming_frs_case_unallocation_request = (
        incoming_request_helper_for_frs_unallocation.get_frs_case_unallocation_request_without_user_reference()
    )

    # act & assert
    with caplog.at_level(logging.ERROR) and pytest.raises(MissingReferenceError):
        TotalmobileReferenceUnallocationFRSModel.get_interviewer_reference_from_incoming_request(
            incoming_frs_case_unallocation_request
        )

    assert (
        "root",
        logging.ERROR,
        "Interviewer Name reference is missing from the Totalmobile payload",
    ) in caplog.record_tuples


def test_frs_unallocation_model_returns_valid_object_if_the_request_is_valid_with_all_references(
    caplog,
):
    # arrange
    questionnaire_name = "FRS2405A"
    case_id = "90001"
    interviewer_name = "User1"

    unallocation_model = TotalmobileReferenceUnallocationFRSModel(
        questionnaire_name, case_id, interviewer_name
    )

    # act
    result = unallocation_model.from_questionnaire_and_case_and_interviewer(
        questionnaire_name, case_id, interviewer_name
    )

    # assert
    assert result.questionnaire_name == "FRS2405A"
    assert result.interviewer_name == "User1"
    assert result.case_id == "90001"
