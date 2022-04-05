from typing import Any, Dict

import requests
from google.auth.transport.requests import Request
from google.oauth2 import id_token


class BusClient:
    def __init__(self, url: str, client_id: str) -> None:
        self._url = url
        self.__client_id = client_id

    def get_uacs_by_case_id(self, instrument_name: str) -> Dict[str, Any]:
        return self.__get(f"uacs/instrument/{instrument_name}/bycaseid").json()

    def __get(self, path: str) -> Any:
        return requests.get(
            f"{self._url}/{path}",
            headers={"Authorization": f"Bearer {self.__get_token()}"},
        )

    def __get_token(self) -> str:
        return id_token.fetch_id_token(Request(), self.__client_id)
