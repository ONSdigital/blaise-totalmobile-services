from models.update.totalmobile_incoming_update_request_model import TotalMobileIncomingUpdateRequestModel


def lms_totalmobile_incoming_update_request_helper(
        questionnaire_name="LMS2101_AA1"
) -> TotalMobileIncomingUpdateRequestModel:
    return TotalMobileIncomingUpdateRequestModel(
        questionnaire_name=questionnaire_name,
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123",
    )