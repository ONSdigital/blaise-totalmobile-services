from typing import List
from appconfig import Config
from client.bus import BusClient
from models.blaise.uac_model import UacModel


def get_uacs(questionnaire_name: str, config: Config) -> List[UacModel]:
    bus_client = BusClient(config.bus_api_url, config.bus_client_id)

    uac_data_dictionary = bus_client.get_uacs_by_case_id(questionnaire_name)

    return [UacModel.import_uac_data(uac_data_dictionary[uac_data_dictionary_item]) for uac_data_dictionary_item in
            uac_data_dictionary]
