import logging
from typing import Dict, Optional

from models.delete.blaise_delete_case_model import BlaiseDeleteCase
from services.blaise_service import BlaiseService


class BlaiseCaseOutcomeService:
    def __init__(
        self,
        blaise_service: BlaiseService,
    ):
        self._blaise_service = blaise_service
        self._questionnaire_case_outcomes: Dict[str, Dict[Optional[str], int]] = {}

    def get_case_outcomes_for_questionnaire(
        self, questionnaire_name: str
    ) -> Dict[Optional[str], int]:
        if questionnaire_name not in self._questionnaire_case_outcomes:
            try:
                self._questionnaire_case_outcomes[
                    questionnaire_name
                ] = self._get_case_outcomes(questionnaire_name)
            except Exception as error:
                logging.error(
                    f"Unable to retrieve cases from Blaise for questionnaire {questionnaire_name}",
                    extra={"json_fields": {"Exception_reason": str(error)}},
                )
                return {}

        return self._questionnaire_case_outcomes[questionnaire_name]

    def _get_case_outcomes(self, questionnaire_name: str) -> Dict[Optional[str], int]:
        cases = self._get_cases(questionnaire_name)

        return {case.case_id: case.outcome_code for case in cases}

    def _get_cases(self, questionnaire_name: str) -> list[BlaiseDeleteCase]:
        case_data_list = self._blaise_service.get_cases(
            questionnaire_name, BlaiseDeleteCase.required_fields()
        )

        return [
            BlaiseDeleteCase(questionnaire_name, case_data)
            for case_data in case_data_list
        ]
