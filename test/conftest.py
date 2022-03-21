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


@pytest.fixture
def mock_create_job_task() -> Dict:
    return {
        "instrument": "DST2101A",
        "world_id": "test-world-id",
        "case": {
            "qiD.Serial_Number": "100100",
            "qDataBag.Prem1": "prem1",
            "qDataBag.Prem2": "prem2",
            "qDataBag.Prem3": "prem3",
            "qDataBag.PostTown": "PostTown",
            "qDataBag.PostCode": "PostCode",
            "qDataBag.UPRN_Latitude": "UPRN_Latitude",
            "qDataBag.UPRN_Longitude": "UPRN_Longitude",
            "qDataBag.TelNo": "TelNo",
            "qDataBag.TelNo2": "TelNo2",
        },
    }
