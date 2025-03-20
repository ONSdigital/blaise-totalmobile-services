from models.create.blaise.blaise_frs_create_case_model import BlaiseFRSCreateCaseModel
from services.create.questionnaires.eligibility.frs_eligible_case_service import (
    FRSEligibleCaseService,
)
from tests.helpers.blaise_case_model_helper import BlaiseCaseModelHelper


def get_case(case_id: str, field_region: str) -> BlaiseFRSCreateCaseModel:
    return BlaiseCaseModelHelper.get_populated_frs_create_case_model(
        questionnaire_name="FRS2210", case_id=case_id, field_region=field_region
    )


def test_get_eligible_cases_returns_expected_list_of_eligible_cases_for_frs():
    # arrange
    service = FRSEligibleCaseService()

    cases = [
        get_case(case_id="90001", field_region="Region 1"),
        get_case(case_id="90002", field_region="Region 2"),
        get_case(case_id="90003", field_region="Region 3"),
        get_case(case_id="90004", field_region="Region 4"),
        get_case(case_id="90005", field_region="Region 5"),
        get_case(case_id="90006", field_region="Region 6"),
        get_case(case_id="90007", field_region="Region 7"),
        get_case(case_id="90008", field_region="Region 8"),
        get_case(case_id="90009", field_region="Region 9"),
        get_case(case_id="90009", field_region="Region 10"),
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 10

    assert result[0].case_id == "90001"
    assert result[1].case_id == "90002"
    assert result[2].case_id == "90003"
    assert result[3].case_id == "90004"
    assert result[4].case_id == "90005"
    assert result[5].case_id == "90006"
    assert result[6].case_id == "90007"
    assert result[7].case_id == "90008"
    assert result[8].case_id == "90009"
    assert result[9].case_id == "90010"
    

def test_get_eligible_cases_handles_unknown_regions():
    # arrange
    service = FRSEligibleCaseService()

    cases = [
        get_case(case_id="90001", field_region="Region 1"),
        get_case(case_id="90002", field_region="Eriador"), 
        get_case(case_id="90003", field_region="The Shire"),
        get_case(case_id="90004", field_region="Region 4"),
        get_case(case_id="90005", field_region="Mordor"),
        get_case(case_id="90006", field_region="Gondor"),
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 2

    assert result[0].case_id == "90001"
    assert result[1].case_id == "90004"

    assert result[0].field_region == "Region 1"
    assert result[1].field_region == "Region 4"