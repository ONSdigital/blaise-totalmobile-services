from dataclasses import dataclass


@dataclass
class TaskRequestModel:
    task_name: str
    task_body: bytes
