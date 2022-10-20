from urllib.parse import parse_qs

import pytest

from client.messaging import MessagingClient


class TestForceRecallVisit:
    @pytest.fixture()
    def access_token(self) -> str:
        return "abc123"

    @pytest.fixture(autouse=True)
    def setup_auth_endpoint(self, requests_mock, access_token) -> None:
        requests_mock.post(
            "http://totalmobile.com/instance1/identity/connect/token",
            status_code=200,
            json=dict(access_token=access_token, expires_in=60),
        )

    @pytest.fixture(autouse=True)
    def setup_endpoint(self, requests_mock):
        requests_mock.post(
            "http://totalmobile.com/instance1/api/messaging/forcerecallvisit",
            status_code=201,
        )

    @pytest.fixture()
    def client(self) -> MessagingClient:
        return MessagingClient(
            url="http://totalmobile.com",
            instance="instance1",
            client_id="client1",
            client_secret="topsecret",
        )

    def test_requests_scope(self, requests_mock, access_token, client):
        client.force_recall_visit("richmond.rice", "LMS", "LMS2208-AA1.12345")
        auth_token_call = requests_mock.request_history[0]
        assert parse_qs(auth_token_call.text) == dict(
            client_id=["client1"],
            client_secret=["topsecret"],
            grant_type=["client_credentials"],
            scope=["messagingApi"],
        )

    def test_sends_access_token(self, requests_mock, access_token, client):
        client.force_recall_visit("richmond.rice", "LMS", "LMS2208-AA1.12345")
        assert (
            requests_mock.last_request.headers["Authorization"]
            == f"Bearer {access_token}"
        )

    def test_returns_the_response(self, client):
        response = client.force_recall_visit(
            "richmond.rice", "LMS", "LMS2208-AA1.12345"
        )
        assert response.status_code is 201

    def test_posts_the_data(self, client, requests_mock):
        client.force_recall_visit("richmond.rice", "LMS", "LMS2208-AA1.12345")
        assert requests_mock.last_request.json() == {
            "message": {
                "Identity": {
                    "WorkType": "LMS",
                    "User": {"Name": "richmond.rice"},
                    "Reference": "LMS2208-AA1.12345",
                },
                "Lines": [],
            },
            "properties": {
                "queueName": "\\TM-VI\\SEND",
                "key": "richmond.rice;LMS2208-AA1.12345",
            },
        }
