import blaise_restapi

from typing import List
from appconfig import Config
from models.questionnaire_case_model import QuestionnaireCaseModel

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
    "qDataBag.FieldRegion",
    "qDataBag.FieldTeam",
    "qDataBag.WaveComDTE",
]


def get_questionnaire_cases(questionnaire_name: str, config: Config) -> List[QuestionnaireCaseModel]:
    restapi_client = blaise_restapi.Client(config.blaise_api_url)

    questionnaire_data = restapi_client.get_questionnaire_data(
        config.blaise_server_park,
        questionnaire_name,
        required_fields_from_blaise
    )

    case_data_dictionary_list = questionnaire_data["reportingData"]
    return [QuestionnaireCaseModel.import_case_data_dictionary(case_data_dictionary) for case_data_dictionary in
            case_data_dictionary_list]
