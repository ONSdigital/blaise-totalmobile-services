from dataclasses import dataclass
from typing import Dict, Type, TypeVar

from client.bus import Uac

T = TypeVar("T", bound="QuestionnaireUacModel")


@dataclass
class UacChunks:
    uac1: str
    uac2: str
    uac3: str


@dataclass
class QuestionnaireUacModel:
    questionnaire_case_uacs: Dict[str, UacChunks]

    @classmethod
    def import_uac_data(cls: Type[T], uac_data_dictionary: Dict[str, Uac]) -> T:

        _questionnaire_case_uacs: Dict[str, UacChunks] = {}
        for item in uac_data_dictionary:
            _questionnaire_case_uacs[item] = UacChunks(
                uac1=uac_data_dictionary[item]["uac_chunks"]["uac1"],
                uac2=uac_data_dictionary[item]["uac_chunks"]["uac2"],
                uac3=uac_data_dictionary[item]["uac_chunks"]["uac3"],
            )

        return cls(_questionnaire_case_uacs)
