from typing import List
from models.case_model import QuestionnaireCaseModel


def get_eligible_cases(cases: List[QuestionnaireCaseModel]) -> List[QuestionnaireCaseModel]:
    return [
        case
        for case in cases
        if (
            case.telephone_number_1 == ""
            and case.telephone_number_2 == ""
            and case.appointment_telephone_number == ""
            and case.wave == "1"
            and case.priority in ["1", "2", "3", "4", "5"]
            and case.outcome_code in ["", "0", "310"])
    ]
