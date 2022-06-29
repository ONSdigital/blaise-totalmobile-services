from typing import Any, Dict
from unittest import mock

import pytest

from app.utilities.parse_json import (
    __valid_element_dictionary,
    __valid_second_level_responses,
    __valid_telephone_number,
    __valid_top_level_responses,
    __valid_value,
    get_case_details,
    get_reference_number,
    get_telephone_number,
    validate_data,
)


def test_get_case_details_returns_questionnaire_name_and_case_id(
    submit_form_result_request_sample: Dict[str, Any]
):
    # arrange
    sample_json = submit_form_result_request_sample

    # act
    actual_result = get_case_details(sample_json)
    actual_questionnaire_name = actual_result[0]
    actual_case_id = actual_result[1]

    # assert
    assert type(actual_result) == list
    assert actual_result == ["DST2111Z", "1001011"]

    assert type(actual_questionnaire_name) == str
    assert actual_questionnaire_name == "DST2111Z"

    assert type(actual_case_id) == str
    assert actual_case_id == "1001011"


def test_get_case_details_raises_an_error():
    with pytest.raises(Exception):
        get_case_details({})


def test_get_telephone_number_returns_a_telephone_number(
    submit_form_result_request_sample: Dict[str, Any]
):
    assert get_telephone_number(submit_form_result_request_sample) == "07000000000"


def test_get_telephone_number_raises_an_error():
    with pytest.raises(Exception):
        get_telephone_number({})


def test_valid_top_level_responses_is_valid(
    submit_form_result_request_sample: Dict[str, Any]
):
    # act
    actual = __valid_top_level_responses(submit_form_result_request_sample)

    # assert
    assert type(actual) == list
    assert actual == submit_form_result_request_sample["Result"]["Responses"]


def test_valid_top_level_responses_raises_key_error():
    with pytest.raises(KeyError) as err:
        __valid_top_level_responses({})
    assert err.type == KeyError


def test_valid_second_level_responses_is_valid(
    submit_form_result_request_sample: Dict[str, Any]
):
    # arrange
    sample_json = submit_form_result_request_sample
    input = sample_json["Result"]["Responses"][0]
    expected = input["Responses"]

    # act
    actual = __valid_second_level_responses(input)

    # assert
    assert actual == expected


def test_valid_second_level_responses_raises_key_error():
    with pytest.raises(KeyError) as err:
        __valid_second_level_responses({})
    assert err.type == KeyError


def test_valid_element_dictionary_is_valid(
    submit_form_result_request_sample: Dict[str, Any]
):
    # arrange
    sample_json = submit_form_result_request_sample
    input = sample_json["Result"]["Responses"][1]["Responses"][1]
    expected = input["Element"]

    # act
    actual = __valid_element_dictionary(input)

    # assert
    assert actual == expected


def test_valid_element_dictionary_raises_key_error():
    with pytest.raises(KeyError) as err:
        __valid_element_dictionary({})
    assert err.type == KeyError


def test_valid_value_dictionary_is_valid(
    submit_form_result_request_sample: Dict[str, Any]
):
    # arrange
    sample_json = submit_form_result_request_sample
    input = sample_json["Result"]["Responses"][1]["Responses"][1]
    expected = input["Value"]

    # act
    actual = __valid_value(input)

    # assert
    assert actual == expected


def test_valid_value_dictionary_raises_key_error():
    with pytest.raises(KeyError) as err:
        __valid_element_dictionary({})
    assert err.type == KeyError


@pytest.mark.parametrize(
    "phone_number",
    [
        "07123456789",
        "07123 456789",
        "+447123 456789",
        "+44 07123 456789",
        "07123-456-789",
    ],
)
def test_valid_telephone_number_returns_a_valid_telephone_number(phone_number: str):
    assert __valid_telephone_number(phone_number) == "07123456789"


@pytest.mark.parametrize(
    "phone_number",
    [
        "07123 45678",
        "+407123 456789",
        "+4 07123 456789",
        "o7123 45678",
        "HelloWorld",
        "Hello World",
        " ",
        "",
    ],
)
def test_valid_telephone_number_raises_a_type_error(phone_number: str):
    with pytest.raises(TypeError):
        __valid_telephone_number(phone_number)


def test_validata_data_returns_none_when_valid_json_is_passed_to_function(
    submit_form_result_request_sample,
):
    assert validate_data(submit_form_result_request_sample) is None


def test_validate_data_raises_error_when_data_is_empty():
    with pytest.raises(Exception):
        validate_data({})


@pytest.mark.parametrize(
    "sample_json",
    [
        pytest.lazy_fixture("upload_visit_status_request_sample"),
        pytest.lazy_fixture("complete_visit_request_sample"),
    ],
)
def test_get_reference_number_returns_reference_number_when_valid_json_is_passed_to_function(
    sample_json,
):
    assert get_reference_number(sample_json) == "SLC-12345-678-910"


def test_get_reference_number_raises_error_when_data_is_empty():
    with pytest.raises(Exception):
        validate_data({})
