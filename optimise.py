from typing import Any, Dict, List

from base import BaseClient


class OptimiseClient(BaseClient):
    def __init__(
        this, url: str, instance: str, client_id: str, client_secret: str
    ) -> None:
        super().__init__(url, instance, client_id, client_secret)

    def create_job(this, world_id: str, job: Dict[Any, Any]) -> Dict[Any, Any]:
        return this._post(f"worlds/{world_id}/jobs", job).json()

    def get_jobs(this, world_id: str) -> List[Any]:
        return this._get_list(f"worlds/{world_id}/jobs")

    def get_worlds(this) -> List[Any]:
        return this._get("worlds").json()

    def get_world(this, world: str) -> Dict[Any, Any]:
        return this._get(f"worlds/{world}").json()

    def get_resources(this) -> List[Any]:
        return this._get("resources").json()

    def get_dispatch(this) -> List[Any]:
        return this._get("dispatch").json()

    def _get(this, path: str) -> Any:
        return super()._get(f"api/optimise/{path}")

    def _post(this, path: str, data: Any) -> Any:
        return super()._post(f"api/optimise/{path}", data)
