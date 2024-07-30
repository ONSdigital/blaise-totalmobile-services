import logging
from datetime import datetime
from typing import Dict, List

from models.blaise.blaise_frs_case_information_model import BlaiseFRSCaseInformationModel
from services.blaise_service import RealBlaiseService
from services.datastore_service import DatastoreService
from services.eligible_frs_case_service import EligibleFRSCaseService


class FRSQuestionnaireService:
    def __init__(
        self,
        blaise_service: RealBlaiseService,
        eligible_case_service: EligibleFRSCaseService,
        datastore_service: DatastoreService,
    ):
        self._blaise_service = blaise_service
        self._eligible_case_service = eligible_case_service
        self._datastore_service = datastore_service

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

    def get_questionnaires_with_totalmobile_release_date_of_today(self) -> list:    # TODO: Can be made generic in a base class
        records = self._datastore_service.get_totalmobile_release_date_records()
        today = datetime.today().strftime("%d/%m/%Y")
        return [
            record["questionnaire"]
            for record in records
            if record["tmreleasedate"].strftime("%d/%m/%Y") == today
        ]
