import logging
from typing import List

from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel


def get_eligible_cases(
    cases: List[BlaiseCaseInformationModel],
) -> List[BlaiseCaseInformationModel]:
    filtered_cases = [
        case
        for case in cases
        if (
            telephone_number_is_empty(case)
            and telephone_number_2_is_empty(case)
            and appointment_telephone_number_is_empty(case)
            and case_is_part_of_wave_1(case)
            and case_has_field_case_of_y(case)
            and case_has_a_desired_outcome_code_of_0_or_310_or_320(case)
            and case_is_in_a_known_region(case)
        )
    ]

    for filtered_case in filtered_cases:
        logging.info(
            f"Case '{filtered_case.case_id}' in questionnaire '{filtered_case.questionnaire_name}' was eligible and will be included"
        )

    return filtered_cases


def telephone_number_is_empty(case: BlaiseCaseInformationModel) -> bool:
    if case.contact_details.telephone_number_1 == "":
        return True

    logging.info(
        f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_1'"
    )
    return False


def telephone_number_2_is_empty(case: BlaiseCaseInformationModel) -> bool:
    if case.contact_details.telephone_number_2 == "":
        return True

    logging.info(
        f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_2'"
    )
    return False


def appointment_telephone_number_is_empty(case: BlaiseCaseInformationModel) -> bool:
    if case.contact_details.appointment_telephone_number == "":
        return True

    logging.info(
        f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value set for the field 'appointment_telephone_number'"
    )
    return False


def case_is_part_of_wave_1(case: BlaiseCaseInformationModel) -> bool:
    value_range = ["1"]
    if case.wave in value_range:
        return True

    logging.info(
        f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value '{case.wave}' outside of the range '{value_range}' set for the field 'wave'"
    )
    return False


def case_has_field_case_of_y(case: BlaiseCaseInformationModel) -> bool:
    if case.field_case == "Y" or case.field_case == "y":
        return True

    logging.info(
        f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a field case value of '{case.field_case}', not 'Y'"
    )
    return False


def case_has_a_desired_outcome_code_of_0_or_310_or_320(
    case: BlaiseCaseInformationModel,
) -> bool:
    value_range = [0, 310, 320]
    if case.outcome_code in value_range:
        return True

    logging.info(
        f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value '{case.outcome_code}' outside of the range '{value_range}' set for the field 'outcome_code'"
    )
    return False


def case_is_in_a_known_region(case: BlaiseCaseInformationModel) -> bool:
    value_range = TotalmobileWorldModel.get_available_regions()
    if case.field_region in value_range:
        return True

    logging.info(
        f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value '{case.field_region}' outside of the range '{value_range}' set for the field 'field_region'"
    )
    return False
