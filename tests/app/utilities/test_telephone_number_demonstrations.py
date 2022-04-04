"""The following module demonstrates how to extract a telephone number
 from the JSON payload that TMobile posts to Submit Form Result Request"""

from typing import Dict, Any


def test_demonstrate_how_to_extract_telephone_number(
        submit_form_result_request_sample: Dict[str, Any]):
    # arrange
    sample_json = submit_form_result_request_sample

    """Mock-looping through JSON sample to find a specific response..."""
    example_response = sample_json['Result']['Responses'][1]['Responses'][1]

    """...Where that element reference is equal to 'TelNo'..."""
    telephone_reference = example_response['Element']['Reference']
    assert telephone_reference == 'TelNo'

    """...and extract the value of that response"""
    telephone_value = example_response['Value']
    assert telephone_value == '07000000000'


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


def test_json_result_responses_responses_returns_another_list_of_dictionaries(
        submit_form_result_request_sample: Dict[str, Any]):
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
