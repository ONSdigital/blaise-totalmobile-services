import logging
from typing import Dict

import pytest

from enums.blaise_fields import BlaiseFields
from models.common.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from models.create.blaise.blaiise_lms_create_case_model import BlaiseLMSCreateCaseModel
from services.create.questionnaires.eligibility.case_filters.case_filter_base import (
    CaseFilterBase,
)
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_4 import (
    CaseFilterWave4,
)
from services.create.questionnaires.eligibility.case_filters.case_filter_wave_5 import (
    CaseFilterWave5,
)


@pytest.fixture()
def valid_case_data() -> Dict[str, str]:
    return {
        BlaiseFields.case_id: "90001",
        BlaiseFields.wave: "1",
        BlaiseFields.field_case: "Y",
        BlaiseFields.outcome_code: "0",
        BlaiseFields.telephone_number_1: "",
        BlaiseFields.telephone_number_2: "",
        BlaiseFields.appointment_telephone_number: "",
        BlaiseFields.field_region: "Region 1",
    }


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


class TestEligibleCases:
    def test_case_is_eligible_returns_true_where_criteria_for_wave_4_and_5_are_met(
        self,
        valid_case_data,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data[BlaiseFields.wave] = str(service.wave_number)
        case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_case_data, None)

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True


class TestIneligibleCases:
    @pytest.mark.parametrize("outcome_code", ["110", "210", "310"])
    def test_case_is_eligible_returns_false_where_criteria_for_wave_4_and_5_are_not_met(
        self,
        outcome_code,
        valid_case_data,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data[BlaiseFields.wave] = str(service.wave_number)
        valid_case_data[BlaiseFields.outcome_code] = outcome_code
        case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_case_data, None)

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("outcome_code", ["110", "210", "310"])
    def test_case_is_eligible_logs_a_message_if_outcome_code_is_not_0(
        self,
        outcome_code,
        valid_case_data,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data[BlaiseFields.wave] = str(service.wave_number)
        valid_case_data[BlaiseFields.outcome_code] = outcome_code
        case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_case_data, None)

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{outcome_code}' outside of the range '[0]' set for the field 'outcome_code'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize("wave_number", ["0", "1", "2", "3"])
    def test_case_is_eligible_returns_false_if_the_case_is_not_wave_2_or_3(
        self, valid_case_data, service: CaseFilterBase, wave_number
    ):
        # arrange

        valid_case_data[BlaiseFields.wave] = wave_number
        case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_case_data, None)
        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_region", ["Region 0", "Region 9", "Default"])
    def test_case_is_eligible_returns_false_if_field_region_is_not_in_range(
        self,
        field_region,
        valid_case_data,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data[BlaiseFields.wave] = str(service.wave_number)
        valid_case_data[BlaiseFields.field_region] = field_region
        case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_case_data, None)

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_region", ["Region 0", "Region 9", "Default"])
    def test_case_is_eligible_logs_a_message_if_field_region_is_not_in_range(
        self,
        field_region,
        valid_case_data,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data[BlaiseFields] = str(service.wave_number)
        valid_case_data[BlaiseFields.field_region] = field_region
        case = BlaiseLMSCreateCaseModel("LMS2101_AA1", valid_case_data, None)

        value_range = TotalmobileWorldModel.get_available_regions()

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{field_region}' outside of the range '{value_range}' set for the field 'field_region'",
        ) in caplog.record_tuples
