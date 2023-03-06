import logging
from typing import Dict, List

from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from services.blaise_service import BlaiseService


class BlaiseCaseOutcomeService:
    def __init__(self, blaise_service: BlaiseService):
        self._blaise_service = blaise_service
        self._questionnaire_case_outcomes: Dict[str, Dict[str, int]] = {}

    def get_case_outcomes_for_questionnaire(
        self, questionnaire_name: str
    ) -> Dict[str, int]:
        if questionnaire_name not in self._questionnaire_case_outcomes:
            try:
                cases = self._blaise_service.get_cases(questionnaire_name)
                self._questionnaire_case_outcomes[
                    questionnaire_name
                ] = self._get_case_outcomes(cases)
            except Exception as error:
                logging.error(
                    f"Unable to retrieve cases from Blaise for questionnaire {questionnaire_name}",
                    extra={"json_fields": {"Exception_reason": str(error)}},
                )
                return {}

        return self._questionnaire_case_outcomes[questionnaire_name]

    @staticmethod
    def _get_case_outcomes(cases: List[BlaiseCaseInformationModel]) -> Dict[str, int]:
        return {str(case.case_id): case.outcome_code for case in cases}
