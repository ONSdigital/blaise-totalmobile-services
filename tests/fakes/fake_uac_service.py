from typing import Dict

from models.create.blaise.questionnaire_uac_model import (
    QuestionnaireUacModel,
    UacChunks,
)
from services.create.uac.uac_service_base import UacServiceBase


class FakeUacService(UacServiceBase):
    def __init__(self):
        self._questionnaire_case_uacs: Dict[str, UacChunks] = {}

    def get_questionnaire_uac_model(
        self, questionnaire_name: str
    ) -> QuestionnaireUacModel:
        self._questionnaire_case_uacs[questionnaire_name] = UacChunks(
            uac1="1234", uac2="4567", uac3="6789"
        )

        return QuestionnaireUacModel(
            questionnaire_case_uacs=self._questionnaire_case_uacs
        )
