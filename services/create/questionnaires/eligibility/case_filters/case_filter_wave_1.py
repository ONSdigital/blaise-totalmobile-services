from models.create.blaise.blaiise_lms_create_case_model import BlaiseLMSCreateCaseModel
from services.create.questionnaires.eligibility.case_filters.case_filter_base import (
    CaseFilterBase,
)


class CaseFilterWave1(CaseFilterBase):
    def __init__(self):
        self.valid_outcome_codes = [0, 310, 320]

    @property
    def wave_number(self) -> int:
        return 1

    def case_is_eligible_additional_checks(
        self, case: BlaiseLMSCreateCaseModel
    ) -> bool:
        return (
            self.telephone_number_1_is_empty(case)
            and self.telephone_number_2_is_empty(case)
            and self.appointment_telephone_number_is_empty(case)
            and self.case_has_field_case_of_y(case)
            and self.case_has_a_desired_outcome_code_of(self.valid_outcome_codes, case)
        )
