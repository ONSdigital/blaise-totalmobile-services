from typing import Dict, Any

import pytest

from app.utilities.parse_json import (get_case_details, get_telephone_number, __valid_top_level_responses, __valid_second_level_responses,
                                      __valid_element_dictionary, __valid_value, __valid_telephone_number)


def test_get_case_details_returns_instrument_name_and_case_id(submit_form_result_request_sample: Dict[str, Any]):
    # arrange
    sample_json = submit_form_result_request_sample

    # act
    actual_result = get_case_details(sample_json)
    actual_instrument_name = actual_result[0]
    actual_case_id = actual_result[1]

    # assert
    assert type(actual_result) == list
    assert actual_result == ['DST2111Z', '1001011']

    assert type(actual_instrument_name) == str
    assert actual_instrument_name == 'DST2111Z'

    assert type(actual_case_id) == str
    assert actual_case_id == '1001011'


def test_get_telephone_number_returns_a_telphone_number(submit_form_result_request_sample: Dict[str, Any]):
    assert get_telephone_number(submit_form_result_request_sample) == "07000000000"


def test_demonstrate_how_to_extract_telephone_number(
        submit_form_result_request_sample: Dict[str, Any]):
    """Demonstrate how to extract telephone number from JSON sample"""
    # arrange
    sample_json = submit_form_result_request_sample

    """loop through JSON sample to find an element reference of 'TelNo'"""
    telephone_reference = sample_json['Result']['Responses'][1]['Responses'][1]['Element']['Reference']

    """Extract the value of that response"""
    telephone_value = sample_json['Result']['Responses'][1]['Responses'][1]['Value']

    # assert
    assert telephone_reference == 'TelNo'
    assert telephone_value == '07000000000'


def test_valid_top_level_responses_is_valid(submit_form_result_request_sample: Dict[str, Any]):
    # act
    actual = __valid_top_level_responses(submit_form_result_request_sample)

    # assert
    assert type(actual) == list
    assert actual == submit_form_result_request_sample["Result"]["Responses"]


def test_valid_top_level_responses_raises_key_error():
    with pytest.raises(KeyError) as err:
        __valid_top_level_responses({})
    assert err.type == KeyError


def test_valid_second_level_responses_is_valid(submit_form_result_request_sample: Dict[str, Any]):
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


def test_valid_element_dictionary_is_valid(submit_form_result_request_sample: Dict[str, Any]):
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


def test_valid_value_dictionary_is_valid(submit_form_result_request_sample: Dict[str, Any]):
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
def test_valid_telephone_number_returns_a_valid_telphone_number(phone_number):
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
        ""
    ],
)
def test_valid_telephone_number_raises_a_type_error(phone_number):
    with pytest.raises(TypeError):
        __valid_telephone_number(phone_number)



    # assert __valid_telephone_number(valid_telephone_number) == valid_telephone_number
    #
    # assert __valid_telephone_number(telephone_number_with_space) == valid_telephone_number
    #
    # with pytest.raises(TypeError):
    #     __valid_telephone_number(telephone_number_is_too_short)
    #
    # with pytest.raises(TypeError):
    #     __valid_telephone_number(telephone_number_is_too_long)

    # with pytest.raises(TypeError):
    #     __valid_telephone_number(telephone_number_is_not_a_number)



def test_json_result_returns_a_dict(submit_form_result_request_sample: Dict[str, Any]):
    """Demonstrate json.Result is dictionary"""
    # arrange
    sample_json = submit_form_result_request_sample

    # assert
    assert type(sample_json["Result"]) == dict


def test_json_result_responses_returns_a_list_of_dictionaries(submit_form_result_request_sample: Dict[str, Any]):
    """Demonstrate json.Result.Responses is a list of dictionaries"""
    # arrange
    sample_json = submit_form_result_request_sample["Result"]["Responses"]

    # assert
    assert type(sample_json) == list
    assert type(sample_json[0]) == dict


def test_json_result_responses_responses_returns_another_list_of_dictionaries(submit_form_result_request_sample: Dict[str, Any]):
    """Demonstrate json.Result.Responses.Responses is a list of dictionaries"""
    # arrange
    sample_json = submit_form_result_request_sample["Result"]["Responses"][0]["Responses"]

    # assert
    assert type(sample_json) == list
    assert type(sample_json[0]) == dict


def test_json_result_responses_responses_element_returns_a_dictionary(
        submit_form_result_request_sample: Dict[str, Any]):
    """Demonstrate json.Result.Responses.Responses.Element is a dictionary"""
    # arrange
    sample_json = submit_form_result_request_sample["Result"]["Responses"][0]["Responses"][0]["Element"]

    # assert
    assert type(sample_json) == dict


def test_json_result_responses_responses_element_reference_is_a_key_of_the_element_dictionary(
        submit_form_result_request_sample: Dict[str, Any]):
    """Demonstrate json.Result.Responses.Responses.Element.Reference is a key"""
    # arrange
    sample_json = submit_form_result_request_sample["Result"]["Responses"][0]["Responses"][0]["Element"]

    # assert
    assert "Reference" in sample_json


def test_whereas_json_result_responses_responses_value_is_a_key_of_the_responses_dictionary(
        submit_form_result_request_sample: Dict[str, Any]):
    """Demonstrate json.Result.Responses.Responses.Value is a key"""
    # arrange
    sample_json = submit_form_result_request_sample["Result"]["Responses"][0]["Responses"][0]

    # assert
    assert "Value" in sample_json
