# TODO: typing
# TODO: Ensure I'm getting the right TelNo for CaseNo!
# TODO: When tests are running, delete __init__s


def get_telephone_number(input):
    # Get the telephone number from
    # json -> Result -> Responses -> Responses -> Value
    # where
    # json -> Result -> Responses -> Responses -> Element -> Reference
    # is equal to "TelNo"
    for response_list in __valid_top_level_responses(input):
        for response in __valid_second_level_responses(response_list):
            if "TelNo" in __valid_element_dictionary(response).values():
                return __valid_value_dictionary(response)
    raise KeyError("Failed to get telephone number")


def __valid_top_level_responses(input):
    try:
        return input["Result"]["Responses"]
    except Exception as err:
        print("Top level 'Responses' not found in JSON.Result")
        raise err


def __valid_second_level_responses(input):
    try:
        return input["Responses"]
    except Exception as err:
        print("Second level 'Responses' not found in JSON.Result.Responses")
        raise err


def __valid_element_dictionary(input):
    if "Element" not in input:
        print("'Element' not an expected dictionary type in JSON.Result.Responses.Responses")
    return input["Element"]


def __valid_value_dictionary(input):
    if "Value" not in input:
        print("'Value' not found in JSON.Result.Responses.Responses.Element")
    return input["Value"]
