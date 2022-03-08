import requests
from datetime import datetime, timedelta


class BaseClient:
    def __init__(this, url: str, instance: str, client_id, client_secret):
        this._url = url
        this._instance = instance
        this._client_id = client_id
        this._client_secret = client_secret
        this.__expires_at = 0
        this.__access_token = ""

    def _get(this, path: str):
        return requests.get(
            f"{this._url}/{this._instance}/{path}",
            headers=this.__auth_header(),
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
        if this.__expires_at == 0:
            return True
        return datetime.now() >= this.__expires_at
