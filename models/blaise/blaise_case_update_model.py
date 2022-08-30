from dataclasses import dataclass
from typing import Type, TypeVar

from models.totalmobile.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)

T = TypeVar("T")


@dataclass
class BlaiseCaseUpdateModel:
    questionnaire_name: str
    case_id: str
    outcome_code: int
    contact_name: str
    home_phone_number: str
    mobile_phone_number: str

    @staticmethod
    def knock_to_nudge_indicator_flag():
        return {"DMktnIND": "1"}  # this is a yes/no enum in Blaise. 1 is yes, 2 is no

    @staticmethod
    def call_history_record(record_number: int):
        return {
            f"catiMana.CatiCall.RegsCalls[{record_number}].WhoMade": "KTN",
            f"catiMana.CatiCall.RegsCalls[{record_number}].DialResult": "5",
        }

    def outcome_details(self):
        return {"hOut": f"{self.outcome_code}", "qhAdmin.HOut": f"{self.outcome_code}"}

    def contact_details(self):
        contact_information = {}

        if self.contact_name != "" and self.contact_name is not None:
            contact_information["dMktnName"] = self.contact_name

        if self.home_phone_number != "" and self.home_phone_number is not None:
            contact_information["qDataBag.TelNo"] = self.home_phone_number

        if self.mobile_phone_number != "" and self.mobile_phone_number is not None:
            contact_information["qDataBag.TelNo2"] = self.mobile_phone_number

        if len(contact_information) == 0:
            return (
                {}
            )  # we dont want to update the knock to nudge indicator as we have no details to update

        return contact_information

    @classmethod
    def import_case(
        cls: Type[T], totalmobile_request: TotalMobileIncomingUpdateRequestModel
    ) -> T:
        return BlaiseCaseUpdateModel(
            questionnaire_name=totalmobile_request.questionnaire_name,
            case_id=totalmobile_request.case_id,
            outcome_code=totalmobile_request.outcome_code,
            contact_name=totalmobile_request.contact_name,
            home_phone_number=totalmobile_request.home_phone_number,
            mobile_phone_number=totalmobile_request.mobile_phone_number,
        )
