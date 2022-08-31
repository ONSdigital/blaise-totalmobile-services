from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Type, TypedDict, TypeVar

from app.exceptions.custom_exceptions import InvalidTotalmobileUpdateRequestException
from models.base_model import BaseModel
from models.totalmobile.totalmobile_reference_model import (
    IncomingRequest,
    TotalmobileReferenceModel,
)

T = TypeVar("T", bound="TotalMobileIncomingUpdateRequestModel")


@dataclass
class TotalMobileIncomingUpdateRequestModel(BaseModel):
    questionnaire_name: str
    case_id: str
    outcome_code: Optional[int]
    contact_name: Optional[str]
    home_phone_number: Optional[str]
    mobile_phone_number: Optional[str]

    @classmethod
    def import_request(cls: Type[T], incoming_request: IncomingRequest) -> T:
        if not cls.dictionary_keys_exist(incoming_request, "result", "responses"):
            raise InvalidTotalmobileUpdateRequestException

        reference_model = TotalmobileReferenceModel.from_request(incoming_request)
        responses_dictionary = cls.get_dictionary_of_response_elements(
            incoming_request["result"]["responses"]
        )

        total_mobile_case = cls(
            questionnaire_name=reference_model.questionnaire_name,
            case_id=reference_model.case_id,
            outcome_code=cls.get_outcome_code(responses_dictionary),
            contact_name=cls.get_contact_name(responses_dictionary),
            home_phone_number=cls.get_home_phone_number(responses_dictionary),
            mobile_phone_number=cls.get_mobile_phone_number(responses_dictionary),
        )

        return total_mobile_case

    @staticmethod
    def get_dictionary_of_response_elements(responses) -> Dict[str, Any]:
        if not isinstance(responses, list):
            return {}

        response_elements = {}
        for main_response_item in responses:
            if not isinstance(main_response_item, dict):
                continue

            if "responses" not in main_response_item:
                continue

            for response_item in main_response_item["responses"]:
                response_elements.update(
                    {response_item["element"]["reference"]: response_item["value"]}
                )
        return response_elements

    @staticmethod
    def get_outcome_code(responses_dictionary: Dict[str, Any]) -> Optional[int]:
        outcome_code = responses_dictionary.get("Primary_Outcome")
        return None if outcome_code is None else int(outcome_code)

    @staticmethod
    def get_contact_name(responses_dictionary: Dict[str, Any]) -> Optional[str]:
        return responses_dictionary.get("Contact_Name")

    @staticmethod
    def get_home_phone_number(responses_dictionary: Dict[str, Any]) -> Optional[str]:
        return responses_dictionary.get("Contact_Tel1")

    @staticmethod
    def get_mobile_phone_number(responses_dictionary: Dict[str, Any]) -> Optional[str]:
        return responses_dictionary.get("Contact_Tel2")
