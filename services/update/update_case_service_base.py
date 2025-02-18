import logging
from abc import ABC, abstractmethod
from typing import Dict, Generic, TypeVar

from app.exceptions.custom_exceptions import (
    QuestionnaireCaseDoesNotExistError,
    QuestionnaireCaseError,
    QuestionnaireDoesNotExistError,
)
from models.update.blaise_update_case_model_base import BlaiseUpdateCaseBase
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.blaise_service import RealBlaiseService

BlaiseUpdateCaseBaseType = TypeVar(
    "BlaiseUpdateCaseBaseType", bound=BlaiseUpdateCaseBase
)


class UpdateCaseServiceBase(ABC, Generic[BlaiseUpdateCaseBaseType]):
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

    def get_existing_blaise_case(
        self,
        questionnaire_name: str,
        case_id: str,
    ) -> BlaiseUpdateCaseBaseType:
        try:
            case = self._blaise_service.get_case(questionnaire_name, case_id)
        except QuestionnaireCaseDoesNotExistError as err:
            logging.error(
                f"Could not find case {case_id} for questionnaire {questionnaire_name} in Blaise"
            )
            raise err
        except QuestionnaireCaseError as err:
            logging.error(
                f"There was an error retrieving case {case_id} for questionnaire {questionnaire_name} in Blaise"
            )
            raise err

        logging.info(
            f"Successfully found case {case_id} for questionnaire {questionnaire_name} in Blaise"
        )
        return self._return_survey_type_update_case_model(questionnaire_name, case)

    @abstractmethod
    def _return_survey_type_update_case_model(
        self, questionnaire_name: str, case: Dict[str, str]
    ) -> BlaiseUpdateCaseBaseType:
        pass
