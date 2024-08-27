import logging
from typing import List

from models.create.blaise.blaiise_lms_create_case_model import BlaiseLMSCreateCaseModel
from services.create.eligibility.case_filters.case_filter_base import CaseFilterBase


class LMSEligibleCaseService:
    def __init__(self, wave_filters: List[CaseFilterBase]):
        self._wave_filters = wave_filters

    def get_eligible_cases(
        self, cases: List[BlaiseLMSCreateCaseModel]
    ) -> List[BlaiseLMSCreateCaseModel]:
        filtered_cases = [case for case in cases if self.case_is_eligible(case)]

        for filtered_case in filtered_cases:
            logging.info(
                f"Case '{filtered_case.case_id}' in questionnaire '{filtered_case.questionnaire_name}' was eligible and will be included"
            )

        return filtered_cases

    def case_is_eligible(self, case: BlaiseLMSCreateCaseModel) -> bool:
        for wave_filter in self._wave_filters:
            if wave_filter.case_is_eligible(case):
                return True

        return False
