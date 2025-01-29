import logging
from typing import Dict

from enums.questionnaire_case_outcome_codes import LMSQuestionnaireOutcomeCodes
from models.update.blaise_update_case_model import BlaiseUpdateCase
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.blaise_service import RealBlaiseService
from services.update.update_case_service_base import UpdateCaseServiceBase


class LMSUpdateCaseService(UpdateCaseServiceBase):
    def __init__(self, blaise_service: RealBlaiseService):
        super().__init__(blaise_service)
        self._blaise_service = blaise_service

    def update_case(
        self, totalmobile_request: TotalMobileIncomingUpdateRequestModel
    ) -> None:
        self.validate_questionnaire_exists(totalmobile_request.questionnaire_name)

        blaise_case = self.get_existing_blaise_case(
            totalmobile_request.questionnaire_name, totalmobile_request.case_id
        )

        if (
            totalmobile_request.outcome_code
            == LMSQuestionnaireOutcomeCodes.APPOINTMENT_300.value
            and blaise_case.outcome_code
            in (
                LMSQuestionnaireOutcomeCodes.NOT_STARTED_0.value,
                LMSQuestionnaireOutcomeCodes.NON_CONTACT_310.value,
                LMSQuestionnaireOutcomeCodes.PHONE_NO_REMOVED_BY_TO_320.value,
            )
        ):
            self._update_case_contact_information(totalmobile_request, blaise_case)
            return

        if totalmobile_request.outcome_code in (
            LMSQuestionnaireOutcomeCodes.REFUSAL_HARD_460.value,
            LMSQuestionnaireOutcomeCodes.REFUSAL_SOFT_461.value,
            LMSQuestionnaireOutcomeCodes.INELIGIBLE_NO_TRACE_OF_ADDRESS_510.value,
            LMSQuestionnaireOutcomeCodes.INELIGIBLE_VACANT_540.value,
            LMSQuestionnaireOutcomeCodes.INELIGIBLE_NON_RESIDENTIAL_551.value,
            LMSQuestionnaireOutcomeCodes.INELIGIBLE_INSTITUTION_560.value,
            LMSQuestionnaireOutcomeCodes.INELIGIBLE_SECOND_OR_HOLIDAY_HOME_580.value,
            LMSQuestionnaireOutcomeCodes.WRONG_ADDRESS_640.value,
        ):

            self._update_case_outcome_code(totalmobile_request, blaise_case)
            return

        logging.info(
            f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
            f"has not been updated in Blaise (Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )

    def _update_case_contact_information(
        self,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
        blaise_case: BlaiseUpdateCase,
    ) -> None:
        fields_to_update: Dict[str, str] = {}
        contact_fields = blaise_case.get_contact_details_fields(totalmobile_request)

        if len(contact_fields) == 0:
            logging.info(
                f"Contact information has not been updated as no contact information was provided (Questionnaire={totalmobile_request.questionnaire_name}, "
                f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
                f"TM hOut={totalmobile_request.outcome_code})"
            )
            return

        fields_to_update.update(contact_fields)
        fields_to_update.update(blaise_case.get_knock_to_nudge_indicator_flag_field())

        logging.info(
            f"Attempting to update case {totalmobile_request.case_id} in questionnaire {totalmobile_request.questionnaire_name} in Blaise"
        )

        self._blaise_service.update_case(
            totalmobile_request.questionnaire_name,
            totalmobile_request.case_id,
            fields_to_update,
        )

        logging.info(
            f"Contact information updated (Questionnaire={totalmobile_request.questionnaire_name}, "
            f"Case Id={totalmobile_request.case_id}, Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )

    def _update_case_outcome_code(
        self,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
        blaise_case: BlaiseUpdateCase,
    ) -> None:

        fields_to_update = {}

        fields_to_update.update(
            blaise_case.get_outcome_code_fields(totalmobile_request)
        )
        fields_to_update.update(blaise_case.get_knock_to_nudge_indicator_flag_field())
        fields_to_update.update(blaise_case.get_call_history_record_field(1))

        if not blaise_case.has_call_history:
            fields_to_update.update(blaise_case.get_call_history_record_field(5))

        self._blaise_service.update_case(
            totalmobile_request.questionnaire_name,
            totalmobile_request.case_id,
            fields_to_update,
        )

        logging.info(
            f"Outcome code and call history updated (Questionnaire={totalmobile_request.questionnaire_name}, "
            f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )
