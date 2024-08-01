import logging
from typing import List

from models.blaise.blaise_frs_case_information_model import BlaiseFRSCaseInformationModel
from services.blaise_service import RealBlaiseService
from services.datastore_service import DatastoreService
from services.frs_eligible_case_service import FRSEligibleCaseService
from services.questionnaires.questionnaire_service_base import QuestionnaireServiceBase


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
    ) -> List[BlaiseFRSCaseInformationModel]:
        questionnaire_cases = self.get_cases(questionnaire_name)
        eligible_cases = self._eligible_case_service.get_eligible_cases(
            questionnaire_cases
        )
        return eligible_cases

    def get_cases(self, questionnaire_name: str) -> List[BlaiseFRSCaseInformationModel]:
        cases = self._blaise_service.get_cases(questionnaire_name)
        logging.info(
            f"Retrieved {len(cases)} cases from questionnaire {questionnaire_name}"
        )
        return cases

    def get_case(
        self, questionnaire_name: str, case_id: str
    ) -> BlaiseFRSCaseInformationModel:
        # TODO: Fix dis
        return self._blaise_service.get_case(questionnaire_name, case_id)
