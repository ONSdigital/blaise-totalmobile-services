import json
from dataclasses import asdict, dataclass
from typing import Dict, TypeVar, Type

T = TypeVar('T')


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

    @classmethod
    def import_job(cls: Type[T], totalmobile_job_dictionary: Dict[str, str]) -> T:
        return TotalmobileJobModel(
            questionnaire=totalmobile_job_dictionary["questionnaire"],
            world_id=totalmobile_job_dictionary["world_id"],
            case_id=totalmobile_job_dictionary["case_id"],
            payload=totalmobile_job_dictionary["payload"]
        )
