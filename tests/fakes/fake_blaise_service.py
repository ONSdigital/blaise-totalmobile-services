from collections import defaultdict
from typing import Any, Dict, List

from app.exceptions.custom_exceptions import QuestionnaireCaseDoesNotExistError
from models.blaise.blaise_case_information_model import (
    Address,
    AddressCoordinates,
    AddressDetails,
    BlaiseCaseInformationModel,
    ContactDetails,
)
from tests.helpers import get_blaise_case_model_helper


def nested_dict() -> defaultdict:
    return defaultdict(nested_dict)


class FakeBlaiseService:
    def __init__(self):
        self._questionnaires = {}
        self._updates = nested_dict()
        self._errors_when_method_is_called = []
        self._get_cases_call_count = defaultdict(lambda: 0)

    def method_throws_exception(self, method_name: str):
        self._errors_when_method_is_called.append(method_name)

    def add_questionnaire(self, questionnaire_name: str) -> None:
        self._questionnaires[questionnaire_name] = {}

    def add_case_to_questionnaire(
        self,
        questionnaire: str,
        case_id: str,
        outcome_code: int = None,
        wave: str = None,
        field_case: str = None,
        telephone_number_1: str = None,
        telephone_number_2: str = None,
        appointment_telephone_number: str = None,
        field_region: str = None,
    ) -> None:
        self._assert_questionnaire_exists(questionnaire)
        self._questionnaires[questionnaire][case_id] = BlaiseCaseInformationModel(
            questionnaire_name=questionnaire,
            case_id=case_id,
            data_model_name=None,
            wave=wave,
            address_details=AddressDetails(
                Address(
                    address_line_1=None,
                    address_line_2=None,
                    address_line_3=None,
                    county=None,
                    town=None,
                    postcode=None,
                    coordinates=AddressCoordinates(latitude=None, longitude=None),
                )
            ),
            contact_details=ContactDetails(
                telephone_number_1=telephone_number_1,
                telephone_number_2=telephone_number_2,
                appointment_telephone_number=appointment_telephone_number,
            ),
            outcome_code=0 if not outcome_code else outcome_code,
            priority=None,
            field_case=field_case,
            field_region=field_region,
            field_team=None,
            wave_com_dte=None,
            has_call_history=False,
        )

    def update_outcome_code_of_case_in_questionnaire(
        self, questionnaire_name: str, case_id: str, outcome_code: str
    ) -> None:
        self._assert_case_exists(questionnaire_name, case_id)
        self._questionnaires[questionnaire_name][case_id].outcome_code = int(
            outcome_code
        )

    def set_case_has_call_history(
        self, has_case_history: bool, questionnaire: str, case_id: str
    ):
        self._assert_case_exists(questionnaire, case_id)
        self._questionnaires[questionnaire][case_id].has_call_history = has_case_history
        pass

    def case_has_been_updated(self, questionnaire_name: str, case_id: str) -> bool:
        return (
            questionnaire_name in self._updates
            and case_id in self._updates[questionnaire_name]
        )

    def get_updates(self, questionnaire_name: str, case_id: str) -> Dict[str, str]:
        if (
            questionnaire_name not in self._updates
            or case_id not in self._updates[questionnaire_name]
        ):
            raise Exception(
                f"No update has been performed for case '{case_id}' in questionnaire '{questionnaire_name}'"
            )
        return dict(self._updates[questionnaire_name][case_id])

    def required_fields_from_blaise(self) -> List[str]:
        raise NotImplementedError()

    def get_cases(self, questionnaire_name: str) -> List[BlaiseCaseInformationModel]:
        if "get_cases" in self._errors_when_method_is_called:
            raise Exception("get_case has errored")

        self._assert_questionnaire_exists(questionnaire_name)
        self._get_cases_call_count[questionnaire_name] += 1
        cases = self._questionnaires[questionnaire_name]

        return [
            get_blaise_case_model_helper.get_populated_case_model(
                case_id=case.case_id,
                outcome_code=case.outcome_code,
                wave=case.wave,
                field_case=case.field_case,
                telephone_number_1=case.contact_details.telephone_number_1,
                telephone_number_2=case.contact_details.telephone_number_2,
                appointment_telephone_number=case.contact_details.appointment_telephone_number,
                field_region=case.field_region,
            )
            for case in cases.values()
        ]

    def get_cases_call_count(self, questionnaire_name: str) -> int:
        return self._get_cases_call_count[questionnaire_name]

    def get_case(
        self, questionnaire_name: str, case_id: str
    ) -> BlaiseCaseInformationModel:
        if "get_case" in self._errors_when_method_is_called:
            raise Exception("get_case has errored")

        self._assert_case_exists(questionnaire_name, case_id)

        return self._questionnaires[questionnaire_name][case_id]

    def questionnaire_exists(self, questionnaire_name: str) -> bool:
        if "questionnaire_exists" in self._errors_when_method_is_called:
            raise Exception("questionnaire_exists has errored")

        return questionnaire_name in self._questionnaires

    def update_case(
        self, questionnaire_name: str, case_id: str, data_fields: Dict[str, str]
    ) -> None:
        if "update_case" in self._errors_when_method_is_called:
            raise Exception("update_case has errored")

        if case_id not in self._updates[questionnaire_name]:
            self._updates[questionnaire_name][case_id] = {}

        for field, value in data_fields.items():
            self._updates[questionnaire_name][case_id][field] = value

    def _assert_questionnaire_exists(self, questionnaire):
        if not self.questionnaire_exists(questionnaire):
            raise QuestionnaireCaseDoesNotExistError(
                f"Questionnaire '{questionnaire}' does not exist"
            )

    def _assert_case_exists(self, questionnaire_name, case_id):
        self._assert_questionnaire_exists(questionnaire_name)
        if case_id not in self._questionnaires[questionnaire_name]:
            raise QuestionnaireCaseDoesNotExistError(
                f"Case '{case_id}' for questionnaire '{questionnaire_name}' does not exist"
            )
