import logging

from appconfig import Config
from services import questionnaire_service
from models.totalmobile_incoming_case_model import TotalMobileIncomingCaseModel
from app.exceptions.custom_exceptions import QuestionnaireDoesNotExistError, QuestionnaireCaseDoesNotExistError


def update_case(totalmobile_case: TotalMobileIncomingCaseModel, config: Config) -> None:
    if not questionnaire_service.questionnaire_exists(totalmobile_case.questionnaire_name, config):
        logging.error(f"Could not find questionnaire {totalmobile_case.questionnaire_name} in Blaise")
        raise QuestionnaireDoesNotExistError()

    logging.info(f'Successfully found questionnaire {totalmobile_case.questionnaire_name} in Blaise')

    try:
        questionnaire_service.get_case(totalmobile_case.questionnaire_name, totalmobile_case.case_id, config)
    except QuestionnaireCaseDoesNotExistError as err:
        logging.error(f"Could not find case {totalmobile_case.case_id} for questionnaire {totalmobile_case.questionnaire_name} in Blaise")
        raise err

    logging.info(f'Successfully found case {totalmobile_case.case_id} for questionnaire {totalmobile_case.questionnaire_name} in Blaise')

