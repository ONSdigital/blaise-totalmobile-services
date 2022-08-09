import logging
from typing import List
from models.questionnaire_case_model import QuestionnaireCaseModel
from cloud_functions.logging import setup_logger

setup_logger()


def filter_eligible_cases(cases: List[QuestionnaireCaseModel]) -> List[QuestionnaireCaseModel]:
    filtered_cases = [
        case
        for case in cases
        if (
                telephone_number_is_empty(case) and
                telephone_number_2_is_empty(case) and
                appointment_telephone_number_is_empty(case) and
                case_is_part_of_wave_1(case) and
                case_has_a_priority_between_1_and_5(case) and
                case_has_a_desired_outcome_code_of_blank_0_or_310(case)
        )
    ]

    for filtered_case in filtered_cases:
        logging.info(f"Case '{filtered_case.case_id}' was eligible and will be included")

    return filtered_cases


def telephone_number_is_empty(case: QuestionnaireCaseModel) -> bool:
    if case.telephone_number_1 == "":
        return True

    logging.info(
        f"Case '{case.case_id}' was not eligible to be sent to totalmobile as it has a value set for the field 'telephone_number_1'")
    return False


def telephone_number_2_is_empty(case: QuestionnaireCaseModel) -> bool:
    if case.telephone_number_2 == "":
        return True

    logging.info(
        f"Case '{case.case_id}' was not eligible to be sent to totalmobile as it has a value set for the field 'telephone_number_2'")
    return False


def appointment_telephone_number_is_empty(case: QuestionnaireCaseModel) -> bool:
    if case.appointment_telephone_number == "":
        return True

    logging.info(
        f"Case '{case.case_id}' was not eligible to be sent to totalmobile as it has a value set for the field 'appointment_telephone_number'")
    return False


def case_is_part_of_wave_1(case: QuestionnaireCaseModel) -> bool:
    value_range = ["1"]
    if case.wave in value_range:
        return True

    logging.info(
        f"Case '{case.case_id}' was not eligible to be sent to totalmobile as it has a value '{case.wave}' outside of the range '{value_range}' set for the field 'wave'")
    return False


def case_has_a_priority_between_1_and_5(case: QuestionnaireCaseModel) -> bool:
    value_range = ["1", "2", "3", "4", "5"]
    if case.priority in value_range:
        return True

    logging.info(
        f"Case '{case.case_id}' was not eligible to be sent to totalmobile as it has a value '{case.priority}' outside of the range '{value_range}' set for the field 'priority'")
    return False


def case_has_a_desired_outcome_code_of_blank_0_or_310(case: QuestionnaireCaseModel) -> bool:
    value_range = ["", "0", "310"]
    if case.outcome_code in value_range:
        return True

    logging.info(
        f"Case '{case.case_id}' was not eligible to be sent to totalmobile as it has a value '{case.outcome_code}' outside of the range '{value_range}' set for the field 'outcome_code'")
    return False
