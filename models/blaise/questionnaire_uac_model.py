from dataclasses import dataclass
from typing import Dict, Optional, Type, TypeVar

from client.bus import Uac

T = TypeVar("T", bound="QuestionnaireUacModel")


@dataclass
class UacChunks:
    uac1: str
    uac2: str
    uac3: str
    uac4: Optional[str] = None

    def formatted_chunks(self) -> str:
        uacs = [self.uac1, self.uac2, self.uac3]
        if self.uac4:
            uacs.append(self.uac4)
        return " ".join(uacs)


@dataclass
class QuestionnaireUacModel:
    questionnaire_case_uacs: Dict[str, UacChunks]

    def get_uac_chunks(self, case_id: Optional[str]):
        if not case_id or case_id not in self.questionnaire_case_uacs.keys():
            return None

        return self.questionnaire_case_uacs[case_id]

    @classmethod
    def import_uac_data(cls: Type[T], uac_data_dictionary: Dict[str, Uac]) -> T:
        _questionnaire_case_uacs: Dict[str, UacChunks] = {
            item: UacChunks(
                uac1=data["uac_chunks"]["uac1"],
                uac2=data["uac_chunks"]["uac2"],
                uac3=data["uac_chunks"]["uac3"],
                uac4=data["uac_chunks"].get("uac4"),
            )
            for item, data in uac_data_dictionary.items()
        }

        return cls(_questionnaire_case_uacs)
