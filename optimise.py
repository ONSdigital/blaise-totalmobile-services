from datetime import datetime, timedelta
import requests


class OptimiseClient:
    def __init__(this, url: str, instance: str, client_id, client_secret):
        this.url = url
        this.instance = instance
        this.client_id = client_id
        this.client_secret = client_secret
        this.expires_at = 0
        this.access_token = ""

    def get_jobs(this, world_id: str):
        return this.__get(f"worlds/{world_id}/jobs").json()

    def get_worlds(this):
        return this.__get("worlds").json()

    def get_world(this, world: str):
        return this.__get(f"worlds/{world}").json()

    def __get(this, path: str):
        return requests.get(
            f"{this.url}/{this.instance}/api/optimise/{path}",
            headers={"Authorization": f"Bearer {this.__get_token()}"},
        )

    def __get_token(this) -> str:
        if this.__token_expired():
            response = requests.post(
                f"{this.url}/{this.instance}/identity/connect/token",
                data={
                    "grant_type": "client_credentials",
                    "client_id": this.client_id,
                    "client_secret": this.client_secret,
                    "scope": "optimiseApi",
                },
            )
            access_token = response.json()
            this.access_token = access_token["access_token"]
            this.expires_at = datetime.now() + timedelta(access_token["expires_in"])
        return this.access_token

    def __token_expired(this) -> bool:
        if this.expires_at == 0:
            return True
        return datetime.now() >= this.expires_at
