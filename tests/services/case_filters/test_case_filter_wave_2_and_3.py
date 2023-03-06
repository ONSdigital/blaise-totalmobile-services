import logging

import pytest

from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from services.case_filters.case_filter_base import CaseFilterBase
from services.case_filters.case_filter_wave_2 import CaseFilterWave2
from services.case_filters.case_filter_wave_3 import CaseFilterWave3
from tests.helpers.get_blaise_case_model_helper import get_populated_case_model


@pytest.fixture()
def valid_case_without_telephone_numbers() -> BlaiseCaseInformationModel:
    return get_populated_case_model(
        case_id="90001",
        telephone_number_1="",
        telephone_number_2="",
        appointment_telephone_number="",
        field_case="Y",
        outcome_code=310,
        rotational_outcome_code=310,
        field_region="Region 1",
    )


@pytest.fixture(scope="module", params=[CaseFilterWave2(), CaseFilterWave3()])
def service(request) -> CaseFilterBase:
    return request.param


def test_valid_outcome_codes_has_not_changed_for_wave_2():
    # arrange
    service = CaseFilterWave2()

    # act
    outcome_codes = service.valid_outcome_codes
    valid_rotational_outcome_codes = service.valid_rotational_outcome_codes

    # assert
    assert outcome_codes == [0, 310]
    assert valid_rotational_outcome_codes == [0, 310]


def test_valid_outcome_codes_has_not_changed_for_wave_3():
    # arrange
    service = CaseFilterWave3()

    # act
    outcome_codes = service.valid_outcome_codes
    valid_rotational_outcome_codes = service.valid_rotational_outcome_codes

    # assert
    assert outcome_codes == [0, 310]
    assert valid_rotational_outcome_codes == [0, 310]


