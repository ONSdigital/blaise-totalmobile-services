import logging
from typing import Tuple
from unittest.mock import create_autospec

import pytest
import requests

from client.optimise import GetJobsResponse
from models.common.totalmobile.totalmobile_world_model import (
    TotalmobileWorldModel,
    World,
)
from models.create.totalmobile.totalmobile_create_job_model import (
    TotalmobileCreateJobModel,
)
from models.delete.totalmobile_get_jobs_response_model import (
    Job,
    TotalmobileGetJobsResponseModel,
)
from services.logging_totalmobile_service import LoggingTotalmobileService
from services.totalmobile_service import TotalmobileService


@pytest.fixture()
def inner_service() -> TotalmobileService:
    return create_autospec(TotalmobileService)


@pytest.fixture()
def logging_service(inner_service) -> TotalmobileService:
    return LoggingTotalmobileService(inner_service)


class TestGetWorldModel:
    @pytest.fixture()
    def returned_model(self) -> TotalmobileWorldModel:
        return TotalmobileWorldModel(
            worlds=[World(region="Region 1", id="a5c89c96-862f-4dd8-9780-2b56497e1aba")]
        )

    @pytest.fixture(autouse=True)
    def setup(self, inner_service, returned_model) -> None:
        inner_service.get_world_model.return_value = returned_model

    def test_delegates_call_to_inner_service(self, inner_service, logging_service):
        logging_service.get_world_model()
        inner_service.get_world_model.assert_called_with()

    def test_returns_the_result(self, logging_service, returned_model):
        result = logging_service.get_world_model()
        assert result == returned_model


class TestCreateJob:
    @pytest.fixture()
    def returned_response(self):
        response = requests.Response()
        response.status_code = 404
        return response

    @pytest.fixture()
    def args(self) -> Tuple[TotalmobileCreateJobModel]:
        return (
            TotalmobileCreateJobModel(
                questionnaire="LMS2202",
                world_id="005c87ca-d2b9-4891-bb22-cd568d01ea3e",
                case_id=None,
                payload={},
            ),
        )

    @pytest.fixture(autouse=True)
    def setup(self, inner_service, returned_response):
        inner_service.create_job.return_value = returned_response

    def test_delegates_call_to_inner_service(
        self, logging_service, inner_service, args
    ):
        logging_service.create_job(*args)
        inner_service.create_job.assert_called_with(*args)

    def test_returns_the_result(self, returned_response, logging_service, args):
        result = logging_service.create_job(*args)
        assert result == returned_response


class TestRecallJob:
    @pytest.fixture()
    def args(self) -> Tuple[str, str, str]:
        return "norbert.minion", "LMS", "LMS2209-AA1.12345"

    def test_delegates_call_to_inner_service(
        self, logging_service, inner_service, args
    ):
        logging_service.recall_job(*args)
        inner_service.recall_job.assert_called_with(*args)

    def test_logs_success(self, logging_service, args, caplog):
        with caplog.at_level(logging.INFO):
            logging_service.recall_job(*args)

        assert (
            "root",
            logging.INFO,
            "Successfully recalled job LMS2209-AA1.12345 from norbert.minion on Totalmobile",
        ) in caplog.record_tuples
        assert (
            "root",
            logging.ERROR,
            "Failed to recall job LMS2209-AA1.12345 from norbert.minion on Totalmobile",
        ) not in caplog.record_tuples

    def test_logs_failure(self, inner_service, logging_service, args, caplog):
        inner_service.recall_job.side_effect = Exception("A bad thing happened")

        with pytest.raises(Exception, match="A bad thing happened"):
            with caplog.at_level(logging.INFO):
                logging_service.recall_job(*args)

        assert (
            "root",
            logging.INFO,
            "Successfully recalled job LMS2209-AA1.12345 from norbert.minion on Totalmobile",
        ) not in caplog.record_tuples
        assert (
            "root",
            logging.ERROR,
            "Failed to recall job LMS2209-AA1.12345 from norbert.minion on Totalmobile",
        ) in caplog.record_tuples


