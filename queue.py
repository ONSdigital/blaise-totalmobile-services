from datetime import timedelta
from typing import Any
from google.cloud import tasks_v2
from google.protobuf.duration_pb2 import Duration

import asyncio
from uuid import uuid4
import json


case_file = open("cases.json")

cases = json.load(case_file)


task_client = tasks_v2.CloudTasksAsyncClient()


def name(case: Any) -> str:
    return f"{case['instrument']}{case['case']['qiD.Serial_Number']}"


async def run() -> None:
    duration = Duration()
    duration.FromTimedelta(timedelta(minutes=30))
    tasks = []
    for case in cases:
        request = tasks_v2.CreateTaskRequest(
            parent="projects/ons-blaise-v2-dev-sam8/locations/europe-west2/queues/totalmobile-test",
            task=tasks_v2.Task(
                name=f"projects/ons-blaise-v2-dev-sam8/locations/europe-west2/queues/totalmobile-test/tasks/test-{str(uuid4())}-{name(case)}",
                http_request=tasks_v2.HttpRequest(
                    http_method="POST",
                    url="https://europe-west2-ons-blaise-v2-dev-sam8.cloudfunctions.net/TestTMCreateJob",
                    body=json.dumps(case).encode(),
                    headers={
                        "Content-Type": "application/json",
                    },
                ),
                dispatch_deadline=duration,
            ),
        )
        task = task_client.create_task(request)
        tasks.append(task)

    await asyncio.gather(*tasks, return_exceptions=True)


asyncio.get_event_loop().run_until_complete(run())
