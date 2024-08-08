import logging
from typing import List, Sequence

from models.blaise.blaise_lms_case_information_model import (
    BlaiseLMSCaseInformationModel,
)
from services.blaise_service import RealBlaiseService
from services.datastore_service import DatastoreService
from services.lms_eligible_case_service import LMSEligibleCaseService
from services.mappers.blaise_lms_case_mapper_service import BlaiseLMSCaseMapperService
from services.questionnaires.questionnaire_service_base import QuestionnaireServiceBase


class LMSQuestionnaireService(QuestionnaireServiceBase):
    def __init__(
        self,
        blaise_service: RealBlaiseService,
        mapper_service: BlaiseLMSCaseMapperService,
        eligible_case_service: LMSEligibleCaseService,
        datastore_service: DatastoreService,
    ):
        super().__init__(blaise_service, datastore_service)
        self._blaise_service = blaise_service
        self._mapper_service = mapper_service
        self._eligible_case_service = eligible_case_service

    @property
    def questionnaire_tla(self) -> str:
        return "LMS"

    def get_eligible_cases(
        self, questionnaire_name: str
    ) -> Sequence[BlaiseLMSCaseInformationModel]:
        questionnaire_cases = self.get_cases(questionnaire_name)
        eligible_cases: Sequence[
            BlaiseLMSCaseInformationModel
        ] = self._eligible_case_service.get_eligible_cases(questionnaire_cases)
        return eligible_cases

    def get_cases(self, questionnaire_name: str) -> List[BlaiseLMSCaseInformationModel]:
        questionnaire_case_data = self._blaise_service.get_cases(
            questionnaire_name, BlaiseLMSCaseInformationModel.required_fields()
        )
        cases = self._mapper_service.map_lms_case_information_models(
            questionnaire_name, questionnaire_case_data
        )

        logging.info(
            f"Retrieved {len(cases)} cases from questionnaire {questionnaire_name}"
        )
        return cases

    def get_case(
        self, questionnaire_name: str, case_id: str
    ) -> BlaiseLMSCaseInformationModel:
        case_data = self._blaise_service.get_case(questionnaire_name, case_id)
        return self._mapper_service.map_lms_case_information_model(
            questionnaire_name, case_data
        )
