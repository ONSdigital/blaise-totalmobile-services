from typing import Dict, List

import blaise_restapi
from urllib3.exceptions import HTTPError

from app.exceptions.custom_exceptions import QuestionnaireCaseDoesNotExistError
from appconfig import Config
from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel

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


def get_cases(
    questionnaire_name: str, config: Config
) -> [List[BlaiseCaseInformationModel]]:
    restapi_client = blaise_restapi.Client(config.blaise_api_url)

    questionnaire_case_data = restapi_client.get_questionnaire_data(
        config.blaise_server_park, questionnaire_name, required_fields_from_blaise
    )

    return [
        BlaiseCaseInformationModel.import_case(questionnaire_name, case_data_item)
        for case_data_item in questionnaire_case_data["reportingData"]
    ]


def get_case(
    questionnaire_name: str, case_id: str, config: Config
) -> BlaiseCaseInformationModel:
    restapi_client = blaise_restapi.Client(config.blaise_api_url)

    try:
        questionnaire_case_data = restapi_client.get_case(
            config.blaise_server_park, questionnaire_name, case_id
        )
    except HTTPError:
        raise QuestionnaireCaseDoesNotExistError()

    return BlaiseCaseInformationModel.import_case(
        questionnaire_name, questionnaire_case_data["fieldData"]
    )


def questionnaire_exists(questionnaire_name: str, config: Config) -> bool:
    restapi_client = blaise_restapi.Client(config.blaise_api_url)

    return restapi_client.questionnaire_exists_on_server_park(
        config.blaise_server_park, questionnaire_name
    )


def update_case(
    questionnaire_name: str, case_id: str, data_fields: Dict[str, str], config: Config
) -> None:
    restapi_client = blaise_restapi.Client(config.blaise_api_url)

    restapi_client.patch_case_data(
        config.blaise_server_park, questionnaire_name, case_id, data_fields
    )
