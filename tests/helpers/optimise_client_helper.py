from datetime import datetime
from typing import List

from client.optimise import DueDate, GetJobResponse, Identity
from tests.helpers.date_helper import format_date_as_totalmobile_formatted_string


def get_worlds_response():
    return [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {"reference": "Region 1"},
            "type": "foo",
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa7",
            "identity": {"reference": "Region 2"},
            "type": "foo",
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa8",
            "identity": {"reference": "Region 3"},
            "type": "foo",
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa9",
            "identity": {"reference": "Region 4"},
            "type": "foo",
        },
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa2",
            "identity": {"reference": "Region 5"},
            "type": "foo",
        },
    ]


def get_jobs_response(due_date: datetime = datetime.today()) -> List[GetJobResponse]:
    return [
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.12345"),
            dueDate=DueDate(end=format_date_as_totalmobile_formatted_string(due_date)),
            visitComplete=True,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS2222-BB2.22222"),
            dueDate=DueDate(end=format_date_as_totalmobile_formatted_string(due_date)),
            visitComplete=False,
            allocatedResource=None,
            workType="LMS",
        ),
        GetJobResponse(
            identity=Identity(reference="LMS1111-AA1.67890"),
            dueDate=DueDate(end=format_date_as_totalmobile_formatted_string(due_date)),
            visitComplete=False,
            allocatedResource=None,
            workType="LMS",
        ),
    ]
