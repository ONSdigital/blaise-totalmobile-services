from dataclasses import dataclass
from typing import Optional


@dataclass
class BlaiseCaseUpdateModel:
    questionnaire_name: str
    case_id: str
    outcome_code: Optional[int]
    contact_name: Optional[str]
    home_phone_number: Optional[str]
    mobile_phone_number: Optional[str]

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
