from models.update.blaise_case_update_model import BlaiseCaseUpdateModel
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.create.mappers.blaise_mapper_base import MapperServiceBase


class BlaiseUpdateCaseMapperService(MapperServiceBase):
    def map_update_case_model(
        self, totalmobile_request: TotalMobileIncomingUpdateRequestModel
    ) -> BlaiseCaseUpdateModel:

        return BlaiseCaseUpdateModel(
            questionnaire_name=totalmobile_request.questionnaire_name,
            case_id=totalmobile_request.case_id,
            outcome_code=totalmobile_request.outcome_code,
            contact_name=totalmobile_request.contact_name,
            home_phone_number=totalmobile_request.home_phone_number,
            mobile_phone_number=totalmobile_request.mobile_phone_number,
        )
