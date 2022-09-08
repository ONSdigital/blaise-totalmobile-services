from models.totalmobile.totalmobile_jobs_model import TotalmobileJobsModel


def test_total_mobile_job_models_maps_expected_list_of_models_from_job_reference_list():
    # arrange
    job_references = [
        "LMS1111-AA1.12345",
        "LMS1111-AA1.67890",
        "LMS2222-BB2.23384"
    ]

    # act
    result = TotalmobileJobsModel(job_references)

    # assert
    assert len(result.questionnaire_jobs) == 2

    assert len(result.questionnaire_jobs["LMS1111_AA1"]) == 2
    assert result.questionnaire_jobs["LMS1111_AA1"][0].case_id == "12345"
    assert result.questionnaire_jobs["LMS1111_AA1"][0].reference == "LMS1111-AA1.12345"
    assert result.questionnaire_jobs["LMS1111_AA1"][1].case_id == "67890"
    assert result.questionnaire_jobs["LMS1111_AA1"][1].reference == "LMS1111-AA1.67890"

    assert len(result.questionnaire_jobs["LMS2222_BB2"]) == 1
    assert result.questionnaire_jobs["LMS2222_BB2"][0].case_id == "23384"
    assert result.questionnaire_jobs["LMS2222_BB2"][0].reference == "LMS2222-BB2.23384"


def test_map_reference_models_from_list_of_job_references_returns_an_expected_list_of_reference_models():
    # arrange
    job_references = ["LMS1111-AA1.67890", "LMS2222-BB2.12345"]

    # act
    result = TotalmobileJobsModel.map_reference_models_from_list_of_job_references(job_references)

    # assert
    assert result[0].questionnaire_name == "LMS1111_AA1"
    assert result[0].case_id == "67890"

    assert result[1].questionnaire_name == "LMS2222_BB2"
    assert result[1].case_id == "12345"