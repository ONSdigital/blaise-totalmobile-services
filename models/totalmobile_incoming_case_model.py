from dataclasses import dataclass
from typing import Type, TypeVar, Dict

from models.totalmobile_reference_model import TotalmobileReferenceModel

T = TypeVar('T')


@dataclass
class TotalMobileIncomingCaseModel:
    questionnaire_name: str
    case_id: str
    outcome_code: str
    home_phone_number: str
    mobile_phone_number: str

    @staticmethod
    def get_outcome_code(incoming_request: Dict[str, str]) -> str:
        for key, value in incoming_request:
            if key == "Reference" and value == "Primary_Outcome":
                print("yo")
            print(key)
        return incoming_request["result"]["responses"][0]["responses"][1][""]

    @staticmethod
    def get_home_phone_number(incoming_request: Dict[str, str]) -> str:
        return ""

    @staticmethod
    def get_mobile_phone_number(incoming_request: Dict[str, str]) -> str:
        return ""

    @classmethod
    def import_case(cls: Type[T], incoming_request: Dict[str, str]) -> T:
        reference_model = TotalmobileReferenceModel(incoming_request)

        total_mobile_case = TotalMobileIncomingCaseModel(
            questionnaire_name=reference_model.questionnaire_name,
            case_id=reference_model.case_id,
            outcome_code=cls.get_outcome_code(incoming_request),
            home_phone_number=cls.get_home_phone_number(incoming_request),
            mobile_phone_number=cls.get_mobile_phone_number(incoming_request)
        )

        return total_mobile_case