class TestEligibleCasesWithoutTelephoneNumbers:
    @pytest.mark.parametrize("knock_to_nudge_indicator", ["", "n", "N"])
    def test_case_is_eligible_returns_true_only_where_criteria_without_telephone_is_met(
        self,
        knock_to_nudge_indicator,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.rotational_knock_to_nudge_indicator = knock_to_nudge_indicator

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [(0, 0), (310, 0), (0, 310), (310, 310)],
    )
    def test_case_is_eligible_returns_true_where_criteria_without_telephone_is_met_for_all_outcome_codes(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.outcome_code = outcome_code
        case.rotational_outcome_code = rotational_outcome_code

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True


class TestEligibleCasesWithATelephoneNumber:
    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [(0, 0), (310, 0), (0, 310), (310, 310)],
    )
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_all_outcome_codes_with_telephone_number_1_set(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.outcome_code = outcome_code
        case.rotational_outcome_code = rotational_outcome_code
        case.contact_details.telephone_number_1 = "07656775679"

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [(0, 0), (310, 0), (0, 310), (310, 310)],
    )
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_all_outcome_codes_with_telephone_number_2_set(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.outcome_code = outcome_code
        case.rotational_outcome_code = rotational_outcome_code
        case.contact_details.telephone_number_2 = "07656775679"

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [(0, 0), (310, 0), (0, 310), (310, 310)],
    )
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_all_outcome_codes_with_tappointment_telephone_number_set(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.outcome_code = outcome_code
        case.rotational_outcome_code = rotational_outcome_code
        case.contact_details.appointment_telephone_number = "07656775679"

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize("rotational_knock_to_nudge_indicator", ["y", "Y"])
    def test_case_is_eligible_returns_true_if_rotational_knock_to_nudge_indicator_is_not_set_to_n_when_telephone_number_1_is_set(
        self,
        rotational_knock_to_nudge_indicator,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.rotational_knock_to_nudge_indicator = rotational_knock_to_nudge_indicator
        case.contact_details.telephone_number_1 = "07656775679"

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize("rotational_knock_to_nudge_indicator", ["y", "Y"])
    def test_case_is_eligible_returns_true_if_rotational_knock_to_nudge_indicator_is_not_set_to_n_when_telephone_number_2_is_set(
        self,
        rotational_knock_to_nudge_indicator,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.rotational_knock_to_nudge_indicator = rotational_knock_to_nudge_indicator
        case.contact_details.telephone_number_2 = "07656775679"

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize("rotational_knock_to_nudge_indicator", ["y", "Y"])
    def test_case_is_eligible_returns_true_if_rotational_knock_to_nudge_indicator_is_not_set_to_n_when_appointment_telephone_number_is_set(
        self,
        rotational_knock_to_nudge_indicator,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.rotational_knock_to_nudge_indicator = rotational_knock_to_nudge_indicator
        case.contact_details.appointment_telephone_number = "07656775679"

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True


class TestCaseIsInCorrectWave:
    @pytest.mark.parametrize("wave_number", [0, 1, 4, 5])
    def test_case_is_eligible_returns_false_if_the_case_is_not_wave_2_or_3(
        self, valid_case_without_telephone_numbers, service: CaseFilterBase, wave_number
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = wave_number

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False


class TestIneligibleCasesWithoutTelephoneNumbers:
    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [(110, 0), (210, 0), (0, 110), (310, 210)],
    )
    def test_case_is_eligible_returns_false_for_all_invalid_outcome_codes_without_telephone_numbers(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.outcome_code = outcome_code
        case.rotational_outcome_code = rotational_outcome_code

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_returns_false_if_field_case_is_not_set_to_y_when_no_telephone_numbers_are_set(
        self,
        field_case,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.field_case = field_case

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n_when_no_telephone_numbers_are_set(
        self,
        field_case,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.field_case = field_case

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of '{field_case}', not 'Y'",
        ) in caplog.record_tuples

    # TODO: Amend refactored logic
    # TODO: Ask Sam. If ktn indicator is set, Y or N, what do we do?
    # @pytest.mark.parametrize("rotational_knock_to_nudge_indicator", ["y", "Y"])
    # def test_case_is_eligible_returns_false_if_rotational_knock_to_nudge_indicator_is_not_set_to_n_when_no_telephone_numbers_are_set(
    #     self,
    #     rotational_knock_to_nudge_indicator,
    #     valid_case_without_telephone_numbers,
    #     service: CaseFilterBase,
    # ):
    #     # arrange
    #     case = valid_case_without_telephone_numbers
    #     case.wave = service.wave_number
    #     case.rotational_knock_to_nudge_indicator = rotational_knock_to_nudge_indicator
    #
    #     # act
    #     result = service.case_is_eligible(case)
    #
    #     # assert
    #     assert result is False

    # TODO: Shimmy around refactored logic
    # @pytest.mark.parametrize("rotational_knock_to_nudge_indicator", ["y", "Y"])
    # def test_case_is_eligible_logs_a_message_if_rotational_knock_to_nudge_indicator_is_not_set_to_n_when_no_telephone_numbers_are_set(
    #     self,
    #     rotational_knock_to_nudge_indicator,
    #     valid_case_without_telephone_numbers,
    #     service: CaseFilterBase,
    #     caplog,
    # ):
    #     # arrange
    #     case = valid_case_without_telephone_numbers
    #     case.wave = service.wave_number
    #     case.rotational_knock_to_nudge_indicator = rotational_knock_to_nudge_indicator
    #
    #     # act && assert
    #     with caplog.at_level(logging.INFO):
    #         service.case_is_eligible(case)
    #     assert (
    #         "root",
    #         logging.INFO,
    #         f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a knock to knudge indicator value of '{rotational_knock_to_nudge_indicator}', not 'N'",
    #     ) in caplog.record_tuples


class TestIneligibleCasesWithATelephoneNumber:
    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [(110, 0), (210, 0), (0, 110), (310, 210)],
    )
    def test_case_is_eligible_returns_false_for_all_invalid_outcome_codes_when_telephone_number_1_is_set(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.contact_details.telephone_number_1 = "07656775679"
        case.outcome_code = outcome_code
        case.rotational_outcome_code = rotational_outcome_code

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_returns_false_if_field_case_is_not_set_to_y_when_a_telephone_number_is_set(
        self,
        field_case,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.field_case = field_case
        case.contact_details.telephone_number_1 = "07656775679"

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n_when_when_telephone_number_1_is_set(
        self,
        field_case,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
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

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_returns_false_if_field_case_is_not_set_to_y_when_telephone_number_2_is_set(
        self,
        field_case,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.field_case = field_case
        case.contact_details.telephone_number_2 = "07656775679"

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n_when_telephone_number_2_is_set(
        self,
        field_case,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.field_case = field_case
        case.contact_details.telephone_number_2 = "07656775679"

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of '{field_case}', not 'Y'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_returns_false_if_field_case_is_not_set_to_y_when_appointment_telephone_number_is_set(
        self,
        field_case,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.field_case = field_case
        case.contact_details.appointment_telephone_number = "07656775679"

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n_when_appointment_telephone_number_is_set(
        self,
        field_case,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.field_case = field_case
        case.contact_details.appointment_telephone_number = "07656775679"

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of '{field_case}', not 'Y'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize("test_input", ["Region 0", "Region 9", "Default"])
    def test_case_is_eligible_returns_false_if_field_region_is_not_in_range_when_A_telephone_numbers_is_set(
        self,
        test_input,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.contact_details.appointment_telephone_number = "07656775679"
        case.field_region = test_input

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_region", ["Region 0", "Region 9", "Default"])
    def test_case_is_eligible_logs_a_message_if_field_region_is_not_in_range_when_a_telephone_numbers_is_set(
        self,
        field_region,
        valid_case_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        case = valid_case_without_telephone_numbers
        case.wave = service.wave_number
        case.contact_details.appointment_telephone_number = "07656775679"
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
