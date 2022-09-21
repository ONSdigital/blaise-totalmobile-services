from models.totalmobile.totalmobile_get_jobs_response_model import (
    TotalmobileGetJobsResponseModel,
)
from tests.helpers import optimise_client_helper


def test_total_mobile_job_models_maps_expected_list_of_models_from_job_response():
    # arrange
    job_response = optimise_client_helper.get_jobs_response()

    # act
    result = TotalmobileGetJobsResponseModel(job_response)

    # assert
    assert len(result.questionnaire_jobs) == 2

    assert len(result.questionnaire_jobs["LMS1111_AA1"]) == 2
    assert result.questionnaire_jobs["LMS1111_AA1"][0].case_id == "12345"
    assert result.questionnaire_jobs["LMS1111_AA1"][0].reference == "LMS1111-AA1.12345"
    assert result.questionnaire_jobs["LMS1111_AA1"][0].visit_complete is True
    assert result.questionnaire_jobs["LMS1111_AA1"][1].case_id == "67890"
    assert result.questionnaire_jobs["LMS1111_AA1"][1].reference == "LMS1111-AA1.67890"
    assert result.questionnaire_jobs["LMS1111_AA1"][1].visit_complete is False

    assert len(result.questionnaire_jobs["LMS2222_BB2"]) == 1
    assert result.questionnaire_jobs["LMS2222_BB2"][0].case_id == "22222"
    assert result.questionnaire_jobs["LMS2222_BB2"][0].reference == "LMS2222-BB2.22222"
    assert result.questionnaire_jobs["LMS2222_BB2"][0].visit_complete is False


def test_questionnaires_with_incomplete_jobs_returns_expected_dictionary():
    # arrange
    job_response = [
        {"visitComplete": True, "identity": {"reference": "LMS1111-AA1.12345"}},
        {"visitComplete": False, "identity": {"reference": "LMS2222-BB2.22222"}},
        {"visitComplete": True, "identity": {"reference": "LMS1111-AA1.67890"}},
    ]

    # act
    model = TotalmobileGetJobsResponseModel(job_response)
    result = model.questionnaires_with_incomplete_jobs()

    # assert
    assert len(result) == 1

    assert len(result["LMS2222_BB2"]) == 1
    assert result["LMS2222_BB2"][0].case_id == "22222"
    assert result["LMS2222_BB2"][0].reference == "LMS2222-BB2.22222"
    assert result["LMS2222_BB2"][0].visit_complete is False
