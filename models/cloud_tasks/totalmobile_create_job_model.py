import json
from dataclasses import asdict, dataclass
from typing import Dict, Optional, Type, TypedDict, TypeVar
from uuid import uuid4

T = TypeVar("T", bound="TotalmobileCreateJobModel")


class TotalmobileCreateJob(TypedDict):
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

    @classmethod
    def import_job(cls: Type[T], totalmobile_job_dictionary: TotalmobileCreateJob) -> T:
        return cls(
            questionnaire=totalmobile_job_dictionary["questionnaire"],
            world_id=totalmobile_job_dictionary["world_id"],
            case_id=totalmobile_job_dictionary["case_id"],
            payload=totalmobile_job_dictionary["payload"],
        )
