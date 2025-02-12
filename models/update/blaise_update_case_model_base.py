from abc import abstractmethod
from typing import Dict, List

from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)


class BlaiseUpdateCaseBase:
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):  # type: ignore
        self.questionnaire_name = questionnaire_name
        self._case_data = case_data

    @abstractmethod
    def get_outcome_code_fields(
        self,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ):
        pass

    @abstractmethod
    def required_fields(self) -> List:
        pass
