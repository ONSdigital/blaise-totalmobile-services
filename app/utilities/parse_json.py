import phonenumbers

from typing import Dict, Any


def get_case_details(input: Dict[str, Any]) -> list[str]:
    print(f"Getting instrument name and case id, please wait...")
    try:
        return input["Result"]["Association"]["Reference"].split("-")
    except Exception as err:
        print(f"Failed to get instrument name and case id: {err}")
        raise err


def get_telephone_number(input: Dict[str, Any]) -> str:
    """loop through JSON sample to find a specific response where
    element reference is equal to 'TelNo'
    and extract the telephone value of that specific response"""
    print(f"Getting telephone number, please wait...")
    for response_list in __valid_top_level_responses(input):
        for response in __valid_second_level_responses(response_list):
            if "TelNo" in __valid_element_dictionary(response).values():
                return __valid_value(response)
    raise KeyError("Failed to get telephone number")


def validate_data(data):
    if not data:
        print("Ain't got no data, mate")
        raise ValueError()
    print("We gots data!")


def get_reference_number(data):
    print("This is completely arbitrary data")
    try:
        return data["Identity"]["Reference"]
    except Exception as err:
        print(f"Failed to get reference number: {err}")
        raise err


def __valid_top_level_responses(input: Dict[str, Any]) -> list:
    try:
        return input["Result"]["Responses"]
    except Exception as err:
        print("Top level 'Responses' not found in JSON.Result")
        raise err


def __valid_second_level_responses(input: Dict[str, Any]) -> list:
    try:
        return input["Responses"]
    except Exception as err:
        print("Second level 'Responses' not found in JSON.Result.Responses")
        raise err


def __valid_element_dictionary(input: Dict[str, Any]) -> dict:
    if "Element" not in input:
        print("'Element' not an expected dictionary type in JSON.Result.Responses.Responses")
    return input["Element"]


def __valid_value(input: Dict[str, Any]) -> str:
    if "Value" not in input:
        print("'Value' not found in JSON.Result.Responses.Responses.Element")
    return input["Value"]


def __valid_telephone_number(input: str) -> str:
    telephone_number = input.replace(" ", "")

    try:
        # where "GB" is the region's country code: https://countrycode.org/
        parsed_telephone_number = phonenumbers.parse(telephone_number, "GB")
    except phonenumbers.NumberParseException as err:
        print(f"Could not parse {input}: {err}")
        raise TypeError

    if len(f"0{str(parsed_telephone_number.national_number)}") != 11:
        print(f"{telephone_number} is an invalid length for a telephone number")
        raise TypeError

    if not phonenumbers.is_possible_number(parsed_telephone_number):
        print(f"{telephone_number} is an invalid phone number")
        raise TypeError

    return f"0{parsed_telephone_number.national_number}"
