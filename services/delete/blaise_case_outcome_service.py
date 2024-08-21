import logging
from typing import Dict, Optional

from models.delete.blaise_delete_case_information__model import (
    BlaiseDeleteCaseInformationBaseModel,
)
from services.common.blaise_service import BlaiseService
from services.delete.mappers.blaise_delete_case_imapper_service import (
    BlaiseDeleteCaseMapperService,
)


class BlaiseCaseOutcomeService:
    def __init__(
        self,
        blaise_service: BlaiseService,
        mapper_service: BlaiseDeleteCaseMapperService,
    ):
        self._blaise_service = blaise_service
        self._mapper_service = mapper_service
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

    def _get_cases(
        self, questionnaire_name: str
    ) -> list[BlaiseDeleteCaseInformationBaseModel]:
        cases = self._blaise_service.get_cases(
            questionnaire_name, BlaiseDeleteCaseInformationBaseModel.required_fields()
        )

        return self._mapper_service.map_blaise_delete_case_models(cases)
