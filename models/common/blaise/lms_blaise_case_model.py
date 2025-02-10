from abc import abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from enums.blaise_fields import BlaiseFields
from models.common.blaise.blaise_case_model_base import BlaiseCaseModelBase


class LMSBlaiseCaseModel(BlaiseCaseModelBase):
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):
        super().__init__(questionnaire_name, case_data)

    @property
    def rotational_outcome_code(self) -> int:
        return self.convert_string_to_integer(
            self._case_data.get(BlaiseFields.rotational_outcome_code, "0")
        )

    @property
    def has_call_history(self) -> bool:
        return self.string_to_bool(self._case_data.get(BlaiseFields.call_history))

    @property
    def priority(self) -> Optional[str]:
        return str(self._case_data.get(BlaiseFields.priority))

    @property
    def wave(self) -> Optional[int]:
        wave = str(self._case_data.get(BlaiseFields.wave))
        return int(wave) if wave != "" else None

    @property
    def telephone_number_1(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.telephone_number_1)

    @property
    def telephone_number_2(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.telephone_number_2)

    @property
    def appointment_telephone_number(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.appointment_telephone_number)

    @property
    def field_case(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.field_case)

    @property
    def rotational_knock_to_nudge_indicator(self) -> Optional[str]:
        return self.convert_indicator_to_y_n_or_empty(
            self._case_data.get(BlaiseFields.rotational_knock_to_nudge_indicator)
        )

    @property
    def data_model_name(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.data_model_name)
