import logging
from abc import abstractmethod
from typing import List

from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel


class CaseFilterBase:
    @property
    @abstractmethod
    def wave_number(self) -> int:
        pass

    def case_is_eligible(self, case: BlaiseCaseInformationModel) -> bool:
        return (
            case.wave == self.wave_number
            and self.case_is_in_a_known_region(case)
            and self.case_is_eligible_additional_checks(case)
        )

    @abstractmethod
    def case_is_eligible_additional_checks(
        self, case: BlaiseCaseInformationModel
    ) -> bool:
        pass

    @staticmethod
    def case_has_telephone_numbers(case: BlaiseCaseInformationModel) -> bool:
        if (
            case.contact_details.telephone_number_1 != ""
            or case.contact_details.telephone_number_2 != ""
            or case.contact_details.appointment_telephone_number != ""
        ):
            return True

        return False

    @staticmethod
    def telephone_number_1_is_empty(case: BlaiseCaseInformationModel) -> bool:
        if case.contact_details.telephone_number_1 == "":
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_1'"
        )
        return False

    @staticmethod
    def telephone_number_2_is_empty(case: BlaiseCaseInformationModel) -> bool:
        if case.contact_details.telephone_number_2 == "":
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_2'"
        )
        return False

    @staticmethod
    def appointment_telephone_number_is_empty(case: BlaiseCaseInformationModel) -> bool:
        if case.contact_details.appointment_telephone_number == "":
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value set for the field 'appointment_telephone_number'"
        )
        return False

    @staticmethod
    def case_has_field_case_of_y(case: BlaiseCaseInformationModel) -> bool:
        if case.field_case == "Y" or case.field_case == "y":
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a field case value of '{case.field_case}', not 'Y'"
        )
        return False

    @staticmethod
    def case_has_rotational_knock_to_nudge_indicator_of_empty_or_n(
        case: BlaiseCaseInformationModel,
    ) -> bool:
        if (
            case.rotational_knock_to_nudge_indicator == ""
            or case.rotational_knock_to_nudge_indicator == "N"
            or case.rotational_knock_to_nudge_indicator == "n"
        ):
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a knock to knudge indicator value of '{case.rotational_knock_to_nudge_indicator}', not 'N'"
        )
        return False

    @staticmethod
    def case_has_a_desired_outcome_code_of(
        value_range: List[int], case: BlaiseCaseInformationModel
    ) -> bool:
        if case.outcome_code in value_range:
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value '{case.outcome_code}' outside of the range '{value_range}' set for the field 'outcome_code'"
        )
        return False

    @staticmethod
    def case_has_a_desired_rotational_outcome_code_of(
        value_range: List[int], case: BlaiseCaseInformationModel
    ) -> bool:
        if case.rotational_outcome_code in value_range:
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value '{case.rotational_outcome_code}' outside of the range '{value_range}' set for the field 'rotational_outcome_code'"
        )
        return False

    @staticmethod
    def case_is_in_a_known_region(case: BlaiseCaseInformationModel) -> bool:
        value_range = TotalmobileWorldModel.get_available_regions()
        if case.field_region in value_range:
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value '{case.field_region}' outside of the range '{value_range}' set for the field 'field_region'"
        )
        return False
