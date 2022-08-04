import blaise_restapi
from appconfig import Config
from typing import Dict

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


def get_questionnaire_case_data(questionnaire_name: str, config: Config) -> [Dict[str, str]]:
    restapi_client = blaise_restapi.Client(config.blaise_api_url)

    questionnaire_case_data = restapi_client.get_questionnaire_data(
        config.blaise_server_park,
        questionnaire_name,
        required_fields_from_blaise
    )

    return questionnaire_case_data["reportingData"]
