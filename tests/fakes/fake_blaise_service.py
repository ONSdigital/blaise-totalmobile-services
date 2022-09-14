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

    def add_questionnaire(self, questionnaire_name: str) -> None:
        self._questionnaires[questionnaire_name] = {}

    def add_case_to_questionnaire(self, questionnaire: str, case_id: str) -> None:
        self._assert_questionnaire_exists(questionnaire)
        self._questionnaires[questionnaire][case_id] = BlaiseCaseInformationModel(
            questionnaire_name=questionnaire,
            case_id=case_id,
            data_model_name=None,
            wave=None,
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
                telephone_number_1=None,
                telephone_number_2=None,
                appointment_telephone_number=None,
            ),
            outcome_code=0,
            priority=None,
            field_case=None,
            field_region=None,
            field_team=None,
            wave_com_dte=None,
            uac_chunks=None,
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
        self._assert_questionnaire_exists(questionnaire_name)

        case = self._questionnaires[questionnaire_name]

        for key in case.keys():
            return [
                get_blaise_case_model_helper.get_populated_case_model(case_id=case[key].case_id, outcome_code=case[key].outcome_code),
            ]

        raise Exception

    def get_case(
        self, questionnaire_name: str, case_id: str
    ) -> BlaiseCaseInformationModel:
        self._assert_case_exists(questionnaire_name, case_id)

        return self._questionnaires[questionnaire_name][case_id]

    def questionnaire_exists(self, questionnaire_name: str) -> bool:
        return questionnaire_name in self._questionnaires

    def update_case(
        self, questionnaire_name: str, case_id: str, data_fields: Dict[str, str]
    ) -> None:
        if case_id not in self._updates[questionnaire_name]:
            self._updates[questionnaire_name][case_id] = {}

        for field, value in data_fields.items():
            self._updates[questionnaire_name][case_id][field] = value

    def get_case_status_information(self, questionnaire_name: str) -> List[Dict[str, Any]]:
        self._assert_questionnaire_exists(questionnaire_name)

        case = self._questionnaires[questionnaire_name]

        for key in case.keys():
            return [
                {
                    "primaryKey": f"{case[key].case_id}",
                    "outcome": case[key].outcome_code,
                },
            ]

        raise Exception

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
