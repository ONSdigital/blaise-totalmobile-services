import logging
from abc import abstractmethod

from app.exceptions.custom_exceptions import QuestionnaireDoesNotExistError
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.blaise_service import RealBlaiseService


class UpdateCaseServiceBase:
    def __init__(self, blaise_service: RealBlaiseService):
        self._blaise_service = blaise_service

    @abstractmethod
    def update_case(
        self, totalmobile_request: TotalMobileIncomingUpdateRequestModel
    ) -> None:
        pass

    def validate_questionnaire_exists(self, questionnaire_name: str) -> None:
        if not self._blaise_service.questionnaire_exists(questionnaire_name):
            logging.error(
                f"Could not find questionnaire {questionnaire_name} in Blaise"
            )
            raise QuestionnaireDoesNotExistError()

        logging.info(f"Successfully found questionnaire {questionnaire_name} in Blaise")
