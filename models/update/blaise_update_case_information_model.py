from dataclasses import dataclass
from typing import List, Optional

from models.base_model import BaseModel


@dataclass  # type: ignore #seems to be an issue with dataclass inheritance
class BlaiseUpdateCaseInformationModel(BaseModel):
    case_id: Optional[str]
    outcome_code: int
    has_call_history: bool

    @staticmethod
    def required_fields() -> List:
        return [
            "qiD.Serial_Number",
            "hOut",
            "catiMana.CatiCall.RegsCalls[1].DialResult",
        ]
