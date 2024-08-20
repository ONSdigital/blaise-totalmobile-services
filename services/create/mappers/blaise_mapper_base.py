from typing import Dict, Optional


class MapperServiceBase:
    @staticmethod
    def get_case_id(case_data: Dict[str, str]) -> Optional[str]:
        return case_data.get("qiD.Serial_Number")

    @staticmethod
    def get_outcome_code(case_data: Dict[str, str]) -> int:
        return MapperServiceBase.convert_string_to_integer(case_data.get("hOut", "0"))

    @staticmethod
    def has_call_history(case_data: Dict[str, str]) -> bool:
        return MapperServiceBase.string_to_bool(
            case_data.get("catiMana.CatiCall.RegsCalls[1].DialResult")
        )

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
