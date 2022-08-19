from models.blaise.update_blaise_case_model import UpdateBlaiseCaseModel
from models.totalmobile.totalmobile_incoming_update_request_model import TotalMobileIncomingUpdateRequestModel


def test_import_case_returns_a_populated_model():
    # arrange
    totalmobile_request = TotalMobileIncomingUpdateRequestModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123"
    )

    # act
    result = UpdateBlaiseCaseModel.import_case(totalmobile_request)

    # assert
    assert result.questionnaire_name == "LMS2101_AA1"
    assert result.case_id == "90001"
    assert result.outcome_code == 300
    assert result.contact_name == "Joe Bloggs"
    assert result.home_phone_number == "01234567890"
    assert result.mobile_phone_number == "07123123123"
