import pytest

from client import AuthException, BadRequest


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
