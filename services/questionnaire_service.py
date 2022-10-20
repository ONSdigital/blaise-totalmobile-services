import logging
from datetime import datetime
from typing import Dict, List

from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from services.blaise_service import RealBlaiseService
from services.datastore_service import DatastoreService
from services.eligible_case_service import EligibleCaseService


class QuestionnaireService:
    def __init__(
        self,
        blaise_service: RealBlaiseService,
        eligible_case_service: EligibleCaseService,
        datastore_service: DatastoreService,
    ):
        self._blaise_service = blaise_service
        self._eligible_case_service = eligible_case_service
        self._datastore_service = datastore_service

    def get_eligible_cases(
        self, questionnaire_name: str
    ) -> List[BlaiseCaseInformationModel]:
        questionnaire_cases = self.get_cases(questionnaire_name)

        return self._eligible_case_service.get_eligible_cases(questionnaire_cases)

    def get_cases(self, questionnaire_name: str) -> List[BlaiseCaseInformationModel]:
        return self._blaise_service.get_cases(questionnaire_name)

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
        logging.info(
            f"Attempting to update case {case_id} in questionnaire {questionnaire_name} in Blaise"
        )
        return self._blaise_service.update_case(
            questionnaire_name, case_id, data_fields
        )

    def get_questionnaires_with_totalmobile_release_date_of_today(self) -> list:
        records = self._datastore_service.get_totalmobile_release_date_records()
        today = datetime.today().strftime("%d/%m/%Y")
        return [
            record["questionnaire"]
            for record in records
            if record["tmreleasedate"].strftime("%d/%m/%Y") == today
        ]
