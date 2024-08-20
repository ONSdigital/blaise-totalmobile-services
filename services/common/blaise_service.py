from typing import Dict, List, Optional, Protocol

import blaise_restapi
from urllib3.exceptions import HTTPError

from app.exceptions.custom_exceptions import (
    QuestionnaireCaseDoesNotExistError,
    QuestionnaireCaseError,
)
from appconfig import Config


class BlaiseService(Protocol):
    def get_cases(
        self, questionnaire_name: str, required_fields: List[str]
    ) -> List[Dict[str, str]]:
        pass

    def get_case(self, questionnaire_name: str, case_id: str) -> Dict[str, str]:
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

    def get_cases(
        self, questionnaire_name: str, required_fields: List[str]
    ) -> List[Dict[str, str]]:

        questionnaire_case_data = self.restapi_client.get_questionnaire_data(
            self._config.blaise_server_park,
            questionnaire_name,
            required_fields,
        )

        return questionnaire_case_data["reportingData"]

    def get_case(self, questionnaire_name: str, case_id: str) -> Dict[str, str]:

        if not self.case_exists(questionnaire_name, case_id):
            raise QuestionnaireCaseDoesNotExistError()

        try:
            questionnaire_case_data = self.restapi_client.get_case(
                self._config.blaise_server_park, questionnaire_name, case_id
            )
        except HTTPError:
            raise QuestionnaireCaseError()

        return questionnaire_case_data["fieldData"]

    def case_exists(self, questionnaire_name: str, case_id: str) -> bool:

        return self.restapi_client.case_exists_for_questionnaire(
            self._config.blaise_server_park, questionnaire_name, case_id
        )

    def questionnaire_exists(self, questionnaire_name: str) -> bool:

        return self.restapi_client.questionnaire_exists_on_server_park(
            self._config.blaise_server_park, questionnaire_name
        )

    def update_case(
        self,
        questionnaire_name: str,
        case_id: Optional[str],
        data_fields: Dict[str, str],
    ) -> None:

        self.restapi_client.patch_case_data(
            self._config.blaise_server_park, questionnaire_name, case_id, data_fields
        )
