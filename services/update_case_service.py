import logging
from enum import Enum

from app.exceptions.custom_exceptions import (
    QuestionnaireCaseDoesNotExistError,
    QuestionnaireCaseError,
    QuestionnaireDoesNotExistError,
)
from models.blaise.blaise_case_update_model import BlaiseCaseUpdateModel
from models.blaise.blaise_lms_case_information_model import (
    BlaiseLMSCaseInformationModel,
)
from models.totalmobile.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.questionnaires.lms_questionnaire_service import LMSQuestionnaireService


class QuestionnaireOutcomeCodes(Enum):
    NOT_STARTED_0 = 0
    WEB_NUDGED_120 = 120
    APPOINTMENT_300 = 300
    NON_CONTACT_310 = 310
    PHONE_NO_REMOVED_BY_TO_320 = 320
    REFUSAL_HARD_460 = 460
    REFUSAL_SOFT_461 = 461
    INELIGIBLE_NO_TRACE_OF_ADDRESS_510 = 510
    INELIGIBLE_VACANT_540 = 540
    INELIGIBLE_NON_RESIDENTIAL_551 = 551
    INELIGIBLE_INSTITUTION_560 = 560
    INELIGIBLE_SECOND_OR_HOLIDAY_HOME_580 = 580
    WRONG_ADDRESS_640 = 640


class UpdateCaseService:
    def __init__(self, questionnaire_service: LMSQuestionnaireService):
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

        if (
            totalmobile_request.outcome_code
            == QuestionnaireOutcomeCodes.APPOINTMENT_300.value
            and blaise_case.outcome_code
            in (
                QuestionnaireOutcomeCodes.NOT_STARTED_0.value,
                QuestionnaireOutcomeCodes.NON_CONTACT_310.value,
                QuestionnaireOutcomeCodes.PHONE_NO_REMOVED_BY_TO_320.value,
            )
        ):
            self._update_case_contact_information(blaise_case, update_blaise_case_model)
            return

        if totalmobile_request.outcome_code in (
            QuestionnaireOutcomeCodes.REFUSAL_HARD_460.value,
            QuestionnaireOutcomeCodes.REFUSAL_SOFT_461.value,
            QuestionnaireOutcomeCodes.INELIGIBLE_NO_TRACE_OF_ADDRESS_510.value,
            QuestionnaireOutcomeCodes.INELIGIBLE_VACANT_540.value,
            QuestionnaireOutcomeCodes.INELIGIBLE_NON_RESIDENTIAL_551.value,
            QuestionnaireOutcomeCodes.INELIGIBLE_INSTITUTION_560.value,
            QuestionnaireOutcomeCodes.INELIGIBLE_SECOND_OR_HOLIDAY_HOME_580.value,
            QuestionnaireOutcomeCodes.WRONG_ADDRESS_640.value,
        ):
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
    ) -> BlaiseLMSCaseInformationModel:
        try:
            case = self._questionnaire_service.get_case(questionnaire_name, case_id, False)
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
