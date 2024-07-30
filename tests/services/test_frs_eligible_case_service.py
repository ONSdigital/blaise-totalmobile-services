from services.eligible_frs_case_service import EligibleFRSCaseService
from tests.helpers.get_blaise_frs_case_model_helper import get_frs_populated_case_model


def test_get_eligible_cases_returns_expected_list_of_eligible_cases_for_frs():
    # arrange
    service = EligibleFRSCaseService()

    cases = [
        get_frs_populated_case_model(case_id="90001", field_region="Region 1"),
        get_frs_populated_case_model(case_id="90002", field_region="Region 2"),
        get_frs_populated_case_model(case_id="90003", field_region="Region 3"),
        get_frs_populated_case_model(case_id="90004", field_region="Region 4"),
        get_frs_populated_case_model(case_id="90005", field_region="Region 5"),
        get_frs_populated_case_model(case_id="90006", field_region="Region 6"),
        get_frs_populated_case_model(case_id="90007", field_region="Region 7"),
        get_frs_populated_case_model(case_id="90008", field_region="Region 8"),
        get_frs_populated_case_model(case_id="90009", field_region="Region 9"),
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 8

    assert result == [
        get_frs_populated_case_model(case_id="90001", field_region="Region 1"),
        get_frs_populated_case_model(case_id="90002", field_region="Region 2"),
        get_frs_populated_case_model(case_id="90003", field_region="Region 3"),
        get_frs_populated_case_model(case_id="90004", field_region="Region 4"),
        get_frs_populated_case_model(case_id="90005", field_region="Region 5"),
        get_frs_populated_case_model(case_id="90006", field_region="Region 6"),
        get_frs_populated_case_model(case_id="90007", field_region="Region 7"),
        get_frs_populated_case_model(case_id="90008", field_region="Region 8"),
    ]
    