from datetime import datetime, timedelta
from typing import Any, List

import requests
import json

from client.errors import AuthException, BadRequest, ServerError


class BaseClient:
    def __init__(
        self, url: str, instance: str, client_id: str, client_secret: str
    ) -> None:
        self._url = url
        self._instance = instance
        self._client_id = client_id
        self._client_secret = client_secret
        self.__access_token = ""
        self.__expires_at = datetime.now()

    def _get(self, path: str) -> requests.Response:
        response = requests.get(
            f"{self._url}/{self._instance}/{path}",
            headers=self.__auth_header(),
        )
        self.__check_response(response)
        return response

    def _get_list(self, path: str, results: List[Any] = []) -> List[Any]:
        response = self._get(path).json()
        results = results + response["results"]
        if (
            "paging" in response
            and "next" in response["paging"]
            and response["paging"]["next"] is not None
        ):
            return self._get_list(response["paging"]["next"], results)
        return results

    def _post(self, path: str, data: Any) -> requests.Response:
        response = requests.post(
            f"{self._url}/{self._instance}/{path}",
            headers=self.__auth_header(),
            json=data,
        )
        self.__check_response(response)
        return response

    def _delete(self, path: str, reason: str) -> requests.Response:
        response = requests.delete(
            f"{self._url}/{self._instance}/{path}",
            headers=self.__auth_header(),
            json={"deletionReason": {"reference": reason}}
        )
        self.__check_response(response)
        return response

    def __get_token(self) -> str:
        if self.__token_expired():
            response = requests.post(
                f"{self._url}/{self._instance}/identity/connect/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": self._client_id,
                    "client_secret": self._client_secret,
                    "scope": "optimiseApi",
                },
            )
            access_token = response.json()
            self.__access_token = access_token["access_token"]
            self.__expires_at = datetime.now() + timedelta(
                0, access_token["expires_in"]
            )
        return self.__access_token

    def __auth_header(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.__get_token()}"}

    def __token_expired(self) -> bool:
        return datetime.now() >= self.__expires_at

    def __check_response(self, response: requests.Response) -> None:
        if response.status_code == 500:
            raise ServerError
        if response.status_code in [401, 403]:
            raise AuthException
        if response.status_code == 400:
            if "application/json" in response.headers.get("Content-Type", ""):
                raise BadRequest(error_details=response.json())
            raise BadRequest(error_message=response.text)
