from typing import Any, Dict, List, Union

import requests

from client.base import BaseClient


class OptimiseClient(BaseClient):
    def __init__(
            self, url: str, instance: str, client_id: str, client_secret: str
    ) -> None:
        super().__init__(url, instance, client_id, client_secret)

    def create_job(self, world_id: str, job: Dict[Any, Any]) -> requests.Response:
        return self._post(f"worlds/{world_id}/jobs", job).json()

    def delete_job(self, world_id: str, job: str) -> requests.Response:
        return self._delete(f"worlds/{world_id}/jobs/{job}")

    def get_jobs(self, world_id: str) -> List[Any]:
        return self._get_list(f"worlds/{world_id}/jobs?pageSize=1000")

    def get_job(self, world_id: str, job_reference: str) -> Dict[Any, Any]:
        return self._get(f"worlds/{world_id}/jobs/{job_reference}").json()

    def get_job_properties(self, world_id: str, job_reference: str) -> Dict[Any, Any]:
        return self._get(
            f"worlds/{world_id}/jobs/{job_reference}/additionalProperties"
        ).json()

    def get_worlds(self) -> Dict[str, Union[str, Dict[str, str]]]:
        return self._get("worlds").json()

    def get_world(self, world: str) -> Dict[Any, Any]:
        return self._get(f"worlds/{world}").json()

    def _get(self, path: str) -> Any:
        return super()._get(f"api/optimise/{path}")

    def _post(self, path: str, data: Any) -> Any:
        return super()._post(f"api/optimise/{path}", data)
