import logging
from typing import List, Sequence

from models.create.blaise.blaiise_frs_create_case_model import BlaiseFRSCreateCaseModel
from services.blaise_service import RealBlaiseService
from services.create.datastore_service import DatastoreService
from services.create.eligibility.frs_eligible_case_service import FRSEligibleCaseService
from services.create.questionnaires.questionnaire_service_base import (
    QuestionnaireServiceBase,
)


class FRSQuestionnaireService(QuestionnaireServiceBase):
    def __init__(
        self,
        blaise_service: RealBlaiseService,
        eligible_case_service: FRSEligibleCaseService,
        datastore_service: DatastoreService,
    ):
        super().__init__(blaise_service, datastore_service)
        self._blaise_service = blaise_service
        self._eligible_case_service = eligible_case_service

    @property
    def questionnaire_tla(self) -> str:
        return "FRS"

    def get_eligible_cases(
        self, questionnaire_name: str
    ) -> Sequence[BlaiseFRSCreateCaseModel]:
        questionnaire_cases = self.get_cases(questionnaire_name)
        eligible_cases: Sequence[
            BlaiseFRSCreateCaseModel
        ] = self._eligible_case_service.get_eligible_cases(questionnaire_cases)
        return eligible_cases

    def get_cases(self, questionnaire_name: str) -> List[BlaiseFRSCreateCaseModel]:
        case_data_list = self._blaise_service.get_cases(
            questionnaire_name, BlaiseFRSCreateCaseModel.required_fields()
        )
        cases = [
            BlaiseFRSCreateCaseModel(questionnaire_name, case_data)
            for case_data in case_data_list
        ]

        logging.info(
            f"Retrieved {len(cases)} cases from questionnaire {questionnaire_name}"
        )
        return cases

    def get_case(
        self, questionnaire_name: str, case_id: str
    ) -> BlaiseFRSCreateCaseModel:
        case_data = self._blaise_service.get_case(questionnaire_name, case_id)
        return BlaiseFRSCreateCaseModel(questionnaire_name, case_data)
