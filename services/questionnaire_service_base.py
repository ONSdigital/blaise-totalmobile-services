from abc import abstractmethod
from datetime import datetime
from typing import List

from models.base_model import BaseModel


class QuestionnaireServiceBase:

    @abstractmethod
    def get_eligible_cases(self, questionnaire_name: str)  -> List[BaseModel]:
        pass
    
    def get_questionnaires_with_totalmobile_release_date_of_today(self) -> list:
        records = self._datastore_service.get_totalmobile_release_date_records()
        today = datetime.today().strftime("%d/%m/%Y")
        return [
            record["questionnaire"]
            for record in records
            if record["tmreleasedate"].strftime("%d/%m/%Y") == today
        ]