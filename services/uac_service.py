from typing import List

from appconfig import Config
from client.bus import BusClient
from models.blaise.uac_model import UacModel


class UacService:
    def __init__(self, config: Config):
        self._config = config

    def get_uacs(self, questionnaire_name: str) -> List[UacModel]:
        bus_client = BusClient(self._config.bus_api_url, self._config.bus_client_id)

        uac_data_dictionary = bus_client.get_uacs_by_case_id(questionnaire_name)

        return [
            UacModel.import_uac_data(uac_data_dictionary[uac_data_dictionary_item])
            for uac_data_dictionary_item in uac_data_dictionary
        ]
