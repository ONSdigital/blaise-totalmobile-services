import json

from dataclasses import asdict, dataclass
from typing import Dict


@dataclass
class QuestionnaireCaseTaskModel:
    questionnaire: str

    def as_dict(self) -> Dict:
        return asdict(self)

    def json(self) -> str:
        return json.dumps(self.as_dict())