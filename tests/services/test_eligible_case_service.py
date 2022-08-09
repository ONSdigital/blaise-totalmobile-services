from services import eligible_case_service
from tests.helpers.questionnaire_case_model_helper import populated_case_model


def test_filter_eligible_cases_returns_cases_only_where_criteria_is_met():
    # arrange
    cases = [
        # should return
        populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        populated_case_model(
            case_id="90002",
            telephone_number_1="123435",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        populated_case_model(
            case_id="90003",
            telephone_number_1="",
            telephone_number_2="123435",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        populated_case_model(
            case_id="90004",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="123435",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        populated_case_model(
            case_id="90005",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="2",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        populated_case_model(
            case_id="90006",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="6",
            outcome_code="310"
        ),
        # should not return
        populated_case_model(
            case_id="90007",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="410"
        ),
        # should return
        populated_case_model(
            case_id="90008",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="0"
        ),
        # should return
        populated_case_model(
            case_id="90009",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="2",
            outcome_code="0"
        ),
        # should return
        populated_case_model(
            case_id="90010",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="3",
            outcome_code="0"
        ),
        # should return
        populated_case_model(
            case_id="90011",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="4",
            outcome_code="0"
        ),
        # should return
        populated_case_model(
            case_id="90012",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="5",
            outcome_code="0"
        ),
        # should return
        populated_case_model(
            case_id="90013",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="5",
            outcome_code=""
        )
    ]

    # act
    result = eligible_case_service.filter_eligible_cases(cases)

    # assert
    assert result == [
        # should return
        populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should return
        populated_case_model(
            case_id="90008",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="0"
        ),
        populated_case_model(
            case_id="90009",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="2",
            outcome_code="0"
        ),
        populated_case_model(
            case_id="90010",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="3",
            outcome_code="0"
        ),
        populated_case_model(
            case_id="90011",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="4",
            outcome_code="0"
        ),
        populated_case_model(
            case_id="90012",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="5",
            outcome_code="0"
        ),
        populated_case_model(
            case_id="90013",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="5",
            outcome_code=""
        )
    ]
