import logging

import pytest

from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from services.eligible_case_service import EligibleCaseService
from tests.helpers.get_blaise_case_model_helper import get_populated_case_model


@pytest.fixture()
def service() -> EligibleCaseService:
    return EligibleCaseService()


def test_get_eligible_cases_returns_cases_only_where_criteria_is_met(
    service: EligibleCaseService,
):
    # arrange
    cases = [
        # should return
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="Y",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90002",
            telephone_number_1="123435",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="Y",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90003",
            telephone_number_1="",
            telephone_number_2="123435",
            appointment_telephone_number="",
            wave=1,
            field_case="Y",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90004",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="123435",
            wave=1,
            field_case="Y",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90005",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=2,
            field_case="Y",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90006",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=2,
            field_case="N",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90007",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="Y",
            outcome_code=410,
            field_region="Region 1",
        ),
        # should return
        get_populated_case_model(
            case_id="90008",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="y",
            outcome_code=0,
            field_region="Region 8",
        ),
        # should not return
        get_populated_case_model(
            case_id="90009",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="y",
            outcome_code=0,
            field_region="Region 9",
        ),
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 2

    assert result == [
        # should return
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="Y",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should return
        get_populated_case_model(
            case_id="90008",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="y",
            outcome_code=0,
            field_region="Region 8",
        ),
    ]


def test_get_eligible_cases_logs_all_cases_appropriately(
    service: EligibleCaseService, caplog
):
    # arrange
    cases = [
        # should return
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="Y",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90002",
            telephone_number_1="123435",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="Y",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90003",
            telephone_number_1="",
            telephone_number_2="123435",
            appointment_telephone_number="",
            wave=1,
            field_case="Y",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90004",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="123435",
            wave=1,
            field_case="Y",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90005",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=2,
            field_case="Y",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90006",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="N",
            outcome_code=310,
            field_region="Region 1",
        ),
        # should not return
        get_populated_case_model(
            case_id="90007",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="Y",
            outcome_code=410,
            field_region="Region 1",
        ),
        # should return
        get_populated_case_model(
            case_id="90008",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="y",
            outcome_code=0,
            field_region="Region 8",
        ),
        # should not return
        get_populated_case_model(
            case_id="90009",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="y",
            outcome_code=0,
            field_region="Region 9",
        ),
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 2

    assert (
        "root",
        logging.INFO,
        "Case '90001' in questionnaire 'LMS2101_AA1' was eligible and will be included",
    ) in caplog.record_tuples
    assert (
        "root",
        logging.INFO,
        "Case '90002' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_1'",
    ) in caplog.record_tuples
    assert (
        "root",
        logging.INFO,
        "Case '90003' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_2'",
    ) in caplog.record_tuples
    assert (
        "root",
        logging.INFO,
        "Case '90004' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'appointment_telephone_number'",
    ) in caplog.record_tuples
    assert (
        "root",
        logging.INFO,
        "Case '90006' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of 'N', not 'Y'",
    ) in caplog.record_tuples
    assert (
        "root",
        logging.INFO,
        "Case '90007' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '410' outside of the range '[0, 310, 320]' set for the field 'outcome_code'",
    ) in caplog.record_tuples
    assert (
        "root",
        logging.INFO,
        "Case '90008' in questionnaire 'LMS2101_AA1' was eligible and will be included",
    ) in caplog.record_tuples
    assert (
        "root",
        logging.INFO,
        f"Case '90009' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value 'Region 9' outside of the range '{TotalmobileWorldModel.get_available_regions()}' set for the field 'field_region'",
    ) in caplog.record_tuples


def test_get_eligible_cases_logs_a_message_when_a_case_is_not_eligible_as_telephone_number_1_has_a_value(
    service: EligibleCaseService,
    caplog,
):
    # arrange
    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="3535232",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            priority="1",
            outcome_code=310,
            field_region="Region 1",
        )
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert (
        "root",
        logging.INFO,
        "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_1'",
    ) in caplog.record_tuples


def test_get_eligible_cases_logs_a_message_when_a_case_is_not_eligible_as_telephone_number_2_has_a_value(
    service: EligibleCaseService,
    caplog,
):
    # arrange
    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="2221221",
            appointment_telephone_number="",
            wave=1,
            priority="1",
            outcome_code=310,
            field_region="Region 1",
        )
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert (
        "root",
        logging.INFO,
        "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_2'",
    ) in caplog.record_tuples


def test_get_eligible_cases_logs_a_message_when_a_case_is_not_eligible_as_appointment_telephone_number_has_a_value(
    service: EligibleCaseService,
    caplog,
):
    # arrange
    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="2221221",
            wave=1,
            priority="1",
            outcome_code=310,
            field_region="Region 1",
        )
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert (
        "root",
        logging.INFO,
        "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'appointment_telephone_number'",
    ) in caplog.record_tuples


@pytest.mark.parametrize("test_input", [110, 210, 410])
def test_get_eligible_cases_logs_a_message_when_a_priority_is_not_in_range(
    test_input, service: EligibleCaseService, caplog
):
    # arrange
    value_range = [0, 310, 320]

    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            priority="1",
            outcome_code=test_input,
            field_region="Region 1",
        )
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert (
        "root",
        logging.INFO,
        f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{test_input}' outside of the range '{value_range}' set for the field 'outcome_code'",
    ) in caplog.record_tuples


def test_get_eligible_cases_logs_a_message_when_field_case_is_set_to_n(service, caplog):
    # arrange

    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="N",
            priority="1",
            outcome_code=310,
            field_region="Region 1",
        )
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert (
        "root",
        logging.INFO,
        f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of 'N', not 'Y'",
    ) in caplog.record_tuples


def test_get_eligible_cases_logs_a_message_when_field_case_is_set_to_N_and_priority_is_missing(
    service: EligibleCaseService,
    caplog,
):
    # arrange

    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="N",
            outcome_code=310,
            field_region="Region 1",
        )
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert (
        "root",
        logging.INFO,
        f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of 'N', not 'Y'",
    ) in caplog.record_tuples


def test_get_eligible_cases_logs_a_message_when_field_case_is_set_to_an_empty_string(
    service: EligibleCaseService,
    caplog,
):
    # arrange

    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            field_case="",
            outcome_code=310,
            field_region="Region 1",
        )
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert (
        "root",
        logging.INFO,
        f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of '', not 'Y'",
    ) in caplog.record_tuples


@pytest.mark.parametrize("test_input", ["Region 0", "Region 9", "Default"])
def test_get_eligible_cases_logs_a_message_when_a_field_region_is_not_in_range(
    test_input, service: EligibleCaseService, caplog
):
    # arrange
    value_range = TotalmobileWorldModel.get_available_regions()

    cases = [
        get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=1,
            priority="1",
            outcome_code=310,
            field_region=test_input,
        )
    ]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 0

    assert (
        "root",
        logging.INFO,
        f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{test_input}' outside of the range '{value_range}' set for the field 'field_region'",
    ) in caplog.record_tuples
