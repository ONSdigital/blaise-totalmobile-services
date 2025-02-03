from abc import abstractmethod
from typing import Dict, List

from models.common.blaise.blaise_case_model import BlaiseCaseModel
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)


class BlaiseUpdateCase(BlaiseCaseModel):
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):  # type: ignore
        super().__init__(questionnaire_name, case_data)

    @abstractmethod
    def get_outcome_code_fields(
        self,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ):
        pass

    @abstractmethod
    def required_fields(self) -> List:
        pass
