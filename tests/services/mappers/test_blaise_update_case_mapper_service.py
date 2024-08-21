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

    def test_map_update_case_model_returns_a_populated_model(
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

    @pytest.mark.parametrize(
        "case_id, outcome_code, has_call_history",
        [
            ("10010", 301, False),
            ("9000", 110, True),
            ("1002", 210, False),
        ],
    )
    def test_map_blaise_update_case_information_model_returns_a_populated_model(
        self,
        service: BlaiseUpdateCaseMapperService,
        case_id: str,
        outcome_code: int,
        has_call_history: bool,
    ):
        # arrange
        case = {
            "qiD.Serial_Number": case_id,
            "hOut": str(outcome_code),
            "catiMana.CatiCall.RegsCalls[1].DialResult": "1"
            if has_call_history
            else "",
        }

        # act
        result = service.map_blaise_update_case_information_model(case)

        # assert
        assert result.case_id == case_id
        assert result.outcome_code == outcome_code
        assert result.has_call_history == has_call_history
