import logging

import pytest

from services import eligible_blaise_case_service
from tests.helpers.questionnaire_case_model_helper import get_populated_case_model


def test_get_eligible_cases_returns_cases_only_where_criteria_is_met():
    # arrange
    cases = [
        # should return
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90002",
            telephone_number_1="123435",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90003",
            telephone_number_1="",
            telephone_number_2="123435",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90004",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="123435",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90005",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="2",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90006",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="6",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90007",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="410"
        ),
        # should return
        get_populated_case_model(
            case_id="90008",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="0"
        ),
        # should return
        get_populated_case_model(
            case_id="90009",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="2",
            outcome_code="0"
        ),
        # should return
        get_populated_case_model(
            case_id="90010",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="3",
            outcome_code="0"
        ),
        # should return
        get_populated_case_model(
            case_id="90011",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="4",
            outcome_code="0"
        ),
        # should return
        get_populated_case_model(
            case_id="90012",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="5",
            outcome_code="0"
        ),
        # should return
        get_populated_case_model(
            case_id="90013",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="5",
            outcome_code=""
        )
    ]

    # act
    result = eligible_blaise_case_service.get_eligible_cases(cases)

    # assert
    assert len(result) == 7

    assert result == [
        # should return
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should return
        get_populated_case_model(
            case_id="90008",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="0"
        ),
        get_populated_case_model(
            case_id="90009",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="2",
            outcome_code="0"
        ),
        get_populated_case_model(
            case_id="90010",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="3",
            outcome_code="0"
        ),
        get_populated_case_model(
            case_id="90011",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="4",
            outcome_code="0"
        ),
        get_populated_case_model(
            case_id="90012",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="5",
            outcome_code="0"
        ),
        get_populated_case_model(
            case_id="90013",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="5",
            outcome_code=""
        )
    ]


def test_filter_eligible_cases_logs_all_cases_appropriately(caplog):
    # arrange
    cases = [
        # should return
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90002",
            telephone_number_1="123435",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90003",
            telephone_number_1="",
            telephone_number_2="123435",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90004",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="123435",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90005",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="2",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90006",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="6",
            outcome_code="310"
        ),
        # should not return
        get_populated_case_model(
            case_id="90007",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="410"
        ),
        # should return
        get_populated_case_model(
            case_id="90008",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="0"
        ),
        # should return
        get_populated_case_model(
            case_id="90009",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="2",
            outcome_code="0"
        ),
        # should return
        get_populated_case_model(
            case_id="90010",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="3",
            outcome_code="0"
        ),
        # should return
        get_populated_case_model(
            case_id="90011",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="4",
            outcome_code="0"
        ),
        # should return
        get_populated_case_model(
            case_id="90012",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="5",
            outcome_code="0"
        ),
        # should return
        get_populated_case_model(
            case_id="90013",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="5",
            outcome_code=""
        )
    ]

    # act
    result = eligible_blaise_case_service.get_eligible_cases(cases)

    # assert
    assert len(result) == 7

    assert ('root', logging.INFO, "Case '90001' in questionnaire 'LMS2101_AA1' was eligible and will be included") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90002' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value set for the field 'telephone_number_1'") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90003' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value set for the field 'telephone_number_2'") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90004' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value set for the field 'appointment_telephone_number'") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90005' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value '2' outside of the range '['1']' set for the field 'wave'") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90006' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value '6' outside of the range '['1', '2', '3', '4', '5']' set for the field 'priority'") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90007' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value '410' outside of the range '['', '0', '310']' set for the field 'outcome_code'") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90008' in questionnaire 'LMS2101_AA1' was eligible and will be included") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90009' in questionnaire 'LMS2101_AA1' was eligible and will be included") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90010' in questionnaire 'LMS2101_AA1' was eligible and will be included") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90011' in questionnaire 'LMS2101_AA1' was eligible and will be included") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90012' in questionnaire 'LMS2101_AA1' was eligible and will be included") in caplog.record_tuples
    assert ('root', logging.INFO, "Case '90013' in questionnaire 'LMS2101_AA1' was eligible and will be included") in caplog.record_tuples


def test_get_eligible_cases_logs_a_message_when_a_case_is_not_eligible_as_telephone_number_1_has_a_value(caplog):
    # arrange
    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="3535232",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        )
    ]

    # act
    result = eligible_blaise_case_service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert ('root', logging.INFO, "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value set for the field 'telephone_number_1'") in caplog.record_tuples


def test_get_eligible_cases_logs_a_message_when_a_case_is_not_eligible_as_telephone_number_2_has_a_value(caplog):
    # arrange
    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="2221221",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        )
    ]

    # act
    result = eligible_blaise_case_service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert ('root', logging.INFO, "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value set for the field 'telephone_number_2'") in caplog.record_tuples


def test_get_eligible_cases_logs_a_message_when_a_case_is_not_eligible_as_appointment_telephone_number_has_a_value(caplog):
    # arrange
    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="2221221",
            wave="1",
            priority="1",
            outcome_code="310"
        )
    ]

    # act
    result = eligible_blaise_case_service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert ('root', logging.INFO, "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value set for the field 'appointment_telephone_number'") in caplog.record_tuples


@pytest.mark.parametrize("test_input", ["2", "3", "4", "5"])
def test_get_eligible_cases_logs_a_message_when_a_wave_is_not_in_range(test_input, caplog):
    # arrange
    value_range = ["1"]

    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=test_input,
            priority="1",
            outcome_code="310"
        )
    ]

    # act
    result = eligible_blaise_case_service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert ('root', logging.INFO, f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value '{test_input}' outside of the range '{value_range}' set for the field 'wave'") in caplog.record_tuples


@pytest.mark.parametrize("test_input", ["", "6", "7", "8"])
def test_get_eligible_cases_logs_a_message_when_a_priority_is_not_in_range(test_input, caplog):
    # arrange
    value_range = ["1", "2", "3", "4", "5"]

    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority=test_input,
            outcome_code="310"
        )
    ]

    # act
    result = eligible_blaise_case_service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert ('root', logging.INFO, f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value '{test_input}' outside of the range '{value_range}' set for the field 'priority'") in caplog.record_tuples


@pytest.mark.parametrize("test_input", ["110", "210", "410"])
def test_get_eligible_cases_logs_a_message_when_a_priority_is_not_in_range(test_input, caplog):
    # arrange
    value_range = ["", "0", "310"]

    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code=test_input
        )
    ]

    # act
    result = eligible_blaise_case_service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert ('root', logging.INFO, f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to totalmobile as it has a value '{test_input}' outside of the range '{value_range}' set for the field 'outcome_code'") in caplog.record_tuples