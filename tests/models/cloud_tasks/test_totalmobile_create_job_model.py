from unittest.mock import Mock

import pytest

from models.create.blaise.questionnaire_uac_model import UacChunks
from models.create.totalmobile.totalmobile_create_job_model import (
    TotalmobileCreateJobModel,
)
from services.create.mappers.totalmobile_create_job_mapper_service import (
    TotalmobileCreateJobMapperService,
)
from services.create.mappers.totalmobile_payload_mapper_service import (
    TotalmobilePayloadMapperService,
)
from tests.helpers.lms_case_model_helper import get_lms_populated_case_model


@pytest.fixture()
def payload_mapper() -> TotalmobilePayloadMapperService:
    return TotalmobilePayloadMapperService()


@pytest.fixture()
def totalmobile_mapper_service(payload_mapper) -> TotalmobileCreateJobMapperService:
    return TotalmobileCreateJobMapperService(payload_mapper)


def test_create_task_name_returns_correct_name_when_called(totalmobile_mapper_service):
    questionnaire_name = "LMS2101_AA1"

    blaise_case = get_lms_populated_case_model()
    blaise_case.case_id = "90001"
    blaise_case.questionnaire_name = questionnaire_name
    blaise_case.uac_chunks = UacChunks(uac1="3456", uac2="3453", uac3="4546")

    model = TotalmobileCreateJobModel("LMS2101_AA1", "world", "90001", {})

    assert model.create_task_name().startswith("LMS2101_AA1-90001-")


def test_create_task_name_returns_unique_name_each_time_when_passed_the_same_model(
    totalmobile_mapper_service,
):
    questionnaire_name = "LMS2101_AA1"

    blaise_case = get_lms_populated_case_model()
    blaise_case.case_id = "90001"
    blaise_case.questionnaire_name = questionnaire_name
    blaise_case.uac_chunks = UacChunks(uac1="3456", uac2="3453", uac3="4546")

    model = TotalmobileCreateJobModel("LMS2101_AA1", "world", "90001", {})

    assert model.create_task_name() != model.create_task_name()
