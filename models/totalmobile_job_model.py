import json
from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class TotalmobileJobModel:
    questionnaire: str
    world_id: str
    case_id: str
    payload: Dict[str, str]

    def as_dict(self) -> Dict:
        return asdict(self)

    def json(self) -> str:
        return json.dumps(self.as_dict())