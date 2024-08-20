import pytest

from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.update.mappers.blaise_update_case_mapper_service import (
    BlaiseUpdateCaseMapperService,
)


class TestUpdateCaseMapping:
    @pytest.fixture()
    def service(self) -> BlaiseUpdateCaseMapperService:
        return BlaiseUpdateCaseMapperService()

    def test_import_case_returns_a_populated_model(
        self, service: BlaiseUpdateCaseMapperService
    ):
        # arrange
        totalmobile_request = TotalMobileIncomingUpdateRequestModel(
            questionnaire_name="LMS2101_AA1",
            case_id="90001",
            outcome_code=300,
            contact_name="Joe Bloggs",
            home_phone_number="01234567890",
            mobile_phone_number="07123123123",
        )

        # act
        result = service.map_update_case_model(totalmobile_request)

        # assert
        assert result.questionnaire_name == "LMS2101_AA1"
        assert result.case_id == "90001"
        assert result.outcome_code == 300
        assert result.contact_name == "Joe Bloggs"
        assert result.home_phone_number == "01234567890"
        assert result.mobile_phone_number == "07123123123"
