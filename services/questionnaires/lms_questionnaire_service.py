import logging
from typing import List, Sequence

from models.blaise.blaise_lms_case_information_model import (
    BlaiseLMSCaseInformationModel,
)
from models.blaise.questionnaire_uac_model import QuestionnaireUacModel
from services.blaise_service import RealBlaiseService
from services.datastore_service import DatastoreService
from services.lms_eligible_case_service import LMSEligibleCaseService
from services.mappers.blaise_lms_case_mapper_service import BlaiseLMSCaseMapperService
from services.questionnaires.questionnaire_service_base import QuestionnaireServiceBase
from services.uac.uac_service_base import UacServiceBase


class LMSQuestionnaireService(QuestionnaireServiceBase):
    def __init__(
        self,
        blaise_service: RealBlaiseService,
        mapper_service: BlaiseLMSCaseMapperService,
        eligible_case_service: LMSEligibleCaseService,
        datastore_service: DatastoreService,
        uac_service: UacServiceBase,
    ):
        super().__init__(blaise_service, datastore_service)
        self._blaise_service = blaise_service
        self._mapper_service = mapper_service
        self._eligible_case_service = eligible_case_service
        self._uac_service = uac_service

    @property
    def questionnaire_tla(self) -> str:
        return "LMS"

    def get_eligible_cases(
        self, questionnaire_name: str
    ) -> Sequence[BlaiseLMSCaseInformationModel]:
        questionnaire_cases = self.get_cases(questionnaire_name, True)
        eligible_cases: Sequence[
            BlaiseLMSCaseInformationModel
        ] = self._eligible_case_service.get_eligible_cases(questionnaire_cases)
        return eligible_cases

    def get_cases(
        self, questionnaire_name: str, include_uac: bool = False
    ) -> List[BlaiseLMSCaseInformationModel]:
        questionnaire_case_data = self._blaise_service.get_cases(
            questionnaire_name, BlaiseLMSCaseInformationModel.required_fields()
        )
        questionnaire_uac_model = (
            self.get_questionnaire_uac_model(questionnaire_name)
            if include_uac
            else None
        )
        cases = self._mapper_service.map_lms_case_information_models(
            questionnaire_name, questionnaire_case_data, questionnaire_uac_model
        )

        logging.info(
            f"Retrieved {len(cases)} cases from questionnaire {questionnaire_name}"
        )
        return cases

    def get_case(
        self, questionnaire_name: str, case_id: str, include_uac: bool = False
    ) -> BlaiseLMSCaseInformationModel:
        case_data = self._blaise_service.get_case(questionnaire_name, case_id)
        questionnaire_uac_model = (
            self.get_questionnaire_uac_model(questionnaire_name)
            if include_uac
            else None
        )
        return self._mapper_service.map_lms_case_information_model(
            questionnaire_name, case_data, questionnaire_uac_model
        )

    def get_questionnaire_uac_model(
        self, questionnaire_name: str
    ) -> QuestionnaireUacModel:
        return self._uac_service.get_questionnaire_uac_model(questionnaire_name)
