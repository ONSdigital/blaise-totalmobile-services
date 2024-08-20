from services.create.eligibility.case_filters.case_filter_wave_2 import CaseFilterWave2


class CaseFilterWave3(CaseFilterWave2):
    @property
    def wave_number(self) -> int:
        return 3
