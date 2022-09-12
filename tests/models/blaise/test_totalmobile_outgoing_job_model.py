from models.cloud_tasks.totalmobile_job_request_model import TotalmobileJobRequestModel
from models.totalmobile.totalmobile_outgoing_job_payload_model import (
    TotalMobileOutgoingJobPayloadModel,
)
from tests.helpers import get_blaise_case_model_helper


def test_create_task_name_returns_correct_name_when_called():
    questionnaire_name = "LMS2101_AA1"

    blaise_case = get_blaise_case_model_helper.get_populated_case_model()
    blaise_case.case_id = "90001"
    blaise_case.questionnaire_name = questionnaire_name
    totalmobile_case_model = TotalMobileOutgoingJobPayloadModel.import_case(
        questionnaire_name, blaise_case
    )
    model = TotalmobileJobRequestModel(
        "LMS2101_AA1", "world", "90001", totalmobile_case_model.to_payload()
    )

    assert model.create_task_name().startswith("LMS2101_AA1-90001-")


def test_create_task_name_returns_unique_name_each_time_when_passed_the_same_model():
    questionnaire_name = "LMS2101_AA1"

    blaise_case = get_blaise_case_model_helper.get_populated_case_model()
    blaise_case.case_id = "90001"
    blaise_case.questionnaire_name = questionnaire_name
    totalmobile_case_model = TotalMobileOutgoingJobPayloadModel.import_case(
        questionnaire_name, blaise_case
    )
    model = TotalmobileJobRequestModel(
        "LMS2101_AA1", "world", "90001", totalmobile_case_model.to_payload()
    )

    assert model.create_task_name() != model.create_task_name()
