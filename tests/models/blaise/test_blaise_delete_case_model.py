import pytest

from models.delete.blaise_delete_case_model import BlaiseDeleteCase


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
    case_data = {
        "qiD.Serial_Number": case_id,
        "hOut": str(outcome_code),
    }

    # act
    result = BlaiseDeleteCase(case_data)

    # assert
    assert result.case_id == case_id
    assert result.outcome_code == outcome_code
