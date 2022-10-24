import logging

import pytest

from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from services.case_filters.case_filter_base import CaseFilterBase
from services.case_filters.case_filter_wave_4 import CaseFilterWave4
from services.case_filters.case_filter_wave_5 import CaseFilterWave5
from tests.helpers.get_blaise_case_model_helper import get_populated_case_model


@pytest.fixture()
def valid_case() -> BlaiseCaseInformationModel:
    return get_populated_case_model(
        case_id="90001",
        outcome_code=0,
    )


@pytest.fixture(scope="module", params=[CaseFilterWave4(), CaseFilterWave5()])
def service(request) -> CaseFilterBase:
    return request.param


def test_valid_outcome_codes_has_not_changed_for_wave_4():
    # arrange
    service = CaseFilterWave4()

    # act
    outcome_codes = service.valid_outcome_codes

    # assert
    assert outcome_codes == [0]


def test_valid_outcome_codes_has_not_changed_for_wave_5():
    # arrange
    service = CaseFilterWave5()

    # act
    outcome_codes = service.valid_outcome_codes

    # assert
    assert outcome_codes == [0]


class TestWave4And5Filters:
    def test_case_is_eligible_returns_true_where_criteria_for_wave_4_and_5_are_met(
            self,
            valid_case,
            service: CaseFilterBase,
    ):
        # arrange
        case = valid_case
        case.wave = service.wave_number

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    def test_case_is_eligible_returns_false_where_criteria_for_wave_4_and_5_are_not_met(
            self,
            valid_case,
            service: CaseFilterBase,
    ):
        # arrange
        case = valid_case
        case.wave = service.wave_number
        case.outcome_code = 310

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    def test_case_is_eligible_logs_a_message_if_outcome_code_is_not_0(
            self,
            valid_case,
            service: CaseFilterBase,
            caplog,
    ):
        # arrange
        case = valid_case
        case.wave = service.wave_number
        case.outcome_code = 310

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
                   "root",
                   logging.INFO,
                   f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '310' outside of the range '[0]' set for the field 'outcome_code'",
               ) in caplog.record_tuples

    @pytest.mark.parametrize("wave_number", [0, 1, 2, 3])
    def test_case_is_eligible_returns_false_if_the_case_is_not_wave_2_or_3(
            self, valid_case, service: CaseFilterBase, wave_number
    ):
        # arrange
        case = valid_case
        case.wave = wave_number

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("test_input", ["Region 0", "Region 9", "Default"])
    def test_case_is_eligible_returns_false_if_field_region_is_not_in_range(
            self,
            test_input,
            valid_case,
            service: CaseFilterBase,
    ):
        # arrange
        case = valid_case
        case.wave = service.wave_number
        case.field_region = test_input

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_region", ["Region 0", "Region 9", "Default"])
    def test_case_is_eligible_logs_a_message_if_field_region_is_not_in_range(
            self,
            field_region,
            valid_case,
            service: CaseFilterBase,
            caplog,
    ):
        # arrange
        case = valid_case
        case.wave = service.wave_number
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
