from unittest.mock import Mock

import pytest

from models.create.totalmobile.totalmobile_create_job_model import (
    TotalmobileCreateJobModel,
)
from services.create.mappers.totalmobile_create_job_mapper_service import (
    TotalmobileCreateJobMapperService,
)
from services.create.mappers.totalmobile_payload_mapper_service import (
    TotalmobilePayloadMapperService,
)


@pytest.fixture()
def payload_mapper() -> TotalmobilePayloadMapperService:
    return TotalmobilePayloadMapperService()


@pytest.fixture()
def totalmobile_mapper_service(payload_mapper) -> TotalmobileCreateJobMapperService:
    return TotalmobileCreateJobMapperService(payload_mapper)


def test_create_task_name_returns_correct_name_when_called(totalmobile_mapper_service):

    model = TotalmobileCreateJobModel("LMS2101_AA1", "world", "90001", {})

    assert model.create_task_name().startswith("LMS2101_AA1-90001-")


def test_create_task_name_returns_unique_name_each_time_when_passed_the_same_model(
    totalmobile_mapper_service,
):
    model = TotalmobileCreateJobModel("LMS2101_AA1", "world", "90001", {})

    assert model.create_task_name() != model.create_task_name()
