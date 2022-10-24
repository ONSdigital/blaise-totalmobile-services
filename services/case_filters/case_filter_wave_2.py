from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from services.case_filters.case_filter_base import CaseFilterBase


class CaseFilterWave2(CaseFilterBase):
    def __init__(self):
        self.valid_outcome_codes = [0, 310]
        self.valid_rotational_outcome_codes = [0, 310]

    @property
    def wave_number(self) -> int:
        return 2

    def case_is_eligible(self, case: BlaiseCaseInformationModel) -> bool:
        return (
            self.case_is_part_of_wave(self.wave_number, case)
            and self.case_has_field_case_of_y(case)
            and self.case_has_a_desired_outcome_code_of(self.valid_outcome_codes, case)
            and self.case_has_a_desired_rotational_outcome_code_of(
                self.valid_rotational_outcome_codes, case
            )
            and self.case_is_in_a_known_region(case)
            and self.case_is_eligible_if_no_telephone_numbers_are_set(case)
        )

    def case_is_eligible_if_no_telephone_numbers_are_set(
        self, case: BlaiseCaseInformationModel
    ) -> bool:
        if self.case_has_no_telephone_numbers_set(case):
            return self.case_has_rotational_knock_to_nudge_indicator_of_empty_or_n(case)

        return True

    def case_has_no_telephone_numbers_set(
        self, case: BlaiseCaseInformationModel
    ) -> bool:
        return (
            self.telephone_number_is_empty(case)
            and self.telephone_number_2_is_empty(case)
            and self.appointment_telephone_number_is_empty(case)
        )
