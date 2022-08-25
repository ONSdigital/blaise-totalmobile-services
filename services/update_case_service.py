import logging

from appconfig import Config
from app.exceptions.custom_exceptions import QuestionnaireDoesNotExistError, QuestionnaireCaseDoesNotExistError
from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.blaise.blaise_case_update_model import BlaiseCaseUpdateModel
from models.totalmobile.totalmobile_incoming_update_request_model import TotalMobileIncomingUpdateRequestModel


def update_case(totalmobile_request: TotalMobileIncomingUpdateRequestModel, config: Config, questionnaire_service) -> None:
    validate_questionnaire_exists(totalmobile_request.questionnaire_name, config, questionnaire_service)

    blaise_case = get_case(totalmobile_request.questionnaire_name, totalmobile_request.case_id, config, questionnaire_service)
    update_blaise_case_model = BlaiseCaseUpdateModel.import_case(totalmobile_request)

    if totalmobile_request.outcome_code == 300 and blaise_case.outcome_code in (0, 310, 320):
        _update_case_contact_information(blaise_case, update_blaise_case_model, config, questionnaire_service)
        return

    if totalmobile_request.outcome_code in (460, 461, 510, 540, 551, 560, 580, 640):
        _update_case_outcome_code(blaise_case, update_blaise_case_model, config, questionnaire_service)
        return

    logging.info(
        f'Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} '
        f'has not been updated in Blaise (Blaise hOut={blaise_case.outcome_code}, '
        f'TM hOut={totalmobile_request.outcome_code})')


def _update_case_contact_information(blaise_case, update_blaise_case_model, config, questionnaire_service) -> None:
    fields_to_update = {}

    contact_fields = update_blaise_case_model.contact_details()
    if len(contact_fields) == 0:
        logging.info(
            f"Contact information has not been updated as no contact information was provided (Questionnaire={blaise_case.questionnaire_name}, "
            f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={update_blaise_case_model.outcome_code})")
        return

    fields_to_update.update(contact_fields)
    fields_to_update.update(update_blaise_case_model.knock_to_nudge_indicator_flag())

    questionnaire_service.update_case(
        blaise_case.questionnaire_name,
        blaise_case.case_id,
        fields_to_update,
        config
    )

    logging.info(
        f"Contact information updated (Questionnaire={blaise_case.questionnaire_name}, "
        f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
        f"TM hOut={update_blaise_case_model.outcome_code})")


def _update_case_outcome_code(blaise_case, update_blaise_case_model, config, questionnaire_service) -> None:
    fields_to_update = {}
    fields_to_update.update(update_blaise_case_model.outcome_details())
    fields_to_update.update(update_blaise_case_model.knock_to_nudge_indicator_flag())

    questionnaire_service.update_case(
        blaise_case.questionnaire_name,
        blaise_case.case_id,
        fields_to_update,
        config
    )

    logging.info(
        f"Outcome code updated (Questionnaire={blaise_case.questionnaire_name}, "
        f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
        f"TM hOut={update_blaise_case_model.outcome_code})")


def validate_questionnaire_exists(questionnaire_name: str, config: Config, questionnaire_service) -> None:
    if not questionnaire_service.questionnaire_exists(questionnaire_name, config):
        logging.error(f"Could not find questionnaire {questionnaire_name} in Blaise")
        raise QuestionnaireDoesNotExistError()

    logging.info(f'Successfully found questionnaire {questionnaire_name} in Blaise')


def get_case(questionnaire_name: str, case_id: str, config: Config, questionnaire_service) -> BlaiseCaseInformationModel:
    try:
        case = questionnaire_service.get_case(questionnaire_name, case_id, config)
    except QuestionnaireCaseDoesNotExistError as err:
        logging.error(f"Could not find case {case_id} for questionnaire {questionnaire_name} in Blaise")
        raise err

    logging.info(f'Successfully found case {case_id} for questionnaire {questionnaire_name} in Blaise')
    return case
