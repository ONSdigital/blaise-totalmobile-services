from datetime import datetime, timedelta
import requests

from base import BaseClient


class OptimiseClient(BaseClient):
    def __init__(this, url: str, instance: str, client_id, client_secret):
        this._url = url
        this._instance = instance
        super().__init__(this._url, this._instance, client_id, client_secret)

    def get_jobs(this, world_id: str):
        return this._get(f"worlds/{world_id}/jobs").json()

    def get_worlds(this):
        return this._get("worlds").json()

    def get_world(this, world: str):
        return this._get(f"worlds/{world}").json()

    def _get(this, path: str):
        return super()._get(f"api/optimise/{path}")
