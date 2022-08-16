import logging

from appconfig import Config
from models.totalmobile_incoming_case_model import TotalMobileIncomingCaseModel
from app.exceptions.custom_exceptions import QuestionnaireDoesNotExistError, QuestionnaireCaseDoesNotExistError


def update_case(totalmobile_case: TotalMobileIncomingCaseModel, config: Config, questionnaire_service) -> None:
    validate_questionnaire_exists(totalmobile_case.questionnaire_name, config, questionnaire_service)
    validate_case_exists(totalmobile_case.questionnaire_name, totalmobile_case.case_id, config, questionnaire_service)


def validate_questionnaire_exists(questionnaire_name: str, config: Config, questionnaire_service) -> None:
    if not questionnaire_service.questionnaire_exists(questionnaire_name, config):
        logging.error(f"Could not find questionnaire {questionnaire_name} in Blaise")
        raise QuestionnaireDoesNotExistError()

    logging.info(f'Successfully found questionnaire {questionnaire_name} in Blaise')


def validate_case_exists(questionnaire_name: str, case_id: str, config: Config, questionnaire_service):
    try:
        questionnaire_service.get_case(questionnaire_name, case_id, config)
    except QuestionnaireCaseDoesNotExistError as err:
        logging.error(f"Could not find case {case_id} for questionnaire {questionnaire_name} in Blaise")
        raise err

    logging.info(f'Successfully found case {case_id} for questionnaire {questionnaire_name} in Blaise')

