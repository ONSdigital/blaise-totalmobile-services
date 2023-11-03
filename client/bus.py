from typing import Any, Dict, Optional, TypedDict

import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token


class UacChunks(TypedDict):
    uac1: str
    uac2: str
    uac3: str
    uac4: Optional[str]


class Uac(TypedDict):  # type: ignore
    instrument_name: str
    case_id: str
    uac_chunks: UacChunks
    full_uac: str


GetUacsResponse = Dict[str, Uac]


class BusClient:
    def __init__(self, url: str, client_id: str) -> None:
        self._url = url
        self.__client_id = client_id

    def get_uacs_by_case_id(self, instrument_name: str) -> GetUacsResponse:
        return self.__get(f"uacs/instrument/{instrument_name}/bycaseid").json()

    def __get(self, path: str) -> Any:
        return requests.get(
            f"{self._url}/{path}",
            headers={"Authorization": f"Bearer {self.__get_token()}"},
        )

    def __get_token(self) -> str:
        return id_token.fetch_id_token(Request(), self.__client_id)
