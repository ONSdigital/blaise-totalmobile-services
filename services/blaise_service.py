from typing import Dict, List, Protocol

import blaise_restapi
from urllib3.exceptions import HTTPError

from app.exceptions.custom_exceptions import QuestionnaireCaseDoesNotExistError
from appconfig import Config
from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel


class BlaiseService(Protocol):
    def get_cases(self, questionnaire_name: str) -> List[BlaiseCaseInformationModel]:
        pass

    def get_case(
        self, questionnaire_name: str, case_id: str
    ) -> BlaiseCaseInformationModel:
        pass

    def questionnaire_exists(self, questionnaire_name: str) -> bool:
        pass

    def update_case(
        self, questionnaire_name: str, case_id: str, data_fields: Dict[str, str]
    ) -> None:
        pass


class RealBlaiseService:
    def __init__(self, config: Config):
        self._config = config
        self.restapi_client = blaise_restapi.Client(self._config.blaise_api_url)

    def get_cases(self, questionnaire_name: str) -> List[BlaiseCaseInformationModel]:

        questionnaire_case_data = self.restapi_client.get_questionnaire_data(
            self._config.blaise_server_park,
            questionnaire_name,
            BlaiseCaseInformationModel.required_fields_from_blaise(),
        )

        questionnaire_cases: List[BlaiseCaseInformationModel] = []

        for case_data_item in questionnaire_case_data["reportingData"]:
            case = BlaiseCaseInformationModel.import_case(
                questionnaire_name, case_data_item
            )

            questionnaire_cases.append(case)

        return questionnaire_cases

    def get_case(
        self, questionnaire_name: str, case_id: str
    ) -> BlaiseCaseInformationModel:

        try:
            questionnaire_case_data = self.restapi_client.get_case(
                self._config.blaise_server_park, questionnaire_name, case_id
            )
        except HTTPError:
            raise QuestionnaireCaseDoesNotExistError()

        return BlaiseCaseInformationModel.import_case(
            questionnaire_name, questionnaire_case_data["fieldData"]
        )

    def questionnaire_exists(self, questionnaire_name: str) -> bool:

        return self.restapi_client.questionnaire_exists_on_server_park(
            self._config.blaise_server_park, questionnaire_name
        )

    def update_case(
        self, questionnaire_name: str, case_id: str, data_fields: Dict[str, str]
    ) -> None:

        self.restapi_client.patch_case_data(
            self._config.blaise_server_park, questionnaire_name, case_id, data_fields
        )
