from abc import abstractmethod
from datetime import datetime
from typing import Dict, List, Optional

from enums.blaise_fields import BlaiseFields


# TODO: This is LMS specific :@
class BlaiseCaseModel:
    def __init__(self, questionnaire_name: str, case_data: Dict[str, str]):
        self._questionnaire_name = questionnaire_name
        self._case_data = case_data

    @property
    def case_data(self):
        return self._case_data

    @property
    def questionnaire_name(self) -> str:
        return self._questionnaire_name

    @property
    def tla(self) -> str:
        return self.questionnaire_name[0:3]

    @property
    def case_id(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.case_id)

    @property
    def outcome_code(self) -> int:
        return self.convert_string_to_integer(
            self._case_data.get(BlaiseFields.outcome_code, "0")
        )

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
    def wave_com_dte(self) -> Optional[datetime]:
        wave_com_dte_str = self._case_data.get(BlaiseFields.wave_com_dte, "")
        return (
            datetime.strptime(wave_com_dte_str, "%d-%m-%Y")
            if wave_com_dte_str != ""
            else None
        )

    @property
    def address_line_1(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.address_line_1)

    @property
    def address_line_2(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.address_line_2)

    @property
    def address_line_3(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.address_line_3)

    @property
    def county(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.county)

    @property
    def town(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.town)

    @property
    def postcode(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.postcode)

    @property
    def reference(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.reference, "")

    @property
    def latitude(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.latitude)

    @property
    def longitude(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.longitude)

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
    def field_region(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.field_region)

    @property
    def field_team(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.field_team)

    @property
    def rotational_knock_to_nudge_indicator(self) -> Optional[str]:
        return self.convert_indicator_to_y_n_or_empty(
            self._case_data.get(BlaiseFields.rotational_knock_to_nudge_indicator)
        )

    @property
    def data_model_name(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.data_model_name)

    @property
    def local_auth(self) -> Optional[str]:
        return self._case_data.get(BlaiseFields.local_auth)

    @abstractmethod
    def required_fields(self) -> List:
        pass

    @staticmethod
    def convert_indicator_to_y_n_or_empty(value: Optional[str]):
        if not value or value == "":
            return ""

        return "Y" if value == "1" else "N"

    @staticmethod
    def convert_string_to_integer(value: str) -> int:
        if value == "":
            return 0
        return int(value)

    @staticmethod
    def string_to_bool(value: Optional[str]) -> bool:
        if value == "" or value is None:
            return False
        return True
