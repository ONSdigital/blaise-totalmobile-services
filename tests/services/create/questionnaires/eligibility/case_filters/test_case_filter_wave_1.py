import logging
from typing import Dict

import pytest

from enums.blaise_fields import BlaiseFields
from models.common.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from models.create.blaise.blaise_lms_create_case_model import BlaiseLMSCreateCaseModel
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_1 import (
    CaseFilterWave1,
)


@pytest.fixture()
def service() -> CaseFilterWave1:
    return CaseFilterWave1()


@pytest.fixture()
def valid_wave_1_case_data() -> Dict[str, str]:
    return {
        BlaiseFields.case_id: "90001",
        BlaiseFields.wave: "1",
        BlaiseFields.field_case: "Y",
        BlaiseFields.outcome_code: "310",
        BlaiseFields.telephone_number_1: "",
        BlaiseFields.telephone_number_2: "",
        BlaiseFields.appointment_telephone_number: "",
        BlaiseFields.field_region: "Region 1",
    }


def test_valid_outcome_codes_has_not_changed(
    service: CaseFilterWave1,
):
    # assert
    assert service.valid_outcome_codes == [0, 310, 320]


@pytest.mark.parametrize("outcome_code", ["0", "310", "320"])
def test_case_is_eligible_returns_true_only_where_criteria_for_wave_1_is_met(
    outcome_code,
    valid_wave_1_case_data,
    service: CaseFilterWave1,
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.outcome_code] = outcome_code
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is True


def test_case_is_eligible_returns_false_if_the_case_is_not_wave_1(
    valid_wave_1_case_data,
    service: CaseFilterWave1,
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.wave] = "2"
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


def test_case_is_eligible_returns_false_if_telephone_number_1_has_a_value(
    valid_wave_1_case_data,
    service: CaseFilterWave1,
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.telephone_number_1] = "07656775679"
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


def test_case_is_eligible_logs_a_message_if_telephone_number_1_has_a_value(
    valid_wave_1_case_data, service: CaseFilterWave1, caplog
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.telephone_number_1] = "07656775679"
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
        "root",
        logging.INFO,
        "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_1'",
    ) in caplog.record_tuples


def test_case_is_eligible_returns_false_if_telephone_number_2_has_a_value(
    valid_wave_1_case_data,
    service: CaseFilterWave1,
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.telephone_number_2] = "07656775679"
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


def test_case_is_eligible_logs_a_message_if_telephone_number_2_has_a_value(
    valid_wave_1_case_data, service: CaseFilterWave1, caplog
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.telephone_number_2] = "07656775679"
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
        "root",
        logging.INFO,
        "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'telephone_number_2'",
    ) in caplog.record_tuples


def test_case_is_eligible_returns_false_if_appointment_telephone_number_has_a_value(
    valid_wave_1_case_data,
    service: CaseFilterWave1,
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.appointment_telephone_number] = "07656775679"
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


def test_case_is_eligible_logs_a_message_if_appointment_telephone_number_has_a_value(
    valid_wave_1_case_data, service: CaseFilterWave1, caplog
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.appointment_telephone_number] = "07656775679"
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
        "root",
        logging.INFO,
        "Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value set for the field 'appointment_telephone_number'",
    ) in caplog.record_tuples


@pytest.mark.parametrize("test_input", ["110", "210", "410"])
def test_case_is_eligible_returns_false_if_outcome_code_is_not_in_acceptable_range(
    test_input,
    valid_wave_1_case_data,
    service: CaseFilterWave1,
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.outcome_code] = test_input
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("test_input", ["110", "210", "410"])
def test_case_is_eligible_logs_a_message_if_outcome_code_is_not_in_acceptable_range(
    test_input, valid_wave_1_case_data, service: CaseFilterWave1, caplog
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.outcome_code] = test_input
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

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
    valid_wave_1_case_data,
    service: CaseFilterWave1,
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.field_case] = test_input
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("test_input", ["", "N", "n"])
def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n(
    test_input, valid_wave_1_case_data, service: CaseFilterWave1, caplog
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.field_case] = test_input
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

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
    valid_wave_1_case_data,
    service: CaseFilterWave1,
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.field_region] = test_input
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("test_input", ["Region 0", "Region 9", "Default"])
def test_case_is_eligible_logs_a_message_if_field_region_is_not_in_range(
    test_input, valid_wave_1_case_data, service: CaseFilterWave1, caplog
):
    # arrange
    valid_wave_1_case_data[BlaiseFields.field_region] = test_input
    case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_wave_1_case_data, None)

    value_range = TotalmobileWorldModel.get_available_regions()

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
        "root",
        logging.INFO,
        f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{test_input}' outside of the range '{value_range}' set for the field 'field_region'",
    ) in caplog.record_tuples
