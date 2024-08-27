import logging
from typing import Dict

import pytest

from models.common.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from models.create.blaise.blaiise_lms_create_case_model import BlaiseLMSCreateCaseModel
from services.create.eligibility.case_filters.case_filter_base import CaseFilterBase
from services.create.eligibility.case_filters.case_filter_wave_2 import CaseFilterWave2
from services.create.eligibility.case_filters.case_filter_wave_3 import CaseFilterWave3


@pytest.fixture()
def valid_case_data_without_telephone_numbers() -> Dict[str, str]:
    return {
        "qiD.Serial_Number": "90001",
        "qDataBag.Wave": "1",
        "qDataBag.FieldCase": "Y",
        "hOut": "310",
        "qRotate.RHOut": "0",
        "qDataBag.TelNo": "",
        "qDataBag.TelNo2": "",
        "telNoAppt": "",
        "qDataBag.FieldRegion": "Region 1",
        "qRotate.RDMktnIND": "",
    }


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
    assert outcome_codes == [0, 310, 320]
    assert valid_rotational_outcome_codes == [0, 310, 320]


def test_valid_outcome_codes_has_not_changed_for_wave_3():
    # arrange
    service = CaseFilterWave3()

    # act
    outcome_codes = service.valid_outcome_codes
    valid_rotational_outcome_codes = service.valid_rotational_outcome_codes

    # assert
    assert outcome_codes == [0, 310, 320]
    assert valid_rotational_outcome_codes == [0, 310, 320]


