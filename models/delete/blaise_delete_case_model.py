from typing import Dict, List

from enums.blaise_fields import BlaiseFields
from models.common.blaise.blaise_case_model import BlaiseCaseModel


class BlaiseDeleteCase(BlaiseCaseModel):
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):
        super().__init__(questionnaire_name, case_data)

    @staticmethod
    def required_fields() -> List:
        return [BlaiseFields.case_id, BlaiseFields.outcome_code]
