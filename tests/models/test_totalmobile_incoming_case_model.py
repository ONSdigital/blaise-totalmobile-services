import pytest

from app.exceptions.custom_exceptions import MissingReferenceError, BadReferenceError
from models.totalmobile_incoming_case_model import TotalMobileIncomingCaseModel
from tests.helpers import incoming_request_helper


def test_import_case_returns_a_populated_model():
    # arrange
    reference = "LMS2101_AA1.90001"
    outcome_code = "300"
    contact_name= "Duncan Bell"
    home_phone_number = "01234567890"
    mobile_phone_number = "07123123123"

    update_case_request = incoming_request_helper.get_populated_update_case_request(
        reference=reference,
        outcome_code=outcome_code,
        contact_name=contact_name,
        home_phone_number=home_phone_number,
        mobile_phone_number=mobile_phone_number)

    # act
    result = TotalMobileIncomingCaseModel.import_case(update_case_request)

    # assert
    assert result.questionnaire_name == "LMS2101_AA1"
    assert result.case_id == "90001"
    assert result.outcome_code == outcome_code
    assert result.contact_name == contact_name
    assert result.home_phone_number == home_phone_number
    assert result.mobile_phone_number == mobile_phone_number


def test_import_case_raises_a_missing_reference_error_if_the_request_does_not_have_expected_root_element():
    # arrange

    update_case_request = {}

    # assert
    with pytest.raises(MissingReferenceError):
        TotalMobileIncomingCaseModel.import_case(update_case_request)


def test_import_case_raises_a_missing_reference_error_if_the_request_does_not_have_expected_association_element():
    # arrange

    update_case_request = incoming_request_helper.get_update_case_request_without_association_element()

    # assert
    with pytest.raises(MissingReferenceError):
        TotalMobileIncomingCaseModel.import_case(update_case_request)


def test_import_case_raises_a_missing_reference_error_if_the_request_does_not_have_expected_reference_element():
    # arrange

    update_case_request = incoming_request_helper.get_update_case_request_without_reference_element()

    # assert
    with pytest.raises(MissingReferenceError):
        TotalMobileIncomingCaseModel.import_case(update_case_request)


def test_import_case_raises_a_missing_reference_error_if_the_request_has_an_empty_reference():
    # arrange
    reference = ""
    update_case_request = incoming_request_helper.get_populated_update_case_request(reference=reference)

    # assert
    with pytest.raises(MissingReferenceError):
        TotalMobileIncomingCaseModel.import_case(update_case_request)


@pytest.mark.parametrize("reference", [" ", "LMS2101_AA1-90001", "LMS2101_AA1:90001", "LMS2101_AA1.", ".90001"])
def test_import_case_raises_a_bad_reference_error_if_the_request_does_not_have_a_correctly_formatted_reference(reference):
    # arrange
    update_case_request = incoming_request_helper.get_populated_update_case_request(reference=reference)

    # assert
    with pytest.raises(BadReferenceError):
        TotalMobileIncomingCaseModel.import_case(update_case_request)


def test_to_blaise_data_fields_maps_the_correct_fields_and_values():
    # arrange
    totalmobile_case_model = TotalMobileIncomingCaseModel(
        questionnaire_name="LMS2101_AA1",
        case_id="900001",
        outcome_code="110",
        contact_name="John Smith",
        home_phone_number="01234 567890",
        mobile_phone_number="07734 567890"
    )

    # act
    result = totalmobile_case_model.to_blaise_data_fields()

    # assert
    assert result == {
        "hOut": "110",
        "dMktnName": "John Smith",
        "qDataBag.TelNo": "01234 567890",
        "qDataBag.TelNo2": "07734 567890"
    }