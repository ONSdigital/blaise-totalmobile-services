import logging
from abc import abstractmethod
from typing import List

from models.common.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from models.create.blaise.blaiise_lms_case_model import BlaiseLMSCaseModel


class CaseFilterBase:
    @property
    @abstractmethod
    def wave_number(self) -> int:
        pass

    def case_is_eligible(self, case: BlaiseLMSCaseModel) -> bool:
        return (
            case.wave == self.wave_number
            and self.case_is_in_a_known_region(case)
            and self.case_is_eligible_additional_checks(case)
        )

    @abstractmethod
    def case_is_eligible_additional_checks(self, case: BlaiseLMSCaseModel) -> bool:
        pass

    @staticmethod
    def telephone_number_1_is_empty(case: BlaiseLMSCaseModel) -> bool:
        if case.telephone_number_1 == "":
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_1'"
        )
        return False

    @staticmethod
    def telephone_number_2_is_empty(case: BlaiseLMSCaseModel) -> bool:
        if case.telephone_number_2 == "":
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_2'"
        )
        return False

    @staticmethod
    def appointment_telephone_number_is_empty(
        case: BlaiseLMSCaseModel,
    ) -> bool:
        if case.appointment_telephone_number == "":
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value set for the field 'appointment_telephone_number'"
        )
        return False

    @staticmethod
    def case_has_field_case_of_y(case: BlaiseLMSCaseModel) -> bool:
        if case.field_case == "Y" or case.field_case == "y":
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a field case value of '{case.field_case}', not 'Y'"
        )
        return False

    @staticmethod
    def case_has_rotational_knock_to_nudge_indicator_of_empty_or_n(
        case: BlaiseLMSCaseModel,
    ) -> bool:
        if (
            case.rotational_knock_to_nudge_indicator == ""
            or case.rotational_knock_to_nudge_indicator == "N"
            or case.rotational_knock_to_nudge_indicator == "n"
        ):
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a knock to knudge indicator value of 'Y', not 'N'"
        )
        return False

    @staticmethod
    def case_has_a_desired_outcome_code_of(
        value_range: List[int], case: BlaiseLMSCaseModel
    ) -> bool:
        if case.outcome_code in value_range:
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value '{case.outcome_code}' outside of the range '{value_range}' set for the field 'outcome_code'"
        )
        return False

    @staticmethod
    def case_has_a_desired_rotational_outcome_code_of(
        value_range: List[int], case: BlaiseLMSCaseModel
    ) -> bool:
        if case.rotational_outcome_code in value_range:
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value '{case.rotational_outcome_code}' outside of the range '{value_range}' set for the field 'rotational_outcome_code'"
        )
        return False

    @staticmethod
    def case_is_in_a_known_region(case: BlaiseLMSCaseModel) -> bool:
        value_range = TotalmobileWorldModel.get_available_regions()
        if case.field_region in value_range:
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value '{case.field_region}' outside of the range '{value_range}' set for the field 'field_region'"
        )
        return False
