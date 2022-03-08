from typing import Any, Dict, List

from base import BaseClient


class OptimiseClient(BaseClient):
    def __init__(
        this, url: str, instance: str, client_id: str, client_secret: str
    ) -> None:
        super().__init__(url, instance, client_id, client_secret)

    def get_jobs(this, world_id: str) -> List[Any]:
        return this._get(f"worlds/{world_id}/jobs").json()

    def get_worlds(this) -> List[Any]:
        return this._get("worlds").json()

    def get_world(this, world: str) -> Dict[Any, Any]:
        return this._get(f"worlds/{world}").json()

    def _get(this, path: str) -> Any:
        return super()._get(f"api/optimise/{path}")
