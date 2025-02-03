import pytest

from enums.blaise_fields import BlaiseFields
from models.update.frs_blaise_update_case_model import FRSBlaiseUpdateCase
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)


@pytest.mark.parametrize(
    "case_id, outcome_code",
    [
        ("10010", 301),
        ("9000", 110),
        ("1002", 210),
    ],
)
def test_populated_update_case_model_has_the_correct_properties(
    case_id: str,
    outcome_code: int,
):
    # arrange
    questionnaire_name = "FRS2101"
    case_data = {
        BlaiseFields.case_id: case_id,
        BlaiseFields.outcome_code: str(outcome_code),
    }

    # act
    result = FRSBlaiseUpdateCase(questionnaire_name, case_data)  # type: ignore

    # assert
    assert result.questionnaire_name == questionnaire_name
    assert result.case_id == case_id
    assert result.outcome_code == outcome_code


def test_get_outcome_code_fields_returns_an_expected_dictionary():
    # arrange
    questionnaire_name = "FRS2101"
    blaise_case = FRSBlaiseUpdateCase(questionnaire_name, {})
    totalmobile_request = TotalMobileIncomingUpdateRequestModel(
        questionnaire_name="FRS2102",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123",
    )

    # act
    result = blaise_case.get_outcome_code_fields(totalmobile_request)

    # assert
    assert result == {
        BlaiseFields.outcome_code: "300",
    }
