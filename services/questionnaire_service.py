import blaise_restapi
from typing import List
from appconfig import Config
from services import blaise_service, uac_service, eligible_case_service
from models.questionnaire_case_model import QuestionnaireCaseModel


def get_eligible_cases(questionnaire_name: str, config: Config) -> List[QuestionnaireCaseModel]:
    questionnaire_cases = get_cases(questionnaire_name, config)

    return eligible_case_service.filter_eligible_cases(questionnaire_cases)


def get_cases(questionnaire_name: str, config: Config) -> List[QuestionnaireCaseModel]:
    questionnaire_cases = blaise_service.get_cases(questionnaire_name, config)
    questionnaire_uacs = uac_service.get_uacs(questionnaire_name, config)

    [questionnaire_case.populate_uac_data(
        next((x for x in questionnaire_uacs if x.case_id == questionnaire_case.case_id), None))
        for questionnaire_case in
        questionnaire_cases]

    return questionnaire_cases


def get_wave_from_questionnaire_name(questionnaire_name: str) -> str:
    if questionnaire_name[0:3] != "LMS":
        raise Exception(f"Invalid format for questionnaire name: {questionnaire_name}")
    return questionnaire_name[-1]


def update_case_field(
    questionnaire_name: str, case_id: str, field_id: str, field_value: str, config: Config
) -> None:
    restapi_client = blaise_restapi.Client(config.blaise_api_url)
    print(f"\nrest_api: {restapi_client}")

    data_fields = {field_id: field_value}
    print(f"\ndata_fields: {data_fields}")
    restapi_client.patch_case_data(
        config.blaise_server_park, questionnaire_name, case_id, data_fields
    )