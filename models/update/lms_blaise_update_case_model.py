from typing import Dict, List

from enums.blaise_fields import BlaiseFields
from models.common.blaise.blaise_case_model import BlaiseCaseModel
from models.update.blaise_update_case_model_base import BlaiseUpdateCase
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)


class LMSBlaiseUpdateCase(BlaiseCaseModel):
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):  # type: ignore
        super().__init__(questionnaire_name, case_data)

    @staticmethod
    def get_contact_details_fields(
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ):
        fields: Dict[str, str] = {}

        if (
            totalmobile_request.contact_name != ""
            and totalmobile_request.contact_name is not None
        ):
            fields[
                BlaiseFields.knock_to_nudge_contact_name
            ] = totalmobile_request.contact_name

        if (
            totalmobile_request.home_phone_number != ""
            and totalmobile_request.home_phone_number is not None
        ):
            fields[
                BlaiseFields.telephone_number_1
            ] = totalmobile_request.home_phone_number

        if (
            totalmobile_request.mobile_phone_number != ""
            and totalmobile_request.mobile_phone_number is not None
        ):
            fields[
                BlaiseFields.telephone_number_2
            ] = totalmobile_request.mobile_phone_number

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
            BlaiseFields.outcome_code: f"{totalmobile_request.outcome_code}",
            BlaiseFields.admin_outcome_code: f"{totalmobile_request.outcome_code}",
        }

    @staticmethod
    def get_knock_to_nudge_indicator_flag_field():
        return {
            BlaiseFields.knock_to_nudge_indicator: "1"
        }  # this is a yes/no enum in Blaise. 1 is yes, 2 is no

    @staticmethod
    def get_call_history_record_field(record_number: int):
        return {
            f"catiMana.CatiCall.RegsCalls[{record_number}].WhoMade": "KTN",
            f"catiMana.CatiCall.RegsCalls[{record_number}].DialResult": "5",
        }

    def required_fields(self) -> List:
        return [
            BlaiseFields.case_id,
            BlaiseFields.outcome_code,
            BlaiseFields.call_history,
        ]
