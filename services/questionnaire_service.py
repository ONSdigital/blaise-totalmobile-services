from typing import List
from appconfig import Config
from models.uac_model import UacModel
from services import blaise_restapi_service, uac_restapi_service, case_service
from models.case_model import CaseModel


def get_eligible_cases(questionnaire_name: str, config: Config) -> List[CaseModel]:
    case_data_models = blaise_restapi_service.get_cases(questionnaire_name, config)

    return case_service.filter_eligible_cases(case_data_models)


def get_uacs(questionnaire_name: str, config: Config) -> List[UacModel]:
    return uac_restapi_service.get_questionnaire_uacs(questionnaire_name, config)


def get_wave_from_questionnaire_name(questionnaire_name: str) -> str:
    if questionnaire_name[0:3] != "LMS":
        raise Exception(f"Invalid format for questionnaire name: {questionnaire_name}")
    return questionnaire_name[-1]