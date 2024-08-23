from typing import Dict, List

from models.common.blaise.blaise_case_model import BlaiseCaseModel


class BlaiseDeleteCase(BlaiseCaseModel):
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):
        super().__init__(questionnaire_name, case_data)

    @staticmethod
    def required_fields() -> List:
        return [
            "qiD.Serial_Number",
            "hOut",
        ]
