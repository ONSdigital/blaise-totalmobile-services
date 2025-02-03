import logging
from typing import Dict

from app.exceptions.custom_exceptions import (
    QuestionnaireCaseDoesNotExistError,
    QuestionnaireCaseError,
)
from enums.questionnaire_case_outcome_codes import FRSQuestionnaireOutcomeCodes
from models.update.frs_blaise_update_case_model import FRSBlaiseUpdateCase
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.blaise_service import RealBlaiseService
from services.update.update_case_service_base import UpdateCaseServiceBase


class FRSUpdateCaseService(UpdateCaseServiceBase):
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

        if self._should_update_case_outcome_code(blaise_case, totalmobile_request):
            self._update_case_outcome_code(totalmobile_request, blaise_case)
            return

        if self._should_update_refusal_reason(blaise_case, totalmobile_request):
            self._update_case_refusal_reason(totalmobile_request, blaise_case)

        self._log_no_update(blaise_case, totalmobile_request)

    def _update_case_outcome_code(
        self,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
        blaise_case: FRSBlaiseUpdateCase,
    ) -> None:

        fields_to_update = self._get_fields_to_update_case_outcome_code(
            blaise_case, totalmobile_request
        )

        self._log_attempting_to_update_case(totalmobile_request)

        self._blaise_service.update_case(
            totalmobile_request.questionnaire_name,
            totalmobile_request.case_id,
            fields_to_update,
        )

        self._log_outcome_code_updated(blaise_case, totalmobile_request)

    @staticmethod
    def _should_update_case_outcome_code(
        blaise_case: FRSBlaiseUpdateCase,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> bool:
        return totalmobile_request.outcome_code in (
            FRSQuestionnaireOutcomeCodes.NO_CONTACT_WITH_ANYONE_AT_ADDRESS_310.value,
            FRSQuestionnaireOutcomeCodes.CONTACT_MADE_AT_ADDRESS_NO_CONTACT_WITH_SAMPLED_HOUSEHOLD_MULTI_320.value,
            FRSQuestionnaireOutcomeCodes.CONTACT_WITH_SAMPLED_HOUSEHOLD_NO_CONTACT_WITH_RESPONSIBLE_RESIDENT_330.value,
            FRSQuestionnaireOutcomeCodes.ILL_AT_HOME_DURING_SURVEY_PERIOD_512.value,
            FRSQuestionnaireOutcomeCodes.AWAY_IN_HOSPITAL_DURING_SURVEY_PERIOD_522.value,
            FRSQuestionnaireOutcomeCodes.PHYSICALLY_MENTALLY_UNABLE_INCOMPETENT_532.value,
            FRSQuestionnaireOutcomeCodes.LANGUAGE_DIFFICULTIES_542.value,
            FRSQuestionnaireOutcomeCodes.NOT_ISSUED_TO_INTERVIEWER_OFFICE_APPROVAL_NEEDED_611.value,
            FRSQuestionnaireOutcomeCodes.ISSUED_BUT_NOT_ATTEMPTED_OFFICE_APPROVAL_NEEDED_612.value,
            FRSQuestionnaireOutcomeCodes.INACCESSIBLE_620.value,
            FRSQuestionnaireOutcomeCodes.UNABLE_TO_LOCATE_ADDRESS_630.value,
            FRSQuestionnaireOutcomeCodes.UNKNOWN_WHETHER_RESIDENTIAL_HOUSING_INFORMATION_REFUSED_641.value,
            FRSQuestionnaireOutcomeCodes.UNKNOWN_WHETHER_RESIDENTIAL_HOUSING_NO_CONTACT_WITH_KNOWLEDGEABLE_PERSON_642.value,
            FRSQuestionnaireOutcomeCodes.RESIDENTIAL_ADDRESS_UNKNOWN_IF_ELIGIBLE_HOUSEHOLD_INFORMATION_REFUSED_651.value,
            FRSQuestionnaireOutcomeCodes.RESIDENTIAL_ADDRESS_UNKNOWN_IF_ELIGIBLE_HOUSEHOLD_NO_CONTACT_WITH_KNOWLEDGEABLE_PERSON_652.value,
            FRSQuestionnaireOutcomeCodes.OTHER_UNKNOWN_ELIGIBILITY_OFFICE_APPROVAL_NEEDED_670.value,
            FRSQuestionnaireOutcomeCodes.NOT_YET_BUILT_UNDER_CONSTRUCTION_710.value,
            FRSQuestionnaireOutcomeCodes.DEMOLISHED_DERELICT_720.value,
            FRSQuestionnaireOutcomeCodes.VACANT_EMPTY_730.value,
            FRSQuestionnaireOutcomeCodes.NON_RESIDENTIAL_ADDRESS_740.value,
            FRSQuestionnaireOutcomeCodes.ADDRESS_OCCUPIED_NO_RESIDENT_HOUSEHOLD_750.value,
            FRSQuestionnaireOutcomeCodes.COMMUNAL_ESTABLISHMENT_INSTITUTION_760.value,
            FRSQuestionnaireOutcomeCodes.DWELLING_OF_FOREIGN_SERVICE_PERSONNEL_DIPLOMATS_771.value,
            FRSQuestionnaireOutcomeCodes.ALL_RESIDENTS_UNDER_16_772.value,
            FRSQuestionnaireOutcomeCodes.OTHER_RESIDENT_HOUSEHOLD_NO_ELIGIBLE_RESIDENTS_773.value,
            FRSQuestionnaireOutcomeCodes.DIRECTED_NOT_TO_SAMPLE_AT_ADDRESS_781.value,
            FRSQuestionnaireOutcomeCodes.NOT_TO_INTERVIEW_INSTRUCTS_SCOTTISH_PRE_SELECTION_SHEET_782.value,
            FRSQuestionnaireOutcomeCodes.HOUSEHOLD_LIMIT_ON_QUOTA_REACHED_MAXIMUM_OF_4_EXTRA_HOUSEHOLDS_783.value,
            FRSQuestionnaireOutcomeCodes.OTHER_OFFICE_APPROVAL_NEEDED_790.value,
        ) and blaise_case.outcome_code in (
            FRSQuestionnaireOutcomeCodes.NOT_STARTED_0.value,
            FRSQuestionnaireOutcomeCodes.NO_CONTACT_WITH_ANYONE_AT_ADDRESS_310.value,
            FRSQuestionnaireOutcomeCodes.CONTACT_MADE_AT_ADDRESS_NO_CONTACT_WITH_SAMPLED_HOUSEHOLD_MULTI_320.value,
            FRSQuestionnaireOutcomeCodes.CONTACT_WITH_SAMPLED_HOUSEHOLD_NO_CONTACT_WITH_RESPONSIBLE_RESIDENT_330.value,
        )

    @staticmethod
    def _get_fields_to_update_case_outcome_code(
        blaise_case: FRSBlaiseUpdateCase,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> Dict[str, str]:
        return {**blaise_case.get_outcome_code_fields(totalmobile_request)}

    @staticmethod
    def _log_outcome_code_updated(
        blaise_case: FRSBlaiseUpdateCase,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> None:
        logging.info(
            f"Outcome code updated (Questionnaire={totalmobile_request.questionnaire_name}, "
            f"Case Id={blaise_case.case_id}, Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )

    @staticmethod
    def _log_attempting_to_update_case(
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> None:
        logging.info(
            f"Attempting to update case {totalmobile_request.case_id} in questionnaire {totalmobile_request.questionnaire_name} in Blaise"
        )

    def get_existing_blaise_case(
        self,
        questionnaire_name: str,
        case_id: str,
    ) -> FRSBlaiseUpdateCase:
        try:
            case = self._blaise_service.get_case(questionnaire_name, case_id)
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
        return FRSBlaiseUpdateCase(questionnaire_name, case)

    @staticmethod
    def _log_no_update(
        blaise_case: FRSBlaiseUpdateCase,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> None:
        logging.info(
            f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
            f"has not been updated in Blaise (Blaise hOut={blaise_case.outcome_code}, "
            f"TM hOut={totalmobile_request.outcome_code})"
        )

    @staticmethod
    def _should_update_refusal_reason(
        blaise_case: FRSBlaiseUpdateCase,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> bool:
        return totalmobile_request.outcome_code in (
            FRSQuestionnaireOutcomeCodes.HQ_OFFICE_REFUSAL_GENERAL_410.value,
            FRSQuestionnaireOutcomeCodes.MULTI_INFORMATION_REFUSED_NO_OF_HOUSEHOLDS_AT_ADDRESS_420.value,
            FRSQuestionnaireOutcomeCodes.REFUSAL_AT_INTRODUCTION_BEFORE_INTERVIEW_BY_ADULT_HOUSEHOLD_MEMBER_431.value,
            FRSQuestionnaireOutcomeCodes.REFUSAL_AT_INTRODUCTION_BEFORE_INTERVIEW_BY_PROXY_432.value,
            FRSQuestionnaireOutcomeCodes.REFUSAL_DURING_INTERVIEW_HRP_BU_MEMBER_REFUSED_TO_COMPLETE_INTERVIEW_441.value,
            FRSQuestionnaireOutcomeCodes.REFUSAL_DURING_INTERVIEW_12_PLUS_DKS_OR_REFUSALS_IN_HHLD_SECTION_HRP_BU_442.value,
            FRSQuestionnaireOutcomeCodes.BROKEN_APPOINTMENT_NO_RE_CONTACT_450.value,
        ) and blaise_case.outcome_code in (
            FRSQuestionnaireOutcomeCodes.NOT_STARTED_0.value,
            FRSQuestionnaireOutcomeCodes.NO_CONTACT_WITH_ANYONE_AT_ADDRESS_310.value,
            FRSQuestionnaireOutcomeCodes.CONTACT_MADE_AT_ADDRESS_NO_CONTACT_WITH_SAMPLED_HOUSEHOLD_MULTI_320.value,
            FRSQuestionnaireOutcomeCodes.CONTACT_WITH_SAMPLED_HOUSEHOLD_NO_CONTACT_WITH_RESPONSIBLE_RESIDENT_330.value,
        )

    def _update_case_refusal_reason(
        self,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
        blaise_case: FRSBlaiseUpdateCase,
    ) -> None:
        fields_to_update = self._get_fields_to_update_refusal_reason(
            blaise_case, totalmobile_request
        )

        self._log_attempting_to_update_case(totalmobile_request)

        self._blaise_service.update_case(
            totalmobile_request.questionnaire_name,
            totalmobile_request.case_id,
            fields_to_update,
        )

        self._log_outcome_code_updated(blaise_case, totalmobile_request)

    @staticmethod
    def _get_fields_to_update_refusal_reason(
        blaise_case: FRSBlaiseUpdateCase,
        totalmobile_request: TotalMobileIncomingUpdateRequestModel,
    ) -> Dict[str, str]:
        return {
            **blaise_case.get_outcome_code_fields(totalmobile_request),
            **blaise_case.get_refusal_reason_fields(totalmobile_request),
        }
