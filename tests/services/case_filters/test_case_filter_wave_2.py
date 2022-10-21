import logging

import pytest

from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from services.case_filters.case_filter_wave_2 import CaseFilterWave2
from tests.helpers.get_blaise_case_model_helper import get_populated_case_model


@pytest.fixture()
def service() -> CaseFilterWave2:
    return CaseFilterWave2()


@pytest.fixture()
def valid_wave_2_case_without_telephone_numbers() -> BlaiseCaseInformationModel:
    return get_populated_case_model(
            case_id="90001",
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave=2,
            field_case="Y",
            outcome_code=310,
            rotational_knock_to_nudge_indicator="N",
            rotational_outcome_code=310,
            field_region="Region 1",
        )


def test_valid_outcome_codes_has_not_changed(
    service: CaseFilterWave2,
):
    # assert
    assert service.valid_outcome_codes == [0, 310]
    assert service.valid_rotational_outcome_codes == [0, 310]


@pytest.mark.parametrize("knock_to_nudge_indicator", ["", "n", "N"])
def test_case_is_eligible_returns_true_only_where_criteria_for_wave_2_without_telephone_is_met(
    knock_to_nudge_indicator,
    valid_wave_2_case_without_telephone_numbers,
    service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.rotational_knock_to_nudge_indicator = knock_to_nudge_indicator

    # act
    result = service.case_is_eligible(valid_wave_2_case_without_telephone_numbers)

    # assert
    assert result is True


@pytest.mark.parametrize("outcome_code, rotational_outcome_code", [(0, 0), (310, 0), (0, 310), (310, 310)])
def test_case_is_eligible_returns_true_only_where_criteria_for_wave_2_without_telephone_is_met_for_all_outcome_codes(
    outcome_code,
    rotational_outcome_code,
    valid_wave_2_case_without_telephone_numbers,
    service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.outcome_code = outcome_code
    case.rotational_outcome_code = rotational_outcome_code

    # act
    result = service.case_is_eligible(valid_wave_2_case_without_telephone_numbers)

    # assert
    assert result is True


@pytest.mark.parametrize("outcome_code, rotational_outcome_code", [(0, 0), (310, 0), (0, 310), (310, 310)])
def test_case_is_eligible_returns_true_only_where_criteria_for_wave_2_when_telephone_number_1_is_set(
    outcome_code,
    rotational_outcome_code,
    valid_wave_2_case_without_telephone_numbers,
    service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.outcome_code = outcome_code
    case.rotational_outcome_code = rotational_outcome_code
    case.contact_details.telephone_number_1 = "07656775679"

    # act
    result = service.case_is_eligible(valid_wave_2_case_without_telephone_numbers)

    # assert
    assert result is True


@pytest.mark.parametrize("outcome_code, rotational_outcome_code", [(0, 0), (310, 0), (0, 310), (310, 310)])
def test_case_is_eligible_returns_true_only_where_criteria_for_wave_2_when_telephone_number_2_is_set(
    outcome_code,
    rotational_outcome_code,
    valid_wave_2_case_without_telephone_numbers,
    service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.outcome_code = outcome_code
    case.rotational_outcome_code = rotational_outcome_code
    case.contact_details.telephone_number_2 = "07656775679"

    # act
    result = service.case_is_eligible(valid_wave_2_case_without_telephone_numbers)

    # assert
    assert result is True


@pytest.mark.parametrize("outcome_code, rotational_outcome_code", [(0, 0), (310, 0), (0, 310), (310, 310)])
def test_case_is_eligible_returns_true_only_where_criteria_for_wave_2_when_appointment_telephone_number_is_set(
    outcome_code,
    rotational_outcome_code,
    valid_wave_2_case_without_telephone_numbers,
    service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.outcome_code = outcome_code
    case.rotational_outcome_code = rotational_outcome_code
    case.contact_details.appointment_telephone_number = "07656775679"

    # act
    result = service.case_is_eligible(valid_wave_2_case_without_telephone_numbers)

    # assert
    assert result is True


def test_case_is_eligible_returns_false_if_the_case_is_not_wave_2(
    valid_wave_2_case_without_telephone_numbers,
    service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.wave = 3

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("field_case", ["", "N", "n"])
def test_case_is_eligible_returns_false_if_field_case_is_not_set_to_y_when_no_telephone_numbers_are_set(
        field_case,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.field_case = field_case

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("field_case", ["", "N", "n"])
def test_case_is_eligible_returns_false_if_field_case_is_not_set_to_y_when_telephone_number_1_is_set(
        field_case,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.field_case = field_case
    case.contact_details.telephone_number_1 = "07656775679"

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("field_case", ["", "N", "n"])
def test_case_is_eligible_returns_false_if_field_case_is_not_set_to_y_when_telephone_number_2_is_set(
        field_case,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.field_case = field_case
    case.contact_details.telephone_number_2 = "07656775679"

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("field_case", ["", "N", "n"])
def test_case_is_eligible_returns_false_if_field_case_is_not_set_to_y_when_appointment_telephone_number_is_set(
        field_case,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.field_case = field_case
    case.contact_details.appointment_telephone_number = "07656775679"

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("field_case", ["", "N", "n"])
def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n_when_no_telephone_numbers_are_set(
        field_case,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
        caplog
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.field_case = field_case

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
               "root",
               logging.INFO,
               f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of '{field_case}', not 'Y'",
           ) in caplog.record_tuples



@pytest.mark.parametrize("field_case", ["", "N", "n"])
def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n_when_when_telephone_number_1_is_set(
        field_case,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
        caplog
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.field_case = field_case
    case.contact_details.telephone_number_1 = "07656775679"

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
               "root",
               logging.INFO,
               f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of '{field_case}', not 'Y'",
           ) in caplog.record_tuples



@pytest.mark.parametrize("rotational_knock_to_nudge_indicator", ["y", "Y"])
def test_case_is_eligible_returns_false_if_rotational_knock_to_nudge_indicator_is_not_set_to_n_when_no_telephone_numbers_are_set(
        rotational_knock_to_nudge_indicator,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.rotational_knock_to_nudge_indicator = rotational_knock_to_nudge_indicator

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("rotational_knock_to_nudge_indicator", ["y", "Y"])
def test_case_is_eligible_does_not_return_false_if_rotational_knock_to_nudge_indicator_is_not_set_to_n_when_telephone_number_1_is_set(
        rotational_knock_to_nudge_indicator,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.rotational_knock_to_nudge_indicator = rotational_knock_to_nudge_indicator
    case.contact_details.telephone_number_1 = "07656775679"

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is True


@pytest.mark.parametrize("rotational_knock_to_nudge_indicator", ["y", "Y"])
def test_case_is_eligible_does_not_return_false_if_rotational_knock_to_nudge_indicator_is_not_set_to_n_when_telephone_number_2_is_set(
        rotational_knock_to_nudge_indicator,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.rotational_knock_to_nudge_indicator = rotational_knock_to_nudge_indicator
    case.contact_details.telephone_number_2 = "07656775679"

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is True


@pytest.mark.parametrize("rotational_knock_to_nudge_indicator", ["y", "Y"])
def test_case_is_eligible_does_not_return_false_if_rotational_knock_to_nudge_indicator_is_not_set_to_n_when_appointment_telephone_number_is_set(
        rotational_knock_to_nudge_indicator,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.rotational_knock_to_nudge_indicator = rotational_knock_to_nudge_indicator
    case.contact_details.appointment_telephone_number = "07656775679"

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is True


@pytest.mark.parametrize("rotational_knock_to_nudge_indicator", ["y", "Y"])
def test_case_is_eligible_logs_a_message_if_rotational_knock_to_nudge_indicator_is_not_set_to_n_when_no_telephone_numbers_are_set(
        rotational_knock_to_nudge_indicator,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
        caplog
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.rotational_knock_to_nudge_indicator = rotational_knock_to_nudge_indicator

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
               "root",
               logging.INFO,
               f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a knock to knudge indicator value of '{rotational_knock_to_nudge_indicator}', not 'N'",
           ) in caplog.record_tuples


@pytest.mark.parametrize("test_input", ["Region 0", "Region 9", "Default"])
def test_case_is_eligible_returns_false_if_field_region_is_not_in_range(
    test_input,
        valid_wave_2_case_without_telephone_numbers,
    service: CaseFilterWave2,
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.field_region = test_input

    # act
    result = service.case_is_eligible(case)

    # assert
    assert result is False


@pytest.mark.parametrize("field_region", ["Region 0", "Region 9", "Default"])
def test_case_is_eligible_logs_a_message_if_field_region_is_not_in_range(
        field_region,
        valid_wave_2_case_without_telephone_numbers,
        service: CaseFilterWave2,
        caplog
):
    # arrange
    case = valid_wave_2_case_without_telephone_numbers
    case.field_region = field_region

    value_range = TotalmobileWorldModel.get_available_regions()

    # act && assert
    with caplog.at_level(logging.INFO):
        service.case_is_eligible(case)
    assert (
        "root",
        logging.INFO,
        f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{field_region}' outside of the range '{value_range}' set for the field 'field_region'",
    ) in caplog.record_tuples

