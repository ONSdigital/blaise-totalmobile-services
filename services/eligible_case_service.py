import logging
from typing import List

from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from services.case_filters.case_filter_base import CaseFilterBase


class EligibleCaseService:
    def __init__(self, wave_filters: List[CaseFilterBase]):
        self._wave_filters = wave_filters

    def get_eligible_cases(
        self, cases: List[BlaiseCaseInformationModel]
    ) -> List[BlaiseCaseInformationModel]:
        filtered_cases = [case for case in cases if self.case_is_eligible(case)]

        for filtered_case in filtered_cases:
            logging.info(
                f"Case '{filtered_case.case_id}' in questionnaire '{filtered_case.questionnaire_name}' was eligible and will be included"
            )

        return filtered_cases

    def case_is_eligible(self, case: BlaiseCaseInformationModel) -> bool:
        for wave_filter in self._wave_filters:
            if wave_filter.case_is_eligible(case):
                return True

        logging.info(
            f"Case '{case.case_id}' in questionnaire '{case.questionnaire_name}' has an unsupported wave {case.wave}"
        )

        return False
