from typing import Dict, List

from enums.blaise_fields import BlaiseFields
from models.common.blaise.frs_blaise_case_model import FRSBlaiseCaseModel
from models.update.blaise_update_case_model_base import BlaiseUpdateCaseBase
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)


class FRSBlaiseUpdateCase(BlaiseUpdateCaseBase, FRSBlaiseCaseModel):
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):  # type: ignore
        BlaiseUpdateCaseBase.__init__(self, questionnaire_name, case_data)
        FRSBlaiseCaseModel.__init__(self, questionnaire_name, case_data)

    def get_outcome_code_fields(
        self,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ):
        return {
            BlaiseFields.outcome_code: f"{totalmobile_request.outcome_code}",
        }

    @staticmethod
    def get_refusal_reason_fields(
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ):
        return {
            BlaiseFields.outcome_code: f"{totalmobile_request.outcome_code}",
            BlaiseFields.refusal_reason: f"{totalmobile_request.refusal_reason}",
        }

    def required_fields(self) -> List:
        return [
            BlaiseFields.case_id,
            BlaiseFields.outcome_code,
            BlaiseFields.refusal_reason,
        ]
