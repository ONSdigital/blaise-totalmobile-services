import json

from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class TotalmobileJobModel:
    instrument: str
    world_id: str
    case: dict

    def as_dict(self) -> Dict:
        return asdict(self)

    def json(self) -> str:
        return json.dumps(self.as_dict())
