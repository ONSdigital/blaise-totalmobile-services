from services.create.eligibility.case_filters.case_filter_wave_4 import CaseFilterWave4


class CaseFilterWave5(CaseFilterWave4):
    @property
    def wave_number(self) -> int:
        return 5
