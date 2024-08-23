from models.create.blaise.blaiise_lms_case_model import BlaiseLMSCaseModel
from services.create.eligibility.case_filters.case_filter_base import CaseFilterBase


class CaseFilterWave2(CaseFilterBase):
    def __init__(self):
        self.valid_outcome_codes = [0, 310, 320]
        self.valid_rotational_outcome_codes = [0, 310, 320]

    @property
    def wave_number(self) -> int:
        return 2

    def case_is_eligible_additional_checks(self, case: BlaiseLMSCaseModel) -> bool:
        return (
            self.case_has_field_case_of_y(case)
            and self.case_has_a_desired_outcome_code_of(self.valid_outcome_codes, case)
            and self.case_has_a_desired_rotational_outcome_code_of(
                self.valid_rotational_outcome_codes, case
            )
            and self.case_has_rotational_knock_to_nudge_indicator_of_empty_or_n(case)
        )
