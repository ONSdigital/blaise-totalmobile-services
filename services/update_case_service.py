import logging

from appconfig import Config
from app.exceptions.custom_exceptions import QuestionnaireDoesNotExistError, QuestionnaireCaseDoesNotExistError
from models.questionnaire_case_model import QuestionnaireCaseModel
from models.totalmobile_incoming_update_request_model import TotalMobileIncomingUpdateRequestModel


def update_case(totalmobile_request: TotalMobileIncomingUpdateRequestModel, config: Config, questionnaire_service) -> None:
    validate_questionnaire_exists(totalmobile_request.questionnaire_name, config, questionnaire_service)

    blaise_case = get_case(totalmobile_request.questionnaire_name, totalmobile_request.case_id, config, questionnaire_service)

    if totalmobile_request.outcome_code == 300 and blaise_case.outcome_code in (0, 310, 320):
        _update_case_contact_information(blaise_case, config, questionnaire_service, totalmobile_request)

    if totalmobile_request.outcome_code in(460, 461, 510, 540, 551, 560, 580, 640):
        _update_case_outcome_code(blaise_case, config, questionnaire_service, totalmobile_request)

    logging.info(
        f'Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} '
        f'has not been updated in Blaise (Blaise hOut={blaise_case.outcome_code}, '
        f'TM hOut={totalmobile_request.outcome_code})')


def _update_case_contact_information(blaise_case, config, questionnaire_service, totalmobile_request) -> None:
    data_fields = {
        "dMktnName": totalmobile_request.contact_name,
        "qDataBag.TelNo": totalmobile_request.home_phone_number,
        "qDataBag.TelNo2": totalmobile_request.mobile_phone_number
    }

    questionnaire_service.update_case(totalmobile_request.questionnaire_name, totalmobile_request.case_id, data_fields,
                                      config)
    logging.info(
        f"Contact information updated (Questionnaire={totalmobile_request.questionnaire_name}, "
        f"Case Id={totalmobile_request.case_id}, Blaise hOut={blaise_case.outcome_code}, "
        f"TM hOut={totalmobile_request.outcome_code})")


def _update_case_outcome_code(blaise_case, config, questionnaire_service, totalmobile_request) -> None:
    data_fields = {
        "hOut": f"{totalmobile_request.outcome_code}"
    }
    questionnaire_service.update_case(totalmobile_request.questionnaire_name, totalmobile_request.case_id, data_fields,
                                      config)

    logging.info(
        f"Outcome code updated (Questionnaire={totalmobile_request.questionnaire_name}, "
        f"Case Id={totalmobile_request.case_id}, Blaise hOut={blaise_case.outcome_code}, "
        f"TM hOut={totalmobile_request.outcome_code})")


def validate_questionnaire_exists(questionnaire_name: str, config: Config, questionnaire_service) -> None:
    if not questionnaire_service.questionnaire_exists(questionnaire_name, config):
        logging.error(f"Could not find questionnaire {questionnaire_name} in Blaise")
        raise QuestionnaireDoesNotExistError()

    logging.info(f'Successfully found questionnaire {questionnaire_name} in Blaise')


def get_case(questionnaire_name: str, case_id: str, config: Config, questionnaire_service) -> QuestionnaireCaseModel:
    try:
        case = questionnaire_service.get_case(questionnaire_name, case_id, config)
    except QuestionnaireCaseDoesNotExistError as err:
        logging.error(f"Could not find case {case_id} for questionnaire {questionnaire_name} in Blaise")
        raise err

    logging.info(f'Successfully found case {case_id} for questionnaire {questionnaire_name} in Blaise')
    return case
