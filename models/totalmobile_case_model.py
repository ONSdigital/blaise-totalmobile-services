from dataclasses import dataclass, fields
from typing import Dict, Type, TypeVar
from models.uac_model import UacChunks, UacModel

T = TypeVar('T')


@dataclass
class TotalMobileCaseModel:
    case_id: str

    uac_chunks: UacChunks


    @classmethod
    def import_questionnaire_case_data(cls: Type[T], case_data_dictionary: Dict[str, str]) -> T:
        return TotalMobileCaseModel(
            case_id=case_data_dictionary.get("qiD.Serial_Number"),
            uac_chunks=UacChunks(uac1='', uac2='', uac3='')
        )
