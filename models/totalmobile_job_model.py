import json
from dataclasses import asdict, dataclass
from typing import Dict
from models.questionnaire_case_model import QuestionnaireCaseModel


@dataclass
class TotalmobileJobModel:
    questionnaire: str
    world_id: str
    case: QuestionnaireCaseModel

    def as_dict(self) -> Dict:
        return asdict(self)

    def json(self) -> str:
        return json.dumps(self.as_dict())
