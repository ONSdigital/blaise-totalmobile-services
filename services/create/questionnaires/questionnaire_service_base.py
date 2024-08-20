import logging
from abc import abstractmethod
from datetime import datetime
from typing import Dict, Sequence

from models.create.blaise.blaise_case_information_base_model import (
    BlaiseCaseInformationBaseModel,
)
from services.common.blaise_service import RealBlaiseService
from services.create.datastore.datastore_service import DatastoreService


class QuestionnaireServiceBase:
    def __init__(
        self, blaise_service: RealBlaiseService, datastore_service: DatastoreService
    ):
        self._datastore_service = datastore_service
        self._blaise_service = blaise_service

    @property
    @abstractmethod
    def questionnaire_tla(self) -> str:
        pass

    @abstractmethod
    def get_eligible_cases(
        self, questionnaire_name: str
    ) -> Sequence[BlaiseCaseInformationBaseModel]:
        pass

    def get_questionnaires_with_totalmobile_release_date_of_today(self) -> list:
        records = self._datastore_service.get_totalmobile_release_date_records()
        today = datetime.today().strftime("%d/%m/%Y")
        return [
            record["questionnaire"]
            for record in records
            if record["tmreleasedate"].strftime("%d/%m/%Y") == today
            and record["questionnaire"].upper().startswith(self.questionnaire_tla)
        ]
