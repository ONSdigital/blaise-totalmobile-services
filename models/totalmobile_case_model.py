from dataclasses import dataclass, fields
from typing import Dict, Type, TypeVar

from models.questionnaire_case_model import QuestionnaireCaseModel
from models.uac_model import UacChunks, UacModel

T = TypeVar('T')


@dataclass
class Identity:
    reference: str


@dataclass
class TotalMobileCaseModel:
    identity: Identity
    description: str
    origin: str
    duration: int
    workType: str


    @classmethod
    def import_questionnaire_case_data(cls: Type[T], questionnaire_case: QuestionnaireCaseModel) -> T:
        return TotalMobileCaseModel(
        )
