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


def get_jobs_response():
    return [
        {
            "visitComplete": "True",
            "identity": {"reference": "LMS1111-AA1.12345"}
        },
        {
            "visitComplete": "False",
            "identity": {"reference": "LMS2222-BB2.22222"}
        },
        {
            "visitComplete": "False",
            "identity": {"reference": "LMS1111-AA1.67890"}
        }
    ]
