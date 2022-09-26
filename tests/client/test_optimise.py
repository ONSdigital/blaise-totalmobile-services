import pytest

from client import AuthException, BadRequest, ServerError


def test_create_job_returns_status_code(
    requests_mock, optimise_client, mock_auth_response
):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.post("/Test/api/optimise/worlds/test/jobs", json={})
    assert optimise_client.create_job("test", {}) == 200


def test_create_job_failing_auth_403(
    requests_mock, optimise_client, mock_auth_response
):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.post("/Test/api/optimise/worlds/test/jobs", status_code=403)
    with pytest.raises(AuthException):
        optimise_client.create_job("test", {})


def test_create_job_failing_auth_401(
    requests_mock, optimise_client, mock_auth_response
):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.post("/Test/api/optimise/worlds/test/jobs", status_code=401)
    with pytest.raises(AuthException) as err:
        optimise_client.create_job("test", {})


def test_create_job_bad_request(requests_mock, optimise_client, mock_auth_response):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.post(
        "/Test/api/optimise/worlds/test/jobs",
        status_code=400,
        text="an error thing",
    )
    with pytest.raises(BadRequest) as err:
        optimise_client.create_job("test", {})
    assert err.value.error_message == "an error thing"
    assert str(err.value) == "an error thing"


def test_create_job_bad_request_with_json(
    requests_mock, optimise_client, mock_auth_response
):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.post(
        "/Test/api/optimise/worlds/test/jobs",
        status_code=400,
        json={"duration": ["The field Duration must be between 1 and 60000."]},
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with pytest.raises(BadRequest) as err:
        optimise_client.create_job("test", {})
    assert err.value.error_details == {
        "duration": ["The field Duration must be between 1 and 60000."]
    }
    assert (
        str(err.value)
        == '{"duration": ["The field Duration must be between 1 and 60000."]}'
    )


def test_get_jobs(requests_mock, optimise_client, mock_auth_response, mock_jobs):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.get(
        "/Test/api/optimise/worlds/test/jobs?pageSize=1000", json=mock_jobs
    )
    assert optimise_client.get_jobs("test") == [{}]


def test_get_jobs_multi_page(
    requests_mock, optimise_client, mock_auth_response, mock_jobs, mock_jobs_multi_page
):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.get(
        "/Test/api/optimise/worlds/test/jobs?pageSize=1000", json=mock_jobs_multi_page
    )
    requests_mock.get(
        "/Test/api/optimise/worlds/test/jobs?pageSize=1000&pageNo=2", json=mock_jobs
    )
    assert optimise_client.get_jobs("test") == [{}, {}]


def test_get_jobs_failing_auth_403(requests_mock, optimise_client, mock_auth_response):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.get(
        "/Test/api/optimise/worlds/test/jobs?pageSize=1000", status_code=403
    )
    with pytest.raises(AuthException):
        optimise_client.get_jobs("test")


def test_get_jobs_failing_auth_401(requests_mock, optimise_client, mock_auth_response):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.get(
        "/Test/api/optimise/worlds/test/jobs?pageSize=1000", status_code=401
    )
    with pytest.raises(AuthException) as err:
        optimise_client.get_jobs("test")


def test_get_jobs_bad_request(requests_mock, optimise_client, mock_auth_response):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.get(
        "/Test/api/optimise/worlds/test/jobs?pageSize=1000",
        status_code=400,
        text="an error thing",
    )
    with pytest.raises(BadRequest) as err:
        optimise_client.get_jobs("test")
    assert err.value.error_message == "an error thing"
    assert str(err.value) == "an error thing"


def test_get_jobs_bad_request_with_json(
    requests_mock, optimise_client, mock_auth_response
):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.get(
        "/Test/api/optimise/worlds/test/jobs?pageSize=1000",
        status_code=400,
        json={"duration": ["The field Duration must be between 1 and 60000."]},
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    with pytest.raises(BadRequest) as err:
        optimise_client.get_jobs("test")
    assert err.value.error_details == {
        "duration": ["The field Duration must be between 1 and 60000."]
    }
    assert (
        str(err.value)
        == '{"duration": ["The field Duration must be between 1 and 60000."]}'
    )


def test_get_jobs_server_error(requests_mock, optimise_client, mock_auth_response):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.get(
        "/Test/api/optimise/worlds/test/jobs?pageSize=1000",
        status_code=500,
    )
    with pytest.raises(ServerError) as err:
        optimise_client.get_jobs("test")


def test_get_worlds(requests_mock, optimise_client, mock_auth_response, mock_worlds):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.get("/Test/api/optimise/worlds", json=mock_worlds)
    assert optimise_client.get_worlds() == [
        {
            "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "identity": {"reference": "test"},
            "type": "foo",
        }
    ]


def test_get_world(requests_mock, optimise_client, mock_auth_response, mock_world):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.get("/Test/api/optimise/worlds/test", json=mock_world)
    assert optimise_client.get_world("test") == {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "identity": {"reference": "test"},
        "type": "foo",
    }


def test_get_job(requests_mock, optimise_client, mock_auth_response):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.get("/Test/api/optimise/worlds/test/jobs/test-job-reference", json={})
    assert optimise_client.get_job("test", "test-job-reference") == {}


def test_get_job_properties(requests_mock, optimise_client, mock_auth_response):
    requests_mock.post("/Test/identity/connect/token", json=mock_auth_response)
    requests_mock.get(
        "/Test/api/optimise/worlds/test/jobs/test-job-reference/additionalProperties",
        json=[
            {
                "name": "study",
                "value": "LMS2202_DI1",
                "instanceId": 0,
                "additionalProperties": [],
            },
            {
                "name": "case_id",
                "value": "99999",
                "instanceId": 0,
                "additionalProperties": [],
            },
        ],
    )
    assert optimise_client.get_job_properties("test", "test-job-reference") == [
        {
            "name": "study",
            "value": "LMS2202_DI1",
            "instanceId": 0,
            "additionalProperties": [],
        },
        {
            "name": "case_id",
            "value": "99999",
            "instanceId": 0,
            "additionalProperties": [],
        },
    ]
