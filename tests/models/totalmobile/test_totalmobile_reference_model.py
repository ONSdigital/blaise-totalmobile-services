import pytest

from app.exceptions.custom_exceptions import BadReferenceError, MissingReferenceError
from models.totalmobile.totalmobile_reference_model import TotalmobileReferenceModel
from tests.helpers import incoming_request_helper


def test_create_reference_returns_an_expected_reference_when_given_questionnaire_name_and_case_id():
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_id = "90001"

    reference_model = TotalmobileReferenceModel(questionnaire_name, case_id)

    # act
    result = reference_model.create_reference()

    # assert
    assert result == "LMS2101-AA1.90001"


@pytest.mark.parametrize(
    "questionnaire_name, case_id",
    [("", "90001"), ("LMS2101_AA1", ""), ("", ""), (None, None)],
)
def test_model_raises_a_missing_reference_error_when_given_an_invalid_questionnaire_name_and_or_case_id(
    questionnaire_name, case_id
):
    # arrange
    questionnaire_name = questionnaire_name
    case_id = case_id

    # act & assert
    with pytest.raises(MissingReferenceError):
        TotalmobileReferenceModel(questionnaire_name, case_id)


def test_questionnaire_name_and_case_id_properties_are_set_correctly_when_given_a_valid_incoming_request():
    # arrange
    reference = "LMS2101-AA1.90001"
    incoming_case_request = (
        incoming_request_helper.get_populated_update_case_request_for_contact_made(
            reference=reference
        )
    )
    reference_model = TotalmobileReferenceModel(incoming_case_request)

    # act & assert
    assert reference_model.questionnaire_name == "LMS2101_AA1"
    assert reference_model.case_id == "90001"


def test_model_raises_a_missing_reference_error_if_the_request_does_not_have_expected_root_element():
    # arrange
    incoming_case_request = {}

    # act & assert
    with pytest.raises(MissingReferenceError):
        TotalmobileReferenceModel(incoming_case_request)


def test_model_raises_a_missing_reference_error_if_the_request_does_not_have_expected_association_element():
    # arrange

    incoming_case_request = (
        incoming_request_helper.get_update_case_request_without_association_element()
    )

    # act & assert
    with pytest.raises(MissingReferenceError):
        TotalmobileReferenceModel(incoming_case_request)


def test_model_raises_a_missing_reference_error_if_the_request_does_not_have_expected_reference_element():
    # arrange

    incoming_case_request = (
        incoming_request_helper.get_update_case_request_without_reference_element()
    )

    # act & assert
    with pytest.raises(MissingReferenceError):
        TotalmobileReferenceModel(incoming_case_request)


def test_model_raises_a_missing_reference_error_if_the_request_has_an_empty_reference():
    # arrange
    reference = ""
    incoming_case_request = (
        incoming_request_helper.get_populated_update_case_request_for_contact_made(
            reference=reference
        )
    )

    # act & assert
    with pytest.raises(MissingReferenceError):
        TotalmobileReferenceModel(incoming_case_request)


@pytest.mark.parametrize(
    "reference",
    [" ", "LMS2101_AA1-90001", "LMS2101_AA1:90001", "LMS2101_AA1.", ".90001"],
)
def test_model_raises_a_bad_reference_error_if_the_request_does_not_have_a_correctly_formatted_reference(
    reference,
):
    # arrange
    incoming_case_request = (
        incoming_request_helper.get_populated_update_case_request_for_contact_made(
            reference=reference
        )
    )

    # assert
    with pytest.raises(BadReferenceError):
        TotalmobileReferenceModel(incoming_case_request)
