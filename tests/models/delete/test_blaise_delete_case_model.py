import pytest

from enums.blaise_fields import BlaiseFields
from models.delete.blaise_delete_case_model import BlaiseDeleteCaseBase


@pytest.mark.parametrize(
    "case_id, outcome_code",
    [
        ("10010", 301),
        ("9000", 110),
        ("1002", 210),
    ],
)
def test_populated_delete_case_model_has_the_correct_properties(
    case_id: str, outcome_code: int
):
    # arrange
    questionnaire_name = "LMS2101_TLR"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: str(outcome_code),
    }

    # act
    result = BlaiseDeleteCaseBase(questionnaire_name, case_data)  # type: ignore

    # assert
    assert result.case_id == case_id
    assert result.outcome_code == outcome_code
