from abc import abstractmethod

from models.update.totalmobile_incoming_update_request_model import TotalMobileIncomingUpdateRequestModel
from services.blaise_service import RealBlaiseService


class UpdateCaseServiceBase:
    def __init__(self, blaise_service: RealBlaiseService):
        self._blaise_service = blaise_service

    @abstractmethod
    def update_case(self, totalmobile_request: TotalMobileIncomingUpdateRequestModel) -> None:
        pass
