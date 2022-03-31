# TODO: typing
# TODO: test validations

from app.utilities.parse_json import get_telephone_number


def test_get_telephone_number(submit_form_result_request_sample):
    assert get_telephone_number(submit_form_result_request_sample) == "07000000000"


def test_valid_top_level_responses():
    pass


def test_valid_second_level_responses():
    pass


def test_valid_element_dictionary():
    pass


def test_valid_value_dictionary():
    pass


def test_json_result_is_a_dict(submit_form_result_request_sample):
    # json -> Result
    json_result = get_json_result(submit_form_result_request_sample)
    assert type(json_result) == dict


def test_json_result_responses_is_a_list(submit_form_result_request_sample):
    # json -> Result -> Responses
    json_result_responses = get_json_result_responses(submit_form_result_request_sample)
    assert type(json_result_responses) == list


def test_json_result_responses_responses_is_another_list(submit_form_result_request_sample):
    # json -> Result -> Responses -> Responses
    top_level_responses = get_json_result_responses(submit_form_result_request_sample)
    for second_level_responses in top_level_responses:
        json_result_responses_responses = get_json_result_responses_responses(second_level_responses)
        assert type(json_result_responses_responses) == list


def test_json_result_responses_responses_element_is_a_dictionary(submit_form_result_request_sample):
    # json -> Result -> Responses -> Responses -> Element
    top_level_responses = get_json_result_responses(submit_form_result_request_sample)
    for second_level_responses in top_level_responses:
        json_result_responses_responses = get_json_result_responses_responses(second_level_responses)
        for each_response in json_result_responses_responses:
            json_result_responses_responses_element = get_json_result_responses_responses_element(each_response)
            assert type(json_result_responses_responses_element) == dict


def test_json_result_responses_responses_element_reference_is_a_key_of_the_element_dictionary(submit_form_result_request_sample):
    # json -> Result -> Responses -> Responses -> Element -> Reference
    top_level_responses = get_json_result_responses(submit_form_result_request_sample)
    for second_level_responses in top_level_responses:
        json_result_responses_responses = get_json_result_responses_responses(second_level_responses)
        for each_response in json_result_responses_responses:
            json_result_responses_responses_element = get_json_result_responses_responses_element(each_response)
            json_result_responses_responses_element_reference = get_json_result_responses_responses_element_reference(json_result_responses_responses_element)
            assert json_result_responses_responses_element_reference in json_result_responses_responses_element.values()


def test_whereas_json_result_responses_responses_value_is_a_key(submit_form_result_request_sample):
    # json -> Result -> Responses -> Responses -> Value
    top_level_responses = get_json_result_responses(submit_form_result_request_sample)
    for second_level_responses in top_level_responses:
        json_result_responses_responses = get_json_result_responses_responses(second_level_responses)
        for each_response in json_result_responses_responses:
            assert "Value" in each_response


def get_json_result(input):
    return input["Result"]


def get_json_result_responses(input):
    return input["Result"]["Responses"]


def get_json_result_responses_responses(input):
    return input["Responses"]


def get_json_result_responses_responses_element(input):
    return input["Element"]


def get_json_result_responses_responses_element_reference(input):
    return input["Reference"]


def fancy_print(this_thing_string, this_thing_var):
    return print(f"\n{this_thing_string}: {this_thing_var}")