import json
from dataclasses import asdict, dataclass
from typing import Dict, Optional, TypedDict, TypeVar
from uuid import uuid4

T = TypeVar("T", bound="TotalmobileCreateJobModel")


class TotalmobileCreateJobModelJson(TypedDict):
    questionnaire: str
    world_id: str
    case_id: str
    payload: Dict[str, str]


@dataclass
class TotalmobileCreateJobModel:
    questionnaire: str
    world_id: str
    case_id: Optional[str]
    payload: Dict[str, str]

    def as_dict(self) -> Dict:
        return asdict(self)

    def json(self) -> str:
        return json.dumps(self.as_dict())

    def create_task_name(self) -> str:
        return f"{self.questionnaire}-{self.case_id}-{str(uuid4())}"
