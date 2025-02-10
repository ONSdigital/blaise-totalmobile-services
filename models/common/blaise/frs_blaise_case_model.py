from typing import Dict

from models.common.blaise.blaise_case_model_base import BlaiseCaseModelBase


class FRSBlaiseCaseModel(BlaiseCaseModelBase):
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):
        super().__init__(questionnaire_name, case_data)