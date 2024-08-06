from appconfig import Config
from client.bus import BusClient
from models.blaise.questionnaire_uac_model import QuestionnaireUacModel
from services.uac.uac_service_base import UacServiceBase


class UacService(UacServiceBase):
    def __init__(self, config: Config):
        self._config = config

    def get_questionnaire_uac_model(
        self, questionnaire_name: str
    ) -> QuestionnaireUacModel:
        bus_client = BusClient(self._config.bus_api_url, self._config.bus_client_id)
        uac_data_dictionary = bus_client.get_uacs_by_case_id(questionnaire_name)

        return QuestionnaireUacModel.import_uac_data(uac_data_dictionary)
