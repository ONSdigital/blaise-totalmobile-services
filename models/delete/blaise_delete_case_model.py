from typing import Dict, List

from models.common.blaise.blaise_case_model import BlaiseCase


class BlaiseDeleteCase(BlaiseCase):
    def __init__(self, case_data: Dict[str, str]):
        super().__init__(case_data)

    @staticmethod
    def required_fields() -> List:
        return [
            "qiD.Serial_Number",
            "hOut",
        ]
