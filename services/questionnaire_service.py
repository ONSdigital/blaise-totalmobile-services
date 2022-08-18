import logging
from typing import List, Dict
from appconfig import Config
from services import blaise_service, uac_service, eligible_blaise_case_service
from models.questionnaire_case_model import QuestionnaireCaseModel


def get_eligible_cases(questionnaire_name: str, config: Config) -> List[QuestionnaireCaseModel]:
    questionnaire_cases = get_cases(questionnaire_name, config)

    return eligible_blaise_case_service.get_eligible_cases(questionnaire_cases)


def get_cases(questionnaire_name: str, config: Config) -> List[QuestionnaireCaseModel]:
    questionnaire_cases = blaise_service.get_cases(questionnaire_name, config)
    questionnaire_uacs = uac_service.get_uacs(questionnaire_name, config)

    [questionnaire_case.populate_uac_data(
        next((x for x in questionnaire_uacs if x.case_id == questionnaire_case.case_id), None))
        for questionnaire_case in
        questionnaire_cases]

    return questionnaire_cases


def get_case(questionnaire_name: str, case_id: str, config: Config) -> QuestionnaireCaseModel:
    return blaise_service.get_case(questionnaire_name, case_id, config)


def get_wave_from_questionnaire_name(questionnaire_name: str) -> str:
    if questionnaire_name[0:3] != "LMS":
        raise Exception(f"Invalid format for questionnaire name: {questionnaire_name}")
    return questionnaire_name[-1]


def questionnaire_exists(questionnaire_name: str, config: Config) -> str:
    return blaise_service.questionnaire_exists(questionnaire_name, config)


def update_case(questionnaire_name: str, case_id: str, data_fields: Dict[str, str], config: Config) -> None:
    logging.info(
        f'Attempting to update case {case_id} in questionnaire {questionnaire_name} in Blaise with data fields {data_fields}')

    return blaise_service.update_case(questionnaire_name, case_id, data_fields, config)
