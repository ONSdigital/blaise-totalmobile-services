from typing import Dict, Optional

from enums.blaise_fields import BlaiseFields
from models.common.blaise.blaise_case_model_base import BlaiseCaseModelBase


class FRSBlaiseCaseModel(BlaiseCaseModelBase):
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):
        super().__init__(questionnaire_name, case_data)

    @property
    def refusal_reason(self) -> Optional[str]:
        return str(self._case_data.get(BlaiseFields.refusal_reason, "0"))
