from dataclasses import dataclass
from typing import Dict, Type, TypeVar

from client.bus import Uac

T = TypeVar("T", bound="UacModel")


@dataclass
class UacChunks:
    uac1: str
    uac2: str
    uac3: str


@dataclass
class UacModel:
    case_id: str
    uac_chunks: UacChunks

    @classmethod
    def import_uac_data(cls: Type[T], uac_data_dictionary: Uac) -> T:
        print(uac_data_dictionary)
        return cls(
            case_id=uac_data_dictionary["case_id"],
            uac_chunks=UacChunks(
                uac1=uac_data_dictionary["uac_chunks"]["uac1"],
                uac2=uac_data_dictionary["uac_chunks"]["uac2"],
                uac3=uac_data_dictionary["uac_chunks"]["uac3"],
            ),
        )
