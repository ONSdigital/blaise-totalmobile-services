from abc import abstractmethod

from models.blaise.questionnaire_uac_model import QuestionnaireUacModel


class UacServiceBase:
    @abstractmethod
    def get_questionnaire_uac_model(
        self, questionnaire_name: str
    ) -> QuestionnaireUacModel:
        pass
