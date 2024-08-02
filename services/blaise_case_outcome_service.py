import logging
from typing import Dict, List, Optional

from models.blaise.blaise_lms_case_information_model import BlaiseLMSCaseInformationModel
from services.blaise_service import BlaiseService
from services.mappers.mapper_base import MapperServiceBase


class BlaiseCaseOutcomeService:
    def __init__(self, blaise_service: BlaiseService):
        self._blaise_service = blaise_service
        self._questionnaire_case_outcomes: Dict[str, Dict[Optional[str], int]] = {}

    def get_case_outcomes_for_questionnaire(
        self, questionnaire_name: str
    ) -> Dict[Optional[str], int]:
        if questionnaire_name not in self._questionnaire_case_outcomes:
            try:
                cases = self._blaise_service.get_cases(questionnaire_name, BlaiseLMSCaseInformationModel.required_fields())
                self._questionnaire_case_outcomes[questionnaire_name] = self._get_case_outcomes(cases)
            except Exception as error:
                logging.error(
                    f"Unable to retrieve cases from Blaise for questionnaire {questionnaire_name}",
                    extra={"json_fields": {"Exception_reason": str(error)}},
                )
                return {}

        return self._questionnaire_case_outcomes[questionnaire_name]

    @staticmethod
    def _get_case_outcomes(case_data_list: List[Dict[str, str]]) -> Dict[Optional[str], int]:
        return {MapperServiceBase.get_case_id(case_data): MapperServiceBase.get_outcome_code(case_data) for case_data in case_data_list}


