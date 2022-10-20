from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from services.case_filters.case_filter_base import CaseFilterBase


class CaseFilterWave2(CaseFilterBase):

    @property
    def wave_number(self) -> int:
        return 2

    def case_is_eligible(self, case: BlaiseCaseInformationModel) -> bool:
        return (
                self.case_is_part_of_wave(self.wave_number, case)
                and self.telephone_number_is_empty(case)
                and self.telephone_number_2_is_empty(case)
                and self.appointment_telephone_number_is_empty(case)
                and self.case_has_field_case_of_y(case)
        )