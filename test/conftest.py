from typing import Dict
import pytest

from client import OptimiseClient


@pytest.fixture
def optimise_client() -> OptimiseClient:
    return OptimiseClient("http://localhost", "Test", "", "")


@pytest.fixture
def mock_auth_response() -> Dict:
    return {"access_token": "foo", "expires_in": 50}


@pytest.fixture
def mock_jobs() -> Dict:
    return {"results": [{}]}


@pytest.fixture
def mock_jobs_multi_page() -> Dict:
    return {
        "results": [{}],
        "paging": {"next": "worlds/test/jobs?pageSize=1000&pageNo=2"},
    }
