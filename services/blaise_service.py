from typing import Dict, List

import blaise_restapi
from urllib3.exceptions import HTTPError

from app.exceptions.custom_exceptions import QuestionnaireCaseDoesNotExistError
from appconfig import Config
from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from services.uac_service import UacService


class BlaiseService:
    def __init__(self, config: Config, uac_service: UacService):
        self._config = config
        self._uac_service = uac_service
        self.restapi_client = blaise_restapi.Client(self._config.blaise_api_url)

    def get_cases(self, questionnaire_name: str) -> List[BlaiseCaseInformationModel]:

        questionnaire_case_data = self.restapi_client.get_questionnaire_data(
            self._config.blaise_server_park,
            questionnaire_name,
            BlaiseCaseInformationModel.required_fields_from_blaise(),
        )

        questionnaire_uac_model = self._uac_service.get_questionnaire_uac_model(
            questionnaire_name
        )

        questionnaire_cases: List[BlaiseCaseInformationModel] = []

        for case_data_item in questionnaire_case_data["reportingData"]:
            case = BlaiseCaseInformationModel.import_case(
                questionnaire_name, case_data_item
            )
            if (
                case.case_id
                and case.case_id
                in questionnaire_uac_model.questionnaire_case_uacs.keys()
            ):
                case.populate_uac_data(
                    questionnaire_uac_model.questionnaire_case_uacs[case.case_id]
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
