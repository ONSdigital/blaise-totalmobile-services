from abc import abstractmethod
from datetime import datetime
from typing import Dict, List, Optional


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
        return self._case_data.get("qiD.Serial_Number")

    @property
    def outcome_code(self) -> int:
        return self.convert_string_to_integer(self._case_data.get("hOut", "0"))

    @property
    def rotational_outcome_code(self) -> int:
        return self.convert_string_to_integer(self._case_data.get("qRotate.RHOut", "0"))

    @property
    def has_call_history(self) -> bool:
        return self.string_to_bool(
            self._case_data.get("catiMana.CatiCall.RegsCalls[1].DialResult")
        )

    @property
    def priority(self) -> Optional[str]:
        return str(self._case_data.get("qDataBag.priority"))

    @property
    def wave(self) -> Optional[int]:
        wave = str(self._case_data.get("qDataBag.Wave"))
        return int(wave) if wave != "None" else None

    @property
    def wave_com_dte(self) -> Optional[datetime]:
        wave_com_dte_str = self._case_data.get("qDataBag.WaveComDTE", "")
        return (
            datetime.strptime(wave_com_dte_str, "%d-%m-%Y")
            if wave_com_dte_str != ""
            else None
        )

    @property
    def address_line_1(self) -> Optional[str]:
        return self._case_data.get("qDataBag.Prem1")

    @property
    def address_line_2(self) -> Optional[str]:
        return self._case_data.get("qDataBag.Prem2")

    @property
    def address_line_3(self) -> Optional[str]:
        return self._case_data.get("qDataBag.Prem3")

    @property
    def county(self) -> Optional[str]:
        return self._case_data.get("qDataBag.District")

    @property
    def town(self) -> Optional[str]:
        return self._case_data.get("qDataBag.PostTown")

    @property
    def postcode(self) -> Optional[str]:
        return self._case_data.get("qDataBag.PostCode")

    @property
    def reference(self) -> Optional[str]:
        return self._case_data.get("qDataBag.UPRN", "")

    @property
    def latitude(self) -> Optional[str]:
        return self._case_data.get("qDataBag.UPRN_Latitude")

    @property
    def longitude(self) -> Optional[str]:
        return self._case_data.get("qDataBag.UPRN_Longitude")

    @property
    def telephone_number_1(self) -> Optional[str]:
        return self._case_data.get("qDataBag.TelNo")

    @property
    def telephone_number_2(self) -> Optional[str]:
        return self._case_data.get("qDataBag.TelNo2")

    @property
    def appointment_telephone_number(self) -> Optional[str]:
        return self._case_data.get("telNoAppt")

    @property
    def field_case(self) -> Optional[str]:
        return self._case_data.get("qDataBag.FieldCase")

    @property
    def field_region(self) -> Optional[str]:
        return self._case_data.get("qDataBag.FieldRegion")

    @property
    def field_team(self) -> Optional[str]:
        return self._case_data.get("qDataBag.FieldTeam")

    @property
    def rotational_knock_to_nudge_indicator(self) -> Optional[str]:
        return self.convert_indicator_to_y_n_or_empty(
            self._case_data.get("qRotate.RDMktnIND")
        )

    @property
    def data_model_name(self) -> Optional[str]:
        return self._case_data.get("dataModelName")

    @staticmethod
    @abstractmethod
    def required_fields() -> List:
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
