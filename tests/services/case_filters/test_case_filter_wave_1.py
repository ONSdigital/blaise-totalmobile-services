import logging

import pytest

from models.blaise.blaise_lms_case_information_model import (
    BlaiseLMSCaseInformationModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from services.case_filters.case_filter_wave_1 import CaseFilterWave1
from tests.helpers.lms_case_model_helper import get_lms_populated_case_model


@pytest.fixture()
def service() -> CaseFilterWave1:
    return CaseFilterWave1()


@pytest.fixture()
def valid_wave_1_case() -> BlaiseLMSCaseInformationModel:
    return get_lms_populated_case_model(
        case_id="90001",
        telephone_number_1="",
        telephone_number_2="",
        appointment_telephone_number="",
        wave=1,
        field_case="Y",
        outcome_code=310,
        field_region="Region 1",
    )


def test_valid_outcome_codes_has_not_changed(
    service: CaseFilterWave1,
):
    # assert
    assert service.valid_outcome_codes == [0, 310, 320]


@pytest.mark.parametrize("outcome_code", [0, 310, 320])
def test_case_is_eligible_returns_true_only_where_criteria_for_wave_1_is_met(
    outcome_code,
    valid_wave_1_case,
    service: CaseFilterWave1,
):
    # arrange
    case = valid_wave_1_case
    case.outcome_code = outcome_code

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is True


def test_case_is_eligible_returns_false_if_the_case_is_not_wave_1(
    valid_wave_1_case,
    service: CaseFilterWave1,
):
    # arrange
    case = valid_wave_1_case
    case.wave = 2

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


def test_case_is_eligible_returns_false_if_telephone_number_1_has_a_value(
    valid_wave_1_case,
    service: CaseFilterWave1,
):
    # arrange
    case = valid_wave_1_case
    case.contact_details.telephone_number_1 = "07656775679"

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


def test_case_is_eligible_logs_a_message_if_telephone_number_1_has_a_value(
    valid_wave_1_case, service: CaseFilterWave1, caplog
):
    # arrange
    case = valid_wave_1_case
    case.contact_details.telephone_number_1 = "07656775679"

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
        "root",
        logging.INFO,
        "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_1'",
    ) in caplog.record_tuples


def test_case_is_eligible_returns_false_if_telephone_number_2_has_a_value(
    valid_wave_1_case,
    service: CaseFilterWave1,
):
    # arrange
    case = valid_wave_1_case
    case.contact_details.telephone_number_2 = "07656775679"

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


def test_case_is_eligible_logs_a_message_if_telephone_number_2_has_a_value(
    valid_wave_1_case, service: CaseFilterWave1, caplog
):
    # arrange
    case = valid_wave_1_case
    case.contact_details.telephone_number_2 = "07656775679"

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
        "root",
        logging.INFO,
        "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_2'",
    ) in caplog.record_tuples


def test_case_is_eligible_returns_false_if_appointment_telephone_number_has_a_value(
    valid_wave_1_case,
    service: CaseFilterWave1,
):
    # arrange
    case = valid_wave_1_case
    case.contact_details.appointment_telephone_number = "07656775679"

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


def test_case_is_eligible_logs_a_message_if_appointment_telephone_number_has_a_value(
    valid_wave_1_case, service: CaseFilterWave1, caplog
):
    # arrange
    case = valid_wave_1_case
    case.contact_details.appointment_telephone_number = "07656775679"

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
        "root",
        logging.INFO,
        "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'appointment_telephone_number'",
    ) in caplog.record_tuples


@pytest.mark.parametrize("test_input", [110, 210, 410])
def test_case_is_eligible_returns_false_if_outcome_code_is_not_in_acceptable_range(
    test_input,
    valid_wave_1_case,
    service: CaseFilterWave1,
):
    # arrange
    case = valid_wave_1_case
    case.outcome_code = test_input

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("test_input", [110, 210, 410])
def test_case_is_eligible_logs_a_message_if_outcome_code_is_not_in_acceptable_range(
    test_input, valid_wave_1_case, service: CaseFilterWave1, caplog
):
    # arrange
    case = valid_wave_1_case
    case.outcome_code = test_input

    valid_outcome_codes = service.valid_outcome_codes

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
        "root",
        logging.INFO,
        f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{test_input}' outside of the range '{valid_outcome_codes}' set for the field 'outcome_code'",
    ) in caplog.record_tuples


@pytest.mark.parametrize("test_input", ["", "N", "n"])
def test_case_is_eligible_returns_false_if_field_case_is_not_set_to_y(
    test_input,
    valid_wave_1_case,
    service: CaseFilterWave1,
):
    # arrange
    case = valid_wave_1_case
    case.field_case = test_input

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("test_input", ["", "N", "n"])
def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n(
    test_input, valid_wave_1_case, service: CaseFilterWave1, caplog
):
    # arrange
    case = valid_wave_1_case
    case.field_case = test_input

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
        "root",
        logging.INFO,
        f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of '{test_input}', not 'Y'",
    ) in caplog.record_tuples


@pytest.mark.parametrize("test_input", ["Region 0", "Region 9", "Default"])
def test_case_is_eligible_returns_false_if_field_region_is_not_in_range(
    test_input,
    valid_wave_1_case,
    service: CaseFilterWave1,
):
    # arrange
    case = valid_wave_1_case
    case.field_region = test_input

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("test_input", ["Region 0", "Region 9", "Default"])
def test_case_is_eligible_logs_a_message_if_field_region_is_not_in_range(
    test_input, valid_wave_1_case, service: CaseFilterWave1, caplog
):
    # arrange
    case = valid_wave_1_case
    case.field_region = test_input

    value_range = TotalmobileWorldModel.get_available_regions()

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
        "root",
        logging.INFO,
        f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{test_input}' outside of the range '{value_range}' set for the field 'field_region'",
    ) in caplog.record_tuples
