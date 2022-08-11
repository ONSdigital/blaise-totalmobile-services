import logging
from typing import Any, Dict, Tuple

import phonenumbers

class MissingReferenceError(Exception):
    pass

def get_case_details(input: Dict[str, Any]) -> Tuple[str]:
    print(f"Getting instquestionnairerument name and case id, please wait...")
    if (
        "Result" not in input
        or "Association" not in input["Result"]
        or "Reference" not in input["Result"]["Association"] 
        or input["Result"]["Association"]["Reference"] == ""
    ):
        logging.error("Unique reference is missing from totalmobile payload")
        raise MissingReferenceError()
    try:
        result = input["Result"]["Association"]["Reference"].split(".")
        return result[0],result[1]
    except Exception as err:
        print(f"Failed to get questionnaire name and case id: {err}")
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
        print(
            "'Element' not an expected dictionary type in JSON.Result.Responses.Responses"
        )
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
