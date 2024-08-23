from typing import Dict, Optional


class BlaiseCase:
    def __init__(self, case_data: Dict[str, str]):
        self._case_data = case_data

    @property
    def case_data(self):
        return self._case_data

    @property
    def case_id(self) -> Optional[str]:
        return self._case_data.get("qiD.Serial_Number")

    @property
    def outcome_code(self) -> int:
        return self.convert_string_to_integer(self._case_data.get("hOut", "0"))

    @property
    def has_call_history(self) -> bool:
        return self.string_to_bool(
            self._case_data.get("catiMana.CatiCall.RegsCalls[1].DialResult")
        )

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
