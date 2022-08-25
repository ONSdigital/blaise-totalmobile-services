import pytest

from models.blaise.update_blaise_case_model import UpdateBlaiseCaseModel
from models.totalmobile.totalmobile_incoming_update_request_model import TotalMobileIncomingUpdateRequestModel


def test_import_case_returns_a_populated_model():
    # arrange
    totalmobile_request = TotalMobileIncomingUpdateRequestModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123"
    )

    # act
    result = UpdateBlaiseCaseModel.import_case(totalmobile_request)

    # assert
    assert result.questionnaire_name == "LMS2101_AA1"
    assert result.case_id == "90001"
    assert result.outcome_code == 300
    assert result.contact_name == "Joe Bloggs"
    assert result.home_phone_number == "01234567890"
    assert result.mobile_phone_number == "07123123123"


def test_get_outcome_details_returns_an_expected_dictionary():
    # arrange
    blaise_case = UpdateBlaiseCaseModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123"
    )

    # act
    result = blaise_case.outcome_details()

    # assert
    assert result == {
        "hOut": "300",
        "qhAdmin.HOut": "300",
        "DMktnIND": "1"
    }


def test_get_contact_details_returns_an_expected_dictionary():
    # arrange
    blaise_case = UpdateBlaiseCaseModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123"
    )

    # act
    result = blaise_case.contact_details()

    # assert
    assert result == {
        "dMktnName": "Joe Bloggs",
        "qDataBag.TelNo": "01234567890",
        "qDataBag.TelNo2": "07123123123",
        "DMktnIND": "1"
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_get_contact_details_returns_an_expected_dictionary_if_contact_name_not_provided(test_input):
    # arrange
    blaise_case = UpdateBlaiseCaseModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name=test_input,
        home_phone_number="01234567890",
        mobile_phone_number="07123123123"
    )

    # act
    result = blaise_case.contact_details()

    # assert
    assert result == {
        "qDataBag.TelNo": "01234567890",
        "qDataBag.TelNo2": "07123123123",
        "DMktnIND": "1"
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_get_contact_details_returns_an_expected_dictionary_if_home_number_not_provided(test_input):
    # arrange
    blaise_case = UpdateBlaiseCaseModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number=test_input,
        mobile_phone_number="07123123123"
    )

    # act
    result = blaise_case.contact_details()

    # assert
    assert result == {
        "dMktnName": "Joe Bloggs",
        "qDataBag.TelNo2": "07123123123",
        "DMktnIND": "1"
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_get_contact_details_returns_an_expected_dictionary_if_mobile_number_not_provided(test_input):
    # arrange
    blaise_case = UpdateBlaiseCaseModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number=test_input
    )

    # act
    result = blaise_case.contact_details()

    # assert
    assert result == {
        "dMktnName": "Joe Bloggs",
        "qDataBag.TelNo": "01234567890",
        "DMktnIND": "1"
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_get_contact_details_returns_an_empty_dictionary_if_no_contact_details_provided(test_input):
    # arrange
    blaise_case = UpdateBlaiseCaseModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name=test_input,
        home_phone_number=test_input,
        mobile_phone_number=test_input
    )

    # act
    result = blaise_case.contact_details()

    # assert
    assert result == {
    }
