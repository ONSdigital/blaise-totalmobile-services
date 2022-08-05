from models.case_model import QuestionnaireCaseModel
from services.case_service import get_eligible_cases


def test_get_eligible_cases_returns_cases_only_where_criteria_is_met():
    # arrange
    cases = [
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "310"
        ),
        # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "123435",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "310"
        ),
        # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "123435",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "310"
        ),
        # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "123435",
            wave = "1",
            priority = "1",
            outcome_code= "310"
        ),
        # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "2",
            priority = "1",
            outcome_code= "310"
        ),
        # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "6",
            outcome_code= "310"
        ),
        # should not return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "410"
        ),
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "0"
        ),
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "2",
            outcome_code= "0"
        ),
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "3",
            outcome_code= "0"
        ),
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "4",
            outcome_code= "0"
        ),
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "5",
            outcome_code= "0"
        ),
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "5",
            outcome_code= ""
        )
    ]

    # act
    result = get_eligible_cases(cases)

    # assert
    assert result == [
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "310"
        ),
        # should return
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "1",
            outcome_code= "0"
        ),
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "2",
            outcome_code= "0"
        ),
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "3",
            outcome_code= "0"
        ),
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "4",
            outcome_code= "0"
        ),
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "5",
            outcome_code= "0"
        ),
        QuestionnaireCaseModel(
            telephone_number_1 = "",
            telephone_number_2 = "",
            appointment_telephone_number = "",
            wave = "1",
            priority = "5",
            outcome_code= ""
        )
    ]
