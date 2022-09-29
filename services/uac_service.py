from appconfig import Config
from client.bus import BusClient
from models.blaise.questionnaire_uac_model import QuestionnaireUacModel


class UacService:
    def __init__(self, config: Config):
        self._config = config
        self.bus_client = BusClient(
            self._config.bus_api_url, self._config.bus_client_id
        )

    def get_questionnaire_uac_model(
        self, questionnaire_name: str
    ) -> QuestionnaireUacModel:
        uac_data_dictionary = self.bus_client.get_uacs_by_case_id(questionnaire_name)

        return QuestionnaireUacModel.import_uac_data(uac_data_dictionary)
