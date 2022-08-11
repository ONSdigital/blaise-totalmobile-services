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