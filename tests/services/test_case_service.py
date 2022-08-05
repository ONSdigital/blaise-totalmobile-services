from services import case_service
from models.case_model import CaseModel


def test_filter_eligible_cases_returns_cases_only_where_criteria_is_met():
    # arrange
    cases = [
        # should return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "310"
        ),
        # should not return
        CaseModel(
            telephone_number_1 = "123435",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "310"
        ),
        # should not return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "123435",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "310"
        ),
        # should not return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "123435",
            wave = "1",
            priority = "1",
            outcome_code= "310"
        ),
        # should not return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "2",
            priority = "1",
            outcome_code= "310"
        ),
        # should not return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "6",
            outcome_code= "310"
        ),
        # should not return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "410"
        ),
        # should return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "0"
        ),
        # should return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "2",
            outcome_code= "0"
        ),
        # should return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "3",
            outcome_code= "0"
        ),
        # should return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "4",
            outcome_code= "0"
        ),
        # should return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "5",
            outcome_code= "0"
        ),
        # should return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "5",
            outcome_code= ""
        )
    ]

    # act
    result = case_service.filter_eligible_cases(cases)

    # assert
    assert result == [
        # should return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "310"
        ),
        # should return
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "0"
        ),
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "2",
            outcome_code= "0"
        ),
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "3",
            outcome_code= "0"
        ),
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "4",
            outcome_code= "0"
        ),
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "5",
            outcome_code= "0"
        ),
        CaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "5",
            outcome_code= ""
        )
    ]