class TestDeleteJob:
    @pytest.fixture()
    def returned_response(self):
        response = requests.Response()
        response.status_code = 404
        return response

    @pytest.fixture()
    def args(self) -> Tuple[str, str, str]:
        return "world-id-1", "LMS2209-AA1.12345", "example reason"

    @pytest.fixture(autouse=True)
    def setup(self, inner_service, returned_response):
        inner_service.delete_job.return_value = returned_response

    def test_delegates_call_to_inner_service(
        self, logging_service, inner_service, args
    ):
        logging_service.delete_job(*args)
        inner_service.delete_job.assert_called_with(*args)

    def test_defaults_reason_to_the_string_0(
        self, logging_service, inner_service, args
    ):
        logging_service.delete_job("world-id-x", "LMS2201-BB1.12345")
        inner_service.delete_job.assert_called_with(
            "world-id-x", "LMS2201-BB1.12345", "0"
        )

    def test_returns_the_result(self, returned_response, logging_service, args):
        result = logging_service.delete_job(*args)
        assert result == returned_response

    def test_logs_success(self, logging_service, args, caplog):
        with caplog.at_level(logging.INFO):
            logging_service.delete_job(*args)
        assert (
            "root",
            logging.INFO,
            "Successfully removed job LMS2209-AA1.12345 from Totalmobile",
        ) in caplog.record_tuples
        assert (
            "root",
            logging.ERROR,
            "Unable to delete job reference 'LMS2209-AA1.12345` from Totalmobile",
        ) not in caplog.record_tuples

    def test_logs_failure(self, inner_service, logging_service, args, caplog):
        inner_service.delete_job.side_effect = Exception("A bad thing happened")

        with pytest.raises(Exception, match="A bad thing happened"):
            with caplog.at_level(logging.INFO):
                logging_service.delete_job(*args)

        assert (
            "root",
            logging.INFO,
            "Successfully removed job LMS2209-AA1.12345 from Totalmobile",
        ) not in caplog.record_tuples
        assert (
            "root",
            logging.ERROR,
            "Unable to delete job reference 'LMS2209-AA1.12345` from Totalmobile",
        ) in caplog.record_tuples


class TestGetJobs:
    @pytest.fixture()
    def returned_response(self) -> GetJobsResponse:
        return [
            dict(
                identity=dict(reference="d0be91fe-c48f-438e-b2f8-ca10f4f3570f"),
                dueDate=dict(end="2022-10-30"),
                visitComplete=True,
                allocatedResource=None,
                workType="LMS",
            )
        ]

    @pytest.fixture()
    def args(self) -> Tuple[str]:
        return ("world-id-1",)

    @pytest.fixture(autouse=True)
    def setup(self, inner_service, returned_response):
        inner_service.get_jobs.return_value = returned_response

    def test_delegates_call_to_inner_service(
        self, logging_service, inner_service, args
    ):
        logging_service.get_jobs(*args)
        inner_service.get_jobs.assert_called_with(*args)

    def test_returns_the_result(self, returned_response, logging_service, args):
        result = logging_service.get_jobs(*args)
        assert result == returned_response


class TestGetJobsModel:
    @pytest.fixture()
    def returned_response(self) -> TotalmobileGetJobsResponseModel:
        return TotalmobileGetJobsResponseModel(
            questionnaire_jobs={
                "LMS2209_AA1": [
                    Job("LMS2209-AA1.12345", "12345", False, False, None, "LMS")
                ]
            }
        )

    @pytest.fixture()
    def args(self) -> Tuple[str]:
        return ("world-id-1",)

    @pytest.fixture(autouse=True)
    def setup(self, inner_service, returned_response):
        inner_service.get_jobs_model.return_value = returned_response

    def test_delegates_call_to_inner_service(
        self, logging_service, inner_service, args
    ):
        logging_service.get_jobs_model(*args)
        inner_service.get_jobs_model.assert_called_with(*args)

    def test_returns_the_result(self, returned_response, logging_service, args):
        result = logging_service.get_jobs_model(*args)
        assert result == returned_response

    def test_logs_success(self, logging_service, args, caplog):
        with caplog.at_level(logging.INFO):
            logging_service.get_jobs_model(*args)
        assert (
            "root",
            logging.INFO,
            "Found 1 incomplete jobs in totalmobile for world world-id-1",
        ) in caplog.record_tuples
