import pytest

from app.exceptions.custom_exceptions import QuestionnaireCaseDoesNotExistError
from enums.blaise_fields import BlaiseFields
from models.create.blaise.blaise_lms_create_case_model import BlaiseLMSCreateCaseModel
from tests.fakes.fake_blaise_service import FakeBlaiseService


@pytest.fixture()
def service() -> FakeBlaiseService:
    return FakeBlaiseService()


def test_questionnaire_exists(service: FakeBlaiseService):
    service.add_questionnaire("LMS11111")
    service.add_questionnaire("LMS22222")

    assert service.questionnaire_exists("LMS11111")
    assert service.questionnaire_exists("LMS22222")
    assert not service.questionnaire_exists("LMS88888")
    assert not service.questionnaire_exists("LMS99999")


def test_add_case_when_questionnaire_does_not_exist(service: FakeBlaiseService):
    with pytest.raises(
        QuestionnaireCaseDoesNotExistError,
        match=f"Questionnaire 'unknown' does not exist",
    ):
        service.add_case_to_questionnaire("unknown", "12345")


def test_update_outcome_code_of_case_in_questionnaire_when_questionnaire_does_not_exist(
    service: FakeBlaiseService,
):
    with pytest.raises(
        QuestionnaireCaseDoesNotExistError,
        match=f"Questionnaire 'unknown' does not exist",
    ):
        service.update_outcome_code_of_case_in_questionnaire("unknown", "12345", "310")


def test_update_outcome_code_of_case_in_questionnaire_when_case_does_not_exist(
    service: FakeBlaiseService,
):
    service.add_questionnaire("LMS12345")
    with pytest.raises(
        QuestionnaireCaseDoesNotExistError,
        match=f"Case '12345' for questionnaire 'LMS12345' does not exist",
    ):
        service.update_outcome_code_of_case_in_questionnaire("LMS12345", "12345", "310")


def test_update_outcome_code_of_case_in_questionnaire(service: FakeBlaiseService):
    service.add_questionnaire("LMS12345")
    service.add_case_to_questionnaire("LMS12345", "11111")
    service.update_outcome_code_of_case_in_questionnaire("LMS12345", "11111", "310")
    case = service.get_case("LMS12345", "11111")
    assert case["hOut"] == 310


def test_set_case_has_call_history_when_questionnaire_does_not_exist(
    service: FakeBlaiseService,
):
    with pytest.raises(
        QuestionnaireCaseDoesNotExistError,
        match=f"Questionnaire 'unknown' does not exist",
    ):
        service.set_case_has_call_history(False, "unknown", "12345")


def test_set_case_has_call_history_when_case_does_not_exist(service: FakeBlaiseService):
    service.add_questionnaire("LMS12345")
    with pytest.raises(
        QuestionnaireCaseDoesNotExistError,
        match=f"Case '12345' for questionnaire 'LMS12345' does not exist",
    ):
        service.set_case_has_call_history(False, "LMS12345", "12345")


def test_set_case_has_call_history(service: FakeBlaiseService):
    service.add_questionnaire("LMS12345")
    service.add_case_to_questionnaire("LMS12345", "11111")
    service.add_case_to_questionnaire("LMS12345", "22222")
    service.set_case_has_call_history(True, "LMS12345", "11111")
    service.set_case_has_call_history(False, "LMS12345", "22222")
    assert service.get_case("LMS12345", "11111")[
        "catiMana.CatiCall.RegsCalls[1].DialResult"
    ]
    assert not service.get_case("LMS12345", "22222")[
        "catiMana.CatiCall.RegsCalls[1].DialResult"
    ]


def test_get_case_when_questionnaire_does_not_exist(service: FakeBlaiseService):
    with pytest.raises(
        QuestionnaireCaseDoesNotExistError,
        match=f"Questionnaire 'unknown' does not exist",
    ):
        service.get_case("unknown", "12345")


def test_get_case_when_case_does_not_exist(service: FakeBlaiseService):
    service.add_questionnaire("LMS22222")
    with pytest.raises(
        QuestionnaireCaseDoesNotExistError,
        match=f"Case '12345' for questionnaire 'LMS22222' does not exist",
    ):
        service.get_case("LMS22222", "12345")


def test_get_case_when_case_exists(service: FakeBlaiseService):
    service.add_questionnaire("LMS12345")
    service.add_case_to_questionnaire("LMS12345", "99999")

    case = service.get_case("LMS12345", "99999")
    assert case == {
        BlaiseFields.call_history: False,
        BlaiseFields.outcome_code: 0,
        BlaiseFields.field_case: "None",
        BlaiseFields.field_region: "None",
        BlaiseFields.tla: "LMS",
        BlaiseFields.telephone_number_1: "None",
        BlaiseFields.telephone_number_2: "None",
        BlaiseFields.wave: "None",
        BlaiseFields.rotational_knock_to_nudge_indicator: "None",
        BlaiseFields.rotational_outcome_code: 0,
        BlaiseFields.case_id: "99999",
        BlaiseFields.appointment_telephone_number: "None",
    }


def test_case_has_been_updated_when_update_case_has_not_been_called(
    service: FakeBlaiseService,
):
    assert service.case_has_been_updated("LMS12345", "12345") is False


def test_case_has_been_updated_when_update_case_has_been_called(
    service: FakeBlaiseService,
):
    service.update_case("LMS12345", "11111", dict())
    assert service.case_has_been_updated("LMS12345", "11111") is True
    assert service.case_has_been_updated("LMS12345", "22222") is False


def test_get_updates_when_questionnaire_cases_have_not_been_updated(
    service: FakeBlaiseService,
):
    with pytest.raises(
        Exception,
        match="No update has been performed for case '12345' in questionnaire 'unknown'",
    ):
        service.get_updates("unknown", "12345")


def test_get_updates_when_case_has_not_been_updated(service: FakeBlaiseService):
    service.update_case("LMS12345", "11111", dict(field="value"))
    with pytest.raises(
        Exception,
        match="No update has been performed for case '99999' in questionnaire 'LMS12345'",
    ):
        service.get_updates("LMS12345", "99999")


def test_get_updates_when_updates_occurred(service: FakeBlaiseService):
    service.update_case("LMS12345", "11111", dict(field1="value1", field2="value2"))
    service.update_case("LMS12345", "22222", dict(field2="value2", field3="value3"))
    assert service.get_updates("LMS12345", "11111") == dict(
        field1="value1", field2="value2"
    )
    assert service.get_updates("LMS12345", "22222") == dict(
        field2="value2", field3="value3"
    )


def test_get_updates_when_overwrite_occurred(service: FakeBlaiseService):
    service.add_questionnaire("LMS12345")
    service.add_case_to_questionnaire("LMS12345", "11111")
    service.update_case(
        "LMS12345", "11111", dict(field1="old value", field2="existing")
    )
    service.update_case("LMS12345", "11111", dict(field1="new value"))
    assert service.get_updates("LMS12345", "11111") == dict(
        field1="new value", field2="existing"
    )


def test_get_cases_called_count(service: FakeBlaiseService):
    # arrange
    service.add_questionnaire("LMS12345")
    service.add_questionnaire("LMS56789")
    service.add_questionnaire("LMS22468")
    required_fields = BlaiseLMSCreateCaseModel.required_fields()

    # act
    service.get_cases("LMS12345", required_fields)
    service.get_cases("LMS12345", required_fields)
    service.get_cases("LMS56789", required_fields)

    # assert
    assert service.get_cases_call_count("LMS12345") == 2
    assert service.get_cases_call_count("LMS56789") == 1
    assert service.get_cases_call_count("LMS22468") == 0
