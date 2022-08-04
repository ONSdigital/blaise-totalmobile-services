from typing import Dict
from appconfig import Config
from client.bus import BusClient


def get_questionnaire_uacs(questionnaire_name: str, config: Config) -> Dict[str, str]:
    bus_client = BusClient(config.bus_api_url, config.bus_client_id)
    return bus_client.get_uacs_by_case_id(questionnaire_name)
