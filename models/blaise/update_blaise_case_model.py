from dataclasses import dataclass
from typing import TypeVar, Type
from models.totalmobile.totalmobile_incoming_update_request_model import TotalMobileIncomingUpdateRequestModel

T = TypeVar('T')


@dataclass
class UpdateBlaiseCaseModel:
    questionnaire_name: str
    case_id: str
    outcome_code: int
    contact_name: str
    home_phone_number: str
    mobile_phone_number: str

    def get_outcome_details(self):
        return {
            "hOut": f"{self.outcome_code}"
        }

    def get_contact_details(self):
        return {
            "dMktnName": self.contact_name,
            "qDataBag.TelNo": self.home_phone_number,
            "qDataBag.TelNo2": self.mobile_phone_number
        }

    @classmethod
    def import_case(cls: Type[T], totalmobile_request: TotalMobileIncomingUpdateRequestModel) -> T:
        return UpdateBlaiseCaseModel(
            questionnaire_name=totalmobile_request.questionnaire_name,
            case_id=totalmobile_request.case_id,
            outcome_code=totalmobile_request.outcome_code,
            contact_name=totalmobile_request.contact_name,
            home_phone_number=totalmobile_request.home_phone_number,
            mobile_phone_number=totalmobile_request.mobile_phone_number
        )
