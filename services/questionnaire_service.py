from typing import List
from appconfig import Config
from models.uac_model import UacModel
from services import blaise_restapi_service, uac_restapi_service
from models.questionnaire_case_model import QuestionnaireCaseModel


def get_questionnaire_cases(questionnaire_name: str, config: Config) -> List[QuestionnaireCaseModel]:
    questionnaire_case_data_dictionary = blaise_restapi_service.get_questionnaire_case_data(questionnaire_name, config)

    return [QuestionnaireCaseModel.import_case_data(questionnaire_case_data_item) for questionnaire_case_data_item in
            questionnaire_case_data_dictionary]


def get_questionnaire_uac_models(questionnaire_name: str, config: Config) -> List[UacModel]:
    uac_data_dictionary = uac_restapi_service.get_questionnaire_uacs(questionnaire_name, config)
    return [UacModel.import_uac_data(uac_data_dictionary[uac_data_dictionary_item]) for uac_data_dictionary_item in
            uac_data_dictionary]


def get_wave_from_questionnaire_name(questionnaire_name: str) -> str:
    if questionnaire_name[0:3] != "LMS":
        raise Exception(f"Invalid format for questionnaire name: {questionnaire_name}")
    return questionnaire_name[-1]