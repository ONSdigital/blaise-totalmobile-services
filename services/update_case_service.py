import logging

from app.exceptions.custom_exceptions import (
    QuestionnaireCaseDoesNotExistError,
    QuestionnaireCaseError,
    QuestionnaireDoesNotExistError,
)
from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.blaise.blaise_case_update_model import BlaiseCaseUpdateModel
from models.totalmobile.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.questionnaire_service import QuestionnaireService


class UpdateCaseService:
    def __init__(self, questionnaire_service: QuestionnaireService):
        self._questionnaire_service = questionnaire_service

    def update_case(
        self, totalmobile_request: TotalMobileIncomingUpdateRequestModel
    ) -> None:
        self._validate_questionnaire_exists(totalmobile_request.questionnaire_name)

        blaise_case = self._get_case(
            totalmobile_request.questionnaire_name,
            totalmobile_request.case_id,
        )
        update_blaise_case_model = BlaiseCaseUpdateModel.import_case(
            totalmobile_request
        )

        if totalmobile_request.outcome_code == 300 and blaise_case.outcome_code in (
            0,
            310,
            320,
        ):
            self._update_case_contact_information(blaise_case, update_blaise_case_model)
            return

        if totalmobile_request.outcome_code in (460, 461, 510, 540, 551, 560, 580, 640):
            self._update_case_outcome_code(blaise_case, update_blaise_case_model)
            return

        logging.info(
            f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
            f"has not been updated in Blaise (Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )

    def _update_case_contact_information(
        self,
        blaise_case,
        update_blaise_case_model,
    ) -> None:
        fields_to_update = {}

        contact_fields = update_blaise_case_model.contact_details()
        if len(contact_fields) == 0:
            logging.info(
                f"Contact information has not been updated as no contact information was provided (Questionnaire={blaise_case.questionnaire_name}, "
                f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
                f"TM hOut={update_blaise_case_model.outcome_code})"
            )
            return

        fields_to_update.update(contact_fields)
        fields_to_update.update(
            update_blaise_case_model.knock_to_nudge_indicator_flag()
        )

        self._questionnaire_service.update_case(
            blaise_case.questionnaire_name, blaise_case.case_id, fields_to_update
        )

        logging.info(
            f"Contact information updated (Questionnaire={blaise_case.questionnaire_name}, "
            f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={update_blaise_case_model.outcome_code})"
        )

    def _update_case_outcome_code(
        self,
        blaise_case,
        update_blaise_case_model,
    ) -> None:
        fields_to_update = {}
        fields_to_update.update(update_blaise_case_model.outcome_details())
        fields_to_update.update(
            update_blaise_case_model.knock_to_nudge_indicator_flag()
        )
        fields_to_update.update(update_blaise_case_model.call_history_record(1))

        if not blaise_case.has_call_history:
            fields_to_update.update(update_blaise_case_model.call_history_record(5))

        self._questionnaire_service.update_case(
            blaise_case.questionnaire_name, blaise_case.case_id, fields_to_update
        )

        logging.info(
            f"Outcome code and call history updated (Questionnaire={blaise_case.questionnaire_name}, "
            f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={update_blaise_case_model.outcome_code})"
        )

    def _validate_questionnaire_exists(self, questionnaire_name: str) -> None:
        if not self._questionnaire_service.questionnaire_exists(questionnaire_name):
            logging.error(
                f"Could not find questionnaire {questionnaire_name} in Blaise"
            )
            raise QuestionnaireDoesNotExistError()

        logging.info(f"Successfully found questionnaire {questionnaire_name} in Blaise")

    def _get_case(
        self,
        questionnaire_name: str,
        case_id: str,
    ) -> BlaiseCaseInformationModel:
        try:
            case = self._questionnaire_service.get_case(questionnaire_name, case_id)
        except QuestionnaireCaseDoesNotExistError as err:
            logging.error(
                f"Could not find case {case_id} for questionnaire {questionnaire_name} in Blaise"
            )
            raise err
        except QuestionnaireCaseError as err:
            logging.error(
                f"There was an error retrieving case {case_id} for questionnaire {questionnaire_name} in Blaise"
            )
            raise err

        logging.info(
            f"Successfully found case {case_id} for questionnaire {questionnaire_name} in Blaise"
        )
        return case
