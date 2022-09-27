import logging
from typing import Dict, List

from appconfig import Config
from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from services.blaise_service import BlaiseService
from services.uac_service import UacService


class QuestionnaireService:
    def __init__(
        self,
        config: Config,
        blaise_service: BlaiseService,
        eligible_case_service,
        uac_service: UacService,
    ):
        self._config = config
        self._blaise_service = blaise_service
        self._eligible_case_service = eligible_case_service
        self._uac_service = uac_service

    def get_eligible_cases(
        self, questionnaire_name: str
    ) -> List[BlaiseCaseInformationModel]:
        questionnaire_cases = self.get_cases(questionnaire_name)

        return self._eligible_case_service.get_eligible_cases(questionnaire_cases)

    def get_cases(self, questionnaire_name: str) -> List[BlaiseCaseInformationModel]:
        questionnaire_cases = self._blaise_service.get_cases(questionnaire_name)
        questionnaire_uacs = self._uac_service.get_uacs(questionnaire_name)

        [
            questionnaire_case.populate_uac_data(
                next(
                    (
                        x
                        for x in questionnaire_uacs
                        if x.case_id == questionnaire_case.case_id
                    ),
                    None,
                )
            )
            for questionnaire_case in questionnaire_cases
        ]

        return questionnaire_cases

    def get_case(
        self, questionnaire_name: str, case_id: str
    ) -> BlaiseCaseInformationModel:
        return self._blaise_service.get_case(questionnaire_name, case_id)

    def get_wave_from_questionnaire_name(self, questionnaire_name: str) -> str:
        if questionnaire_name[0:3] != "LMS":
            raise Exception(
                f"Invalid format for questionnaire name: {questionnaire_name}"
            )
        return questionnaire_name[-1]

    def questionnaire_exists(self, questionnaire_name: str) -> bool:
        return self._blaise_service.questionnaire_exists(questionnaire_name)

    def update_case(
        self, questionnaire_name: str, case_id: str, data_fields: Dict[str, str]
    ) -> None:
        keys_to_log = [key for data_field in data_fields for key in data_field]
        logging.info(
            f"Attempting to update case {case_id} in questionnaire {questionnaire_name} in Blaise with data fields {keys_to_log}"
        )
        return self._blaise_service.update_case(
            questionnaire_name, case_id, data_fields
        )
