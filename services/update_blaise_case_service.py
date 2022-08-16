import logging

from appconfig import Config
from services import questionnaire_service
from models.totalmobile_incoming_case_model import TotalMobileIncomingCaseModel
from app.exceptions.custom_exceptions import QuestionnaireDoesNotExistError, QuestionnaireCaseDoesNotExistError


def update_case(totalmobile_case: TotalMobileIncomingCaseModel, config: Config) -> None:
    validate_questionnaire_exists(totalmobile_case.questionnaire_name, config)
    validate_case_exists(totalmobile_case.questionnaire_name, totalmobile_case.case_id, config)


def validate_questionnaire_exists(questionnaire_name: str, config: Config) -> None:
    if not questionnaire_service.questionnaire_exists(questionnaire_name, config):
        logging.error(f"Could not find questionnaire {questionnaire_name} in Blaise")
        raise QuestionnaireDoesNotExistError()

    logging.info(f'Successfully found questionnaire {questionnaire_name} in Blaise')


def validate_case_exists(questionnaire_name: str, case_id: str, config: Config):
    try:
        questionnaire_service.get_case(questionnaire_name, case_id, config)
    except QuestionnaireCaseDoesNotExistError as err:
        logging.error(f"Could not find case {case_id} for questionnaire {questionnaire_name} in Blaise")
        raise err

    logging.info(f'Successfully found case {case_id} for questionnaire {questionnaire_name} in Blaise')

