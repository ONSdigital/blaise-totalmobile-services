import blaise_restapi
from appconfig import Config
from typing import List

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


def get_cases(questionnaire_name: str, config: Config) -> [List[QuestionnaireCaseModel]]:
    restapi_client = blaise_restapi.Client(config.blaise_api_url)

    questionnaire_case_data = restapi_client.get_questionnaire_data(
        config.blaise_server_park,
        questionnaire_name,
        required_fields_from_blaise
    )

    return [QuestionnaireCaseModel.import_case_data(case_data_item) for case_data_item in
            questionnaire_case_data["reportingData"]]
