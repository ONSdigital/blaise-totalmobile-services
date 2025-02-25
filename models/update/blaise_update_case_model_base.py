from abc import abstractmethod
from typing import Dict, List

from enums.blaise_fields import BlaiseFields
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)


class BlaiseUpdateCaseBase:
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):  # type: ignore
        self.questionnaire_name = questionnaire_name
        self._case_data = case_data

    @property
    def questionnaire_name(self) -> str:
        return self._questionnaire_name

    @questionnaire_name.setter
    def questionnaire_name(self, value):
        self._questionnaire_name = value

    @staticmethod
    def get_outcome_code_fields(
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ):
        return {
            BlaiseFields.outcome_code: f"{totalmobile_request.outcome_code}",
            BlaiseFields.admin_outcome_code: f"{totalmobile_request.outcome_code}",
        }

    @abstractmethod
    def required_fields(self) -> List:
        pass
