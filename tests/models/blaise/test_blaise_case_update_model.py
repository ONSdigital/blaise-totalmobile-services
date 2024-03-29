import pytest

from models.blaise.blaise_case_update_model import BlaiseCaseUpdateModel
from models.totalmobile.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)


def test_import_case_returns_a_populated_model():
    # arrange
    totalmobile_request = TotalMobileIncomingUpdateRequestModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123",
    )

    # act
    result = BlaiseCaseUpdateModel.import_case(totalmobile_request)

    # assert
    assert result.questionnaire_name == "LMS2101_AA1"
    assert result.case_id == "90001"
    assert result.outcome_code == 300
    assert result.contact_name == "Joe Bloggs"
    assert result.home_phone_number == "01234567890"
    assert result.mobile_phone_number == "07123123123"


def test_knock_to_nudge_indicator_flag_returns_expected_dictionary():
    # act & assert
    assert BlaiseCaseUpdateModel.knock_to_nudge_indicator_flag() == {"DMktnIND": "1"}


def test_outcome_details_returns_an_expected_dictionary():
    # arrange
    blaise_case = BlaiseCaseUpdateModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123",
    )

    # act
    result = blaise_case.outcome_details()

    # assert
    assert result == {
        "hOut": "300",
        "qhAdmin.HOut": "300",
    }


def test_contact_details_returns_an_expected_dictionary():
    # arrange
    blaise_case = BlaiseCaseUpdateModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123",
    )

    # act
    result = blaise_case.contact_details()

    # assert
    assert result == {
        "dMktnName": "Joe Bloggs",
        "qDataBag.TelNo": "01234567890",
        "qDataBag.TelNo2": "07123123123",
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_contact_details_returns_an_expected_dictionary_if_contact_name_not_provided(
    test_input,
):
    # arrange
    blaise_case = BlaiseCaseUpdateModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name=test_input,
        home_phone_number="01234567890",
        mobile_phone_number="07123123123",
    )

    # act
    result = blaise_case.contact_details()

    # assert
    assert result == {
        "qDataBag.TelNo": "01234567890",
        "qDataBag.TelNo2": "07123123123",
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_contact_details_returns_an_expected_dictionary_if_home_number_not_provided(
    test_input,
):
    # arrange
    blaise_case = BlaiseCaseUpdateModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number=test_input,
        mobile_phone_number="07123123123",
    )

    # act
    result = blaise_case.contact_details()

    # assert
    assert result == {
        "dMktnName": "Joe Bloggs",
        "qDataBag.TelNo2": "07123123123",
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_contact_details_returns_an_expected_dictionary_if_mobile_number_not_provided(
    test_input,
):
    # arrange
    blaise_case = BlaiseCaseUpdateModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number=test_input,
    )

    # act
    result = blaise_case.contact_details()

    # assert
    assert result == {
        "dMktnName": "Joe Bloggs",
        "qDataBag.TelNo": "01234567890",
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_contact_details_returns_an_empty_dictionary_if_no_contact_details_provided(
    test_input,
):
    # arrange
    blaise_case = BlaiseCaseUpdateModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name=test_input,
        home_phone_number=test_input,
        mobile_phone_number=test_input,
    )

    # act
    result = blaise_case.contact_details()

    # assert
    assert result == {}


@pytest.mark.parametrize("record_number", [1, 5])
def test_contact_details_returns_expected_detail_if_record_number_provided(
    record_number,
):
    # act
    result = BlaiseCaseUpdateModel.call_history_record(record_number)

    # assert
    assert result == {
        f"catiMana.CatiCall.RegsCalls[{record_number}].WhoMade": "KTN",
        f"catiMana.CatiCall.RegsCalls[{record_number}].DialResult": "5",
    }
