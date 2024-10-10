import logging
from typing import Any, Dict, Protocol, Union

import blaise_restapi

from app.exceptions.custom_exceptions import CaseAllocationException
from appconfig import Config
from models.create.cma.blaise_cma_frs_create_case_model import FRSCaseModel


class CMA_BlaiseService(Protocol):
    def questionnaire_exists(self, questionnaire_name: str) -> Dict[str, Any]:
        pass

    def case_exist(self, guid: str, case_id: str) -> Union[Dict[str, Any], bool]:
        pass

    def create_frs_case(self, frs_case_model: FRSCaseModel) -> None:
        pass

    def update_frs_case(self, frs_case_model: FRSCaseModel) -> None:
        pass


class CMABlaiseService:
    def __init__(self, config: Config) -> None:
        self._config = config
        self.restapi_client = blaise_restapi.Client(self._config.blaise_api_url)

    def questionnaire_exists(self, questionnaire_name: str) -> Dict[str, Any]:

        return self.restapi_client.get_questionnaire_for_server_park(
            self._config.blaise_server_park, questionnaire_name
        )

    def case_exists(self, guid: str, case_id: str) -> Union[Dict[str, Any], bool]:

        logging.info(f"CMA Server park name found as: {self._config.cma_server_park}")
        logging.info(f"Validating if case exists with id in cma launcher")
        try:
            case = self.restapi_client.get_multikey_case(
                self._config.cma_server_park,
                "CMA_Launcher",
                ["MainSurveyID", "ID"],
                [guid, case_id],
            )
            return case
        except:
            return False

    def create_frs_case(self, frs_case_model: FRSCaseModel):
        try:
            self.restapi_client.create_multikey_case(
                self._config.cma_server_park,
                "CMA_Launcher",
                frs_case_model.key_names,
                frs_case_model.key_values,
                frs_case_model.data_fields,
            )
        except:
            logging.error(
                f"Could not create a case for User {frs_case_model.user} "
                f"within Questionnaire {frs_case_model.questionnaire_name} with case_id {frs_case_model.case_id} in CMA_Launcher..."
            )
            raise CaseAllocationException

    def update_frs_case(self, frs_case_model: FRSCaseModel):
        try:
            self.restapi_client.patch_multikey_case_data(
                self._config.cma_server_park,
                "CMA_Launcher",
                frs_case_model.key_names,
                frs_case_model.key_values,
                frs_case_model.data_fields,
            )
        except:
            logging.error(
                f"Reallocation failed. Failed in allocating Case {frs_case_model.case_id} to User: {frs_case_model.user}"
            )
            raise CaseAllocationException
