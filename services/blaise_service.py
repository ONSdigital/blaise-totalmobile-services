from typing import Dict, List

import blaise_restapi
from urllib3.exceptions import HTTPError

from app.exceptions.custom_exceptions import QuestionnaireCaseDoesNotExistError
from appconfig import Config
from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel


class BlaiseService:
    required_fields_from_blaise = [
        "qiD.Serial_Number",
        "dataModelName",
        "qDataBag.TLA",
        "qDataBag.Wave",
        "qDataBag.Prem1",
        "qDataBag.Prem2",
        "qDataBag.Prem3",
        "qDataBag.District",
        "qDataBag.PostTown",
        "qDataBag.PostCode",
        "qDataBag.TelNo",
        "qDataBag.TelNo2",
        "telNoAppt",
        "hOut",
        "qDataBag.UPRN_Latitude",
        "qDataBag.UPRN_Longitude",
        "qDataBag.Priority",
        "qDataBag.FieldCase",
        "qDataBag.FieldRegion",
        "qDataBag.FieldTeam",
        "qDataBag.WaveComDTE",
        "catiMana.CatiCall.RegsCalls[1].DialResult",
    ]

    def __init__(self, config: Config):
        self._config = config

    def get_cases(self, questionnaire_name: str) -> List[BlaiseCaseInformationModel]:
        restapi_client = blaise_restapi.Client(self._config.blaise_api_url)

        questionnaire_case_data = restapi_client.get_questionnaire_data(
            self._config.blaise_server_park,
            questionnaire_name,
            self.required_fields_from_blaise,
        )

        return [
            BlaiseCaseInformationModel.import_case(questionnaire_name, case_data_item)
            for case_data_item in questionnaire_case_data["reportingData"]
        ]

    def get_case(
        self, questionnaire_name: str, case_id: str
    ) -> BlaiseCaseInformationModel:
        restapi_client = blaise_restapi.Client(self._config.blaise_api_url)

        try:
            questionnaire_case_data = restapi_client.get_case(
                self._config.blaise_server_park, questionnaire_name, case_id
            )
        except HTTPError:
            raise QuestionnaireCaseDoesNotExistError()

        return BlaiseCaseInformationModel.import_case(
            questionnaire_name, questionnaire_case_data["fieldData"]
        )

    def questionnaire_exists(self, questionnaire_name: str) -> bool:
        restapi_client = blaise_restapi.Client(self._config.blaise_api_url)

        return restapi_client.questionnaire_exists_on_server_park(
            self._config.blaise_server_park, questionnaire_name
        )

    def update_case(
        self, questionnaire_name: str, case_id: str, data_fields: Dict[str, str]
    ) -> None:
        restapi_client = blaise_restapi.Client(self._config.blaise_api_url)

        restapi_client.patch_case_data(
            self._config.blaise_server_park, questionnaire_name, case_id, data_fields
        )
