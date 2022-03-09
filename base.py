from datetime import datetime, timedelta
from typing import Any, List

import requests


class BaseClient:
    def __init__(
        this, url: str, instance: str, client_id: str, client_secret: str
    ) -> None:
        this._url = url
        this._instance = instance
        this._client_id = client_id
        this._client_secret = client_secret
        this.__access_token = ""
        this.__expires_at = datetime.now()

    def _get(this, path: str) -> requests.Response:
        return requests.get(
            f"{this._url}/{this._instance}/{path}",
            headers=this.__auth_header(),
        )

    def _get_list(this, path: str, results: List[Any] = []) -> List[Any]:
        response = this._get(path).json()
        results = results + response["results"]
        if (
            "paging" in response
            and "next" in response["paging"]
            and response["paging"]["next"] is not None
        ):
            return this._get_list(response["paging"]["next"], results)
        return results

    def _post(this, path: str, data: Any) -> requests.Response:
        return requests.post(
            f"{this._url}/{this._instance}/{path}",
            headers=this.__auth_header(),
            json=data,
        )

    def __get_token(this) -> str:
        if this.__token_expired():
            response = requests.post(
                f"{this._url}/{this._instance}/identity/connect/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": this._client_id,
                    "client_secret": this._client_secret,
                    "scope": "optimiseApi",
                },
            )
            access_token = response.json()
            this.__access_token = access_token["access_token"]
            this.__expires_at = datetime.now() + timedelta(access_token["expires_in"])
        return this.__access_token

    def __auth_header(this) -> dict[str, str]:
        return {"Authorization": f"Bearer {this.__get_token()}"}

    def __token_expired(this) -> bool:
        return datetime.now() >= this.__expires_at
