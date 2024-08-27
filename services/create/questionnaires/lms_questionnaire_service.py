import logging
from typing import List, Sequence

from models.create.blaise.blaiise_lms_create_case_model import BlaiseLMSCreateCaseModel
from models.create.blaise.questionnaire_uac_model import QuestionnaireUacModel
from services.common.blaise_service import RealBlaiseService
from services.create.datastore.datastore_service import DatastoreService
from services.create.eligibility.lms_eligible_case_service import LMSEligibleCaseService
from services.create.questionnaires.questionnaire_service_base import (
    QuestionnaireServiceBase,
)
from services.create.uac.uac_service_base import UacServiceBase


class LMSQuestionnaireService(QuestionnaireServiceBase):
    def __init__(
        self,
        blaise_service: RealBlaiseService,
        eligible_case_service: LMSEligibleCaseService,
        datastore_service: DatastoreService,
        uac_service: UacServiceBase,
    ):
        super().__init__(blaise_service, datastore_service)
        self._blaise_service = blaise_service
        self._eligible_case_service = eligible_case_service
        self._uac_service = uac_service

    @property
    def questionnaire_tla(self) -> str:
        return "LMS"

    def get_eligible_cases(
        self, questionnaire_name: str
    ) -> Sequence[BlaiseLMSCreateCaseModel]:
        questionnaire_cases = self.get_cases(questionnaire_name, True)
        eligible_cases: Sequence[
            BlaiseLMSCreateCaseModel
        ] = self._eligible_case_service.get_eligible_cases(questionnaire_cases)
        return eligible_cases

    def get_cases(
        self, questionnaire_name: str, include_uac: bool = False
    ) -> List[BlaiseLMSCreateCaseModel]:
        case_data_list = self._blaise_service.get_cases(
            questionnaire_name, BlaiseLMSCreateCaseModel.required_fields()
        )
        questionnaire_uac_model = (
            self.get_questionnaire_uac_model(questionnaire_name)
            if include_uac
            else None
        )

        if include_uac or questionnaire_uac_model is None:
            cases = [
                BlaiseLMSCreateCaseModel(questionnaire_name, case_data, None)
                for case_data in case_data_list
            ]
        else:
            cases = [
                BlaiseLMSCreateCaseModel(
                    questionnaire_name,
                    case_data,
                    questionnaire_uac_model.get_uac_chunks(
                        case_data["qiD.Serial_Number"]
                    ),
                )
                for case_data in case_data_list
            ]

        logging.info(
            f"Retrieved {len(cases)} cases from questionnaire {questionnaire_name}"
        )
        return cases

    def get_case(
        self, questionnaire_name: str, case_id: str, include_uac: bool = False
    ) -> BlaiseLMSCreateCaseModel:
        case_data = self._blaise_service.get_case(questionnaire_name, case_id)
        questionnaire_uac_model = (
            self.get_questionnaire_uac_model(questionnaire_name)
            if include_uac
            else None
        )

        uac_chunks = (
            None
            if questionnaire_uac_model is None
            else questionnaire_uac_model.get_uac_chunks(case_id)
        )

        return BlaiseLMSCreateCaseModel(questionnaire_name, case_data, uac_chunks)

    def get_questionnaire_uac_model(
        self, questionnaire_name: str
    ) -> QuestionnaireUacModel:
        return self._uac_service.get_questionnaire_uac_model(questionnaire_name)
