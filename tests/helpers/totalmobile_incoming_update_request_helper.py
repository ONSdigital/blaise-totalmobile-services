from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)


def lms_totalmobile_incoming_update_request_helper(
    questionnaire_name="LMS2101_AA1", case_id="90001", outcome_code=0
) -> TotalMobileIncomingUpdateRequestModel:
    return TotalMobileIncomingUpdateRequestModel(
        questionnaire_name=questionnaire_name,
        case_id=case_id,
        outcome_code=outcome_code,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123",
        refusal_reason=None,
    )


def frs_totalmobile_incoming_update_request_helper(
    questionnaire_name="FRS2102", case_id="90002", outcome_code=0
) -> TotalMobileIncomingUpdateRequestModel:
    return TotalMobileIncomingUpdateRequestModel(
        questionnaire_name=questionnaire_name,
        case_id=case_id,
        outcome_code=outcome_code,
        contact_name="Joe Bloggs Jr",
        home_phone_number="01234567891",
        mobile_phone_number="07123123124",
        refusal_reason=None,
    )