class TestEligibleCasesWithoutTelephoneNumbers:
    @pytest.mark.parametrize("knock_to_nudge_indicator", ["", None])
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_knock_to_nudge_indicator_without_telephone_number_1_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["", None])
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_knock_to_nudge_indicator_without_telephone_number_2_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["", None])
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_knock_to_nudge_indicator_without_appointment_telephone_number_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [
            (0, 0),
            (0, 310),
            (0, 320),
            (310, 0),
            (310, 310),
            (310, 320),
            (320, 0),
            (320, 310),
            (320, 320),
        ],
    )
    def test_case_is_eligible_returns_true_where_criteria_without_telephone_is_met_for_all_outcome_codes(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange

        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["hOut"] = str(outcome_code)
        valid_case_data_without_telephone_numbers["qRotate.RHOut"] = str(
            rotational_outcome_code
        )
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True


class TestEligibleCasesWithATelephoneNumber:
    @pytest.mark.parametrize("knock_to_nudge_indicator", ["", None])
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_knock_to_nudge_indicator_with_telephone_number_1_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        valid_case_data_without_telephone_numbers["qDataBag.TelNo"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["", None])
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_knock_to_nudge_indicator_with_telephone_number_2_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        valid_case_data_without_telephone_numbers["qDataBag.TelNo2"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["", None])
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_knock_to_nudge_indicator_with_appointment_telephone_number_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        valid_case_data_without_telephone_numbers["telNoAppt"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [
            (0, 0),
            (0, 310),
            (0, 320),
            (310, 0),
            (310, 310),
            (310, 320),
            (320, 0),
            (320, 310),
            (320, 320),
        ],
    )
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_all_outcome_codes_with_telephone_number_1_set(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["hOut"] = str(outcome_code)
        valid_case_data_without_telephone_numbers["qRotate.RHOut"] = str(
            rotational_outcome_code
        )
        valid_case_data_without_telephone_numbers["qDataBag.TelNo"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [
            (0, 0),
            (0, 310),
            (0, 320),
            (310, 0),
            (310, 310),
            (310, 320),
            (320, 0),
            (320, 310),
            (320, 320),
        ],
    )
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_all_outcome_codes_with_telephone_number_2_set(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["hOut"] = str(outcome_code)
        valid_case_data_without_telephone_numbers["qRotate.RHOut"] = str(
            rotational_outcome_code
        )
        valid_case_data_without_telephone_numbers["qDataBag.TelNo2"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True

    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [
            (0, 0),
            (0, 310),
            (0, 320),
            (310, 0),
            (310, 310),
            (310, 320),
            (320, 0),
            (320, 310),
            (320, 320),
        ],
    )
    def test_case_is_eligible_returns_true_where_criteria_is_met_for_all_outcome_codes_with_appointment_telephone_number_set(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["hOut"] = str(outcome_code)
        valid_case_data_without_telephone_numbers["qRotate.RHOut"] = str(
            rotational_outcome_code
        )
        valid_case_data_without_telephone_numbers["telNoAppt"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is True


class TestCaseIsInCorrectWave:
    @pytest.mark.parametrize("wave_number", ["0", "1", "4", "5"])
    def test_case_is_eligible_returns_false_if_the_case_is_not_wave_2_or_3(
        self,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        wave_number,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = wave_number
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False


class TestIneligibleCasesWithoutTelephoneNumbers:
    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_returns_false_for_invalid_knock_to_nudge_indicator_without_telephone_number_1_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_logs_a_message_if_knock_to_nudge_indicator_is_set_to_y_when_telephone_number_1_is_not_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a knock to knudge indicator value of 'Y', not 'N'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_returns_false_for_invalid_knock_to_nudge_indicator_without_telephone_number_2_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_logs_a_message_if_knock_to_nudge_indicator_is_set_to_y_when_telephone_number_2_is_not_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a knock to knudge indicator value of 'Y', not 'N'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_returns_false_for_invalid_knock_to_nudge_indicator_without_appointment_telephone_number_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_logs_a_message_if_knock_to_nudge_indicator_is_set_to_y_when_appointment_telephone_number_is_not_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a knock to knudge indicator value of 'Y', not 'N'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [(110, 0), (210, 0), (0, 110), (310, 210)],
    )
    def test_case_is_eligible_returns_false_for_all_invalid_outcome_codes_when_no_telephone_numbers_are_set(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["hOut"] = str(outcome_code)
        valid_case_data_without_telephone_numbers["qRotate.RHOut"] = str(
            rotational_outcome_code
        )
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize(
        "outcome_code",
        [110, 210],
    )
    def test_case_is_eligible_logs_a_message_for_all_invalid_outcome_codes_when_no_telephone_numbers_are_set(
        self,
        outcome_code,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["hOut"] = str(outcome_code)
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{outcome_code}' outside of the range '[0, 310, 320]' set for the field 'outcome_code'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize(
        "rotational_outcome_code",
        [110, 210],
    )
    def test_case_is_eligible_logs_a_message_for_all_invalid_rotational_outcome_codes_when_no_telephone_numbers_are_set(
        self,
        rotational_outcome_code,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qRotate.RHOut"] = str(
            rotational_outcome_code
        )
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{rotational_outcome_code}' outside of the range '[0, 310, 320]' set for the field 'rotational_outcome_code'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_returns_false_if_field_case_is_not_set_to_y_when_no_telephone_numbers_are_set(
        self,
        field_case,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qDataBag.FieldCase"] = field_case
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n_when_no_telephone_numbers_are_set(
        self,
        field_case,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qDataBag.FieldCase"] = field_case
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of '{field_case}', not 'Y'",
        ) in caplog.record_tuples


class TestIneligibleCasesWithATelephoneNumber:
    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_returns_false_for_invalid_knock_to_nudge_indicator_with_telephone_number_1_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        valid_case_data_without_telephone_numbers["qDataBag.TelNo"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_logs_a_message_if_knock_to_nudge_indicator_is_set_to_y_when_telephone_number_1_is_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        valid_case_data_without_telephone_numbers["qDataBag.TelNo"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a knock to knudge indicator value of 'Y', not 'N'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_returns_false_for_invalid_knock_to_nudge_indicator_with_telephone_number_2_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        valid_case_data_without_telephone_numbers["qDataBag.TelNo2"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_logs_a_message_if_knock_to_nudge_indicator_is_set_to_y_when_telephone_number_2_is_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        valid_case_data_without_telephone_numbers["qDataBag.TelNo2"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a knock to knudge indicator value of 'Y', not 'N'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_returns_false_for_invalid_knock_to_nudge_indicator_with_appointment_telephone_number_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        valid_case_data_without_telephone_numbers["telNoAppt"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("knock_to_nudge_indicator", ["1"])
    def test_case_is_eligible_logs_a_message_if_knock_to_nudge_indicator_is_set_to_y_when_appointment_telephone_number_is_set(
        self,
        knock_to_nudge_indicator,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers[
            "qRotate.RDMktnIND"
        ] = knock_to_nudge_indicator
        valid_case_data_without_telephone_numbers["telNoAppt"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a knock to knudge indicator value of 'Y', not 'N'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize(
        "outcome_code, rotational_outcome_code",
        [(110, 0), (210, 0), (0, 110), (310, 210)],
    )
    def test_case_is_eligible_returns_false_for_all_invalid_outcome_codes_when_telephone_numbers_are_set(
        self,
        outcome_code,
        rotational_outcome_code,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["hOut"] = str(outcome_code)
        valid_case_data_without_telephone_numbers["qRotate.RHOut"] = str(
            rotational_outcome_code
        )
        valid_case_data_without_telephone_numbers["qDataBag.TelNo"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize(
        "outcome_code",
        [110, 210],
    )
    def test_case_is_eligible_logs_a_message_for_all_invalid_outcome_codes_when_telephone_numbers_are_set(
        self,
        outcome_code,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["hOut"] = str(outcome_code)
        valid_case_data_without_telephone_numbers["qDataBag.TelNo"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{outcome_code}' outside of the range '[0, 310, 320]' set for the field 'outcome_code'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize(
        "rotational_outcome_code",
        [110, 210],
    )
    def test_case_is_eligible_logs_a_message_for_all_invalid_rotational_outcome_codes_when_telephone_numbers_are_set(
        self,
        rotational_outcome_code,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qRotate.RHOut"] = str(
            rotational_outcome_code
        )
        valid_case_data_without_telephone_numbers["qDataBag.TelNo"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{rotational_outcome_code}' outside of the range '[0, 310, 320]' set for the field 'rotational_outcome_code'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_returns_false_if_field_case_is_not_set_to_y_when_a_telephone_number_is_set(
        self,
        field_case,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qDataBag.FieldCase"] = field_case
        valid_case_data_without_telephone_numbers["qDataBag.TelNo"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n_when_when_atelephone_number1_is_set(
        self,
        field_case,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qDataBag.FieldCase"] = field_case
        valid_case_data_without_telephone_numbers["qDataBag.TelNo"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

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
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qDataBag.FieldCase"] = field_case
        valid_case_data_without_telephone_numbers["qDataBag.TelNo2"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n_when_telephone_number_2_is_set(
        self,
        field_case,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qDataBag.FieldCase"] = field_case
        valid_case_data_without_telephone_numbers["qDataBag.TelNo2"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

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
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qDataBag.FieldCase"] = field_case
        valid_case_data_without_telephone_numbers["telNoAppt"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_case", ["", "N", "n"])
    def test_case_is_eligible_logs_a_message_if_field_case_is_set_to_n_when_appointment_telephone_number_is_set(
        self,
        field_case,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qDataBag.FieldCase"] = field_case
        valid_case_data_without_telephone_numbers["telNoAppt"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a field case value of '{field_case}', not 'Y'",
        ) in caplog.record_tuples

    @pytest.mark.parametrize("field_region", ["Region 0", "Region 9", "Default"])
    def test_case_is_eligible_returns_false_if_field_region_is_not_in_range_when_telephone_numbers_is_set(
        self,
        field_region,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qDataBag.FieldRegion"] = field_region
        valid_case_data_without_telephone_numbers["telNoAppt"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        # act
        result = service.case_is_eligible(case)

        # assert
        assert result is False

    @pytest.mark.parametrize("field_region", ["Region 0", "Region 9", "Default"])
    def test_case_is_eligible_logs_a_message_if_field_region_is_not_in_range_when_a_telephone_number_is_set(
        self,
        field_region,
        valid_case_data_without_telephone_numbers,
        service: CaseFilterBase,
        caplog,
    ):
        # arrange
        valid_case_data_without_telephone_numbers["qDataBag.Wave"] = str(
            service.wave_number
        )
        valid_case_data_without_telephone_numbers["qDataBag.FieldRegion"] = field_region
        valid_case_data_without_telephone_numbers["telNoAppt"] = "07656775679"
        case = BlaiseLMSCreateCaseModel(
            "LMS2101_AA1", valid_case_data_without_telephone_numbers, None
        )

        value_range = TotalmobileWorldModel.get_available_regions()

        # act && assert
        with caplog.at_level(logging.INFO):
            service.case_is_eligible(case)
        assert (
            "root",
            logging.INFO,
            f"Case '90001' in questionnaire 'LMS2101_AA1' was not eligible to be sent to Totalmobile as it has a value '{field_region}' outside of the range '{value_range}' set for the field 'field_region'",
        ) in caplog.record_tuples
