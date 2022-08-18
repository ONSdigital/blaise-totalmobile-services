from dataclasses import dataclass
from typing import Type, TypeVar, Dict

from models.totalmobile_reference_model import TotalmobileReferenceModel

T = TypeVar('T')


@dataclass
class TotalMobileIncomingUpdateRequestModel:
    questionnaire_name: str
    case_id: str
    outcome_code: int
    contact_name: str
    home_phone_number: str
    mobile_phone_number: str

    @classmethod
    def import_request(cls: Type[T], incoming_request: Dict[str, str]) -> T:
        reference_model = TotalmobileReferenceModel(incoming_request)

        total_mobile_case = TotalMobileIncomingUpdateRequestModel(
            questionnaire_name=reference_model.questionnaire_name,
            case_id=reference_model.case_id,
            outcome_code=cls.get_outcome_code(incoming_request),
            contact_name=cls.get_contact_name(incoming_request),
            home_phone_number=cls.get_home_phone_number(incoming_request),
            mobile_phone_number=cls.get_mobile_phone_number(incoming_request)
        )

        return total_mobile_case

    @staticmethod
    def get_outcome_code(incoming_request: Dict[str, str]) -> str:
        return int(incoming_request["Result"]["Responses"][0]["Responses"][1]["Value"])

    @staticmethod
    def get_contact_name(incoming_request: Dict[str, str]) -> str:
        return incoming_request["Result"]["Responses"][1]["Responses"][0]["Value"]

    @staticmethod
    def get_home_phone_number(incoming_request: Dict[str, str]) -> str:
        return incoming_request["Result"]["Responses"][1]["Responses"][1]["Value"]

    @staticmethod
    def get_mobile_phone_number(incoming_request: Dict[str, str]) -> str:
        return incoming_request["Result"]["Responses"][1]["Responses"][2]["Value"]
