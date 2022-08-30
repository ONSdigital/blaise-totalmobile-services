from dataclasses import dataclass
from typing import Dict, Type, TypeVar

from app.exceptions.custom_exceptions import InvalidTotalmobileUpdateRequestException
from models.base_model import BaseModel
from models.totalmobile.totalmobile_reference_model import TotalmobileReferenceModel

T = TypeVar("T")


@dataclass
class TotalMobileIncomingUpdateRequestModel(BaseModel):
    questionnaire_name: str
    case_id: str
    outcome_code: int
    contact_name: str
    home_phone_number: str
    mobile_phone_number: str

    @classmethod
    def import_request(cls: Type[T], incoming_request: Dict[str, str]) -> T:
        if not TotalMobileIncomingUpdateRequestModel.dictionary_keys_exist(
            incoming_request, "result", "responses"
        ):
            raise InvalidTotalmobileUpdateRequestException

        reference_model = TotalmobileReferenceModel(incoming_request)
        responses_dictionary = cls.get_dictionary_of_response_elements(
            incoming_request["result"]["responses"]
        )

        total_mobile_case = TotalMobileIncomingUpdateRequestModel(
            questionnaire_name=reference_model.questionnaire_name,
            case_id=reference_model.case_id,
            outcome_code=cls.get_outcome_code(responses_dictionary),
            contact_name=cls.get_contact_name(responses_dictionary),
            home_phone_number=cls.get_home_phone_number(responses_dictionary),
            mobile_phone_number=cls.get_mobile_phone_number(responses_dictionary),
        )

        return total_mobile_case

    @staticmethod
    def get_dictionary_of_response_elements(responses) -> Dict[str, any]:
        response_elements = {}

        if isinstance(responses, list):
            for main_response_item in responses:
                if isinstance(main_response_item, dict):
                    for dict_item in main_response_item.keys():
                        if dict_item == "responses" and isinstance(
                            main_response_item[dict_item], list
                        ):
                            for response_item in main_response_item[dict_item]:
                                response_elements.update(
                                    {
                                        response_item["element"][
                                            "reference"
                                        ]: response_item["value"]
                                    }
                                )

        return response_elements

    @staticmethod
    def get_outcome_code(responses_dictionary: Dict[str, any]) -> int:
        outcome_code = responses_dictionary.get("Primary_Outcome")
        return None if outcome_code is None else int(outcome_code)

    @staticmethod
    def get_contact_name(responses_dictionary: Dict[str, any]) -> str:
        return responses_dictionary.get("Contact_Name")

    @staticmethod
    def get_home_phone_number(responses_dictionary: Dict[str, any]) -> str:
        return responses_dictionary.get("Contact_Tel1")

    @staticmethod
    def get_mobile_phone_number(responses_dictionary: Dict[str, any]) -> str:
        return responses_dictionary.get("Contact_Tel2")
