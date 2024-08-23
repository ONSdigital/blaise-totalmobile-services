import pytest

from models.update.blaise_update_case_model import BlaiseUpdateCase
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)


@pytest.mark.parametrize(
    "case_id, outcome_code, has_call_history",
    [
        ("10010", 301, False),
        ("9000", 110, True),
        ("1002", 210, False),
    ],
)
def test_populated_update_case_model_has_the_correct_properties(
    case_id: str,
    outcome_code: int,
    has_call_history: bool,
):
    # arrange
    questionnaire_name = "LMS2101_TLR"
    case_data = {
        "qiD.Serial_Number": case_id,
        "hOut": str(outcome_code),
        "catiMana.CatiCall.RegsCalls[1].DialResult": "1" if has_call_history else "",
    }

    # act
    result = BlaiseUpdateCase(questionnaire_name, case_data)

    # assert
    assert result.questionnaire_name == questionnaire_name
    assert result.case_id == case_id
    assert result.outcome_code == outcome_code
    assert result.has_call_history == has_call_history


def test_get_knock_to_nudge_indicator_flag_field_returns_expected_dictionary():
    # arrange
    questionnaire_name = "LMS2101_TLR"
    blaise_case = BlaiseUpdateCase(questionnaire_name, {})

    # act
    result = blaise_case.get_knock_to_nudge_indicator_flag_field()

    # assert
    assert result == {"DMktnIND": "1"}


def test_get_outcome_code_fields_returns_an_expected_dictionary():
    # arrange
    questionnaire_name = "LMS2101_TLR"
    blaise_case = BlaiseUpdateCase(questionnaire_name, {})
    totalmobile_request = TotalMobileIncomingUpdateRequestModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123",
    )

    # act
    result = blaise_case.get_outcome_code_fields(totalmobile_request)

    # assert
    assert result == {
        "hOut": "300",
        "qhAdmin.HOut": "300",
    }


def test_get_contact_details_fields_returns_an_expected_dictionary():
    # arrange
    questionnaire_name = "LMS2101_TLR"
    blaise_case = BlaiseUpdateCase(questionnaire_name, {})
    totalmobile_request = TotalMobileIncomingUpdateRequestModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123",
    )

    # act
    result = blaise_case.get_contact_details_fields(totalmobile_request)

    # assert
    assert result == {
        "dMktnName": "Joe Bloggs",
        "qDataBag.TelNo": "01234567890",
        "qDataBag.TelNo2": "07123123123",
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_get_contact_details_fields_returns_an_expected_dictionary_if_contact_name_not_provided(
    test_input,
):
    # arrange
    questionnaire_name = "LMS2101_TLR"
    blaise_case = BlaiseUpdateCase(questionnaire_name, {})
    totalmobile_request = TotalMobileIncomingUpdateRequestModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name=test_input,
        home_phone_number="01234567890",
        mobile_phone_number="07123123123",
    )

    # act
    result = blaise_case.get_contact_details_fields(totalmobile_request)

    # assert
    assert result == {
        "qDataBag.TelNo": "01234567890",
        "qDataBag.TelNo2": "07123123123",
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_get_contact_details_fields_returns_an_expected_dictionary_if_home_number_not_provided(
    test_input,
):
    # arrange
    questionnaire_name = "LMS2101_TLR"
    blaise_case = BlaiseUpdateCase(questionnaire_name, {})
    totalmobile_request = TotalMobileIncomingUpdateRequestModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number=test_input,
        mobile_phone_number="07123123123",
    )

    # act
    result = blaise_case.get_contact_details_fields(totalmobile_request)

    # assert
    assert result == {
        "dMktnName": "Joe Bloggs",
        "qDataBag.TelNo2": "07123123123",
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_get_contact_details_fields_returns_an_expected_dictionary_if_mobile_number_not_provided(
    test_input,
):
    # arrange
    questionnaire_name = "LMS2101_TLR"
    blaise_case = BlaiseUpdateCase(questionnaire_name, {})
    totalmobile_request = TotalMobileIncomingUpdateRequestModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number=test_input,
    )

    # act
    result = blaise_case.get_contact_details_fields(totalmobile_request)

    # assert
    assert result == {
        "dMktnName": "Joe Bloggs",
        "qDataBag.TelNo": "01234567890",
    }


@pytest.mark.parametrize("test_input", ["", None])
def test_get_contact_details_fields_returns_an_empty_dictionary_if_no_contact_details_provided(
    test_input,
):
    # arrange
    questionnaire_name = "LMS2101_TLR"
    blaise_case = BlaiseUpdateCase(questionnaire_name, {})
    totalmobile_request = TotalMobileIncomingUpdateRequestModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name=test_input,
        home_phone_number=test_input,
        mobile_phone_number=test_input,
    )

    # act
    result = blaise_case.get_contact_details_fields(totalmobile_request)

    # assert
    assert result == {}


@pytest.mark.parametrize("record_number", [1, 5])
def test_get_call_history_record_field_returns_expected_detail_if_record_number_provided(
    record_number,
):
    # arrange
    questionnaire_name = "LMS2101_TLR"
    blaise_case = BlaiseUpdateCase(questionnaire_name, {})

    # act
    result = blaise_case.get_call_history_record_field(record_number)

    # assert
    assert result == {
        f"catiMana.CatiCall.RegsCalls[{record_number}].WhoMade": "KTN",
        f"catiMana.CatiCall.RegsCalls[{record_number}].DialResult": "5",
    }
