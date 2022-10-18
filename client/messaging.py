from typing import Any

import requests

from client.base import BaseClient


class MessagingClient(BaseClient):
    def __init__(self, url: str, instance: str, client_id: str, client_secret: str):
        super().__init__(url, instance, client_id, client_secret)

    def force_recall_visit(
        self, allocated_resource_reference: str, work_type: str, job_reference: str
    ) -> requests.Response:
        return self._post(
            "forcerecallvisit",
            {
                "message": {
                    "Identity": {
                        "WorkType": work_type,
                        "User": {"Name": allocated_resource_reference},
                        "Reference": job_reference,
                    },
                    "Lines": [],
                },
                "properties": {
                    "queueName": "\\TM-VI\\SEND",
                    "key": f"{allocated_resource_reference};{job_reference}",
                },
            },
        )

    def _post(self, path: str, data: Any) -> Any:
        return super()._post(f"api/messaging/{path}", data)
