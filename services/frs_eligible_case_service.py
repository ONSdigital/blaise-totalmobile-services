import logging
from typing import List

from models.blaise.blaise_frs_case_information_model import (
    BlaiseFRSCaseInformationModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel


class FRSEligibleCaseService:
    def get_eligible_cases(
        self, cases: List[BlaiseFRSCaseInformationModel]
    ) -> List[BlaiseFRSCaseInformationModel]:
        logging.info(f"DEBUG: FRSEligibleCaseService.get_eligible_cases() called")

        filtered_cases = [case for case in cases if self.case_is_eligible(case)]
        logging.info(f"DEBUG: filtered_cases: {filtered_cases}")

        for filtered_case in filtered_cases:
            logging.info(
                f"Case '{filtered_case.case_id}' in questionnaire '{filtered_case.questionnaire_name}' was eligible and will be included"
            )

        return filtered_cases

    def case_is_eligible(self, case: BlaiseFRSCaseInformationModel) -> bool:
        return self.case_is_in_a_known_region(case)

    @staticmethod
    def case_is_in_a_known_region(case: BlaiseFRSCaseInformationModel) -> bool:
        value_range = TotalmobileWorldModel.get_available_regions()
        if case.field_region in value_range:
            return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' was not eligible to be sent to Totalmobile as it has a value '{case.field_region}' outside of the range '{value_range}' set for the field 'field_region'"
        )
        return False
