from typing import Dict, List

from models.common.blaise.blaise_case_model import BlaiseCase
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)


class BlaiseUpdateCase(BlaiseCase):
    def __init__(self, case_data: Dict[str, str]):
        super().__init__(case_data)

    @staticmethod
    def get_contact_details_fields(
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ):
        fields: Dict[str, str] = {}

        if (
            totalmobile_request.contact_name != ""
            and totalmobile_request.contact_name is not None
        ):
            fields["dMktnName"] = totalmobile_request.contact_name

        if (
            totalmobile_request.home_phone_number != ""
            and totalmobile_request.home_phone_number is not None
        ):
            fields["qDataBag.TelNo"] = totalmobile_request.home_phone_number

        if (
            totalmobile_request.mobile_phone_number != ""
            and totalmobile_request.mobile_phone_number is not None
        ):
            fields["qDataBag.TelNo2"] = totalmobile_request.mobile_phone_number

        if len(fields) == 0:
            return (
                {}
            )  # we dont want to update the knock to nudge indicator as we have no details to update

        return fields

    @staticmethod
    def get_outcome_code_fields(
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ):
        return {
            "hOut": f"{totalmobile_request.outcome_code}",
            "qhAdmin.HOut": f"{totalmobile_request.outcome_code}",
        }

    @staticmethod
    def get_knock_to_nudge_indicator_flag_field():
        return {"DMktnIND": "1"}  # this is a yes/no enum in Blaise. 1 is yes, 2 is no

    @staticmethod
    def get_call_history_record_field(record_number: int):
        return {
            f"catiMana.CatiCall.RegsCalls[{record_number}].WhoMade": "KTN",
            f"catiMana.CatiCall.RegsCalls[{record_number}].DialResult": "5",
        }

    @staticmethod
    def required_fields() -> List:
        return [
            "qiD.Serial_Number",
            "hOut",
            "catiMana.CatiCall.RegsCalls[1].DialResult",
        ]
