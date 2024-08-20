import logging
from unittest.mock import Mock

import pytest

from services.case_filters.case_filter_base import CaseFilterBase
from services.lms_eligible_case_service import LMSEligibleCaseService
from tests.helpers.lms_case_model_helper import get_lms_populated_case_model


@pytest.fixture()
def mock_case_filter_wave_1() -> CaseFilterBase:
    return Mock(CaseFilterBase)


@pytest.fixture()
def mock_case_filter_wave_2() -> CaseFilterBase:
    return Mock(CaseFilterBase)


@pytest.fixture()
def service(mock_case_filter_wave_1) -> LMSEligibleCaseService:
    return LMSEligibleCaseService(wave_filters=[mock_case_filter_wave_1])


def test_get_eligible_cases_returns_expected_list_of_cases_with_one_filter(
    mock_case_filter_wave_1, service: LMSEligibleCaseService
):
    # arrange
    cases = [
        get_lms_populated_case_model(case_id="90001"),
        get_lms_populated_case_model(case_id="90002"),
        get_lms_populated_case_model(case_id="90003"),
        get_lms_populated_case_model(case_id="90004"),
    ]

    mock_case_filter_wave_1.case_is_eligible.side_effect = [True, False, True, True]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 3

    assert result == [
        get_lms_populated_case_model(case_id="90001"),
        get_lms_populated_case_model(case_id="90003"),
        get_lms_populated_case_model(case_id="90004"),
    ]


def test_get_eligible_cases_returns_expected_list_of_cases_with_two_filters(
    mock_case_filter_wave_1, mock_case_filter_wave_2
):
    # arrange
    cases = [
        get_lms_populated_case_model(case_id="90001"),
        get_lms_populated_case_model(case_id="90002"),
        get_lms_populated_case_model(case_id="90003"),
        get_lms_populated_case_model(case_id="90004"),
    ]

    mock_case_filter_wave_1.case_is_eligible.side_effect = [
        True,
        False,
        True,
        True,
    ]  # false will pass down to filter 2
    mock_case_filter_wave_2.case_is_eligible.side_effect = [True]

    service = LMSEligibleCaseService(
        wave_filters=[mock_case_filter_wave_1, mock_case_filter_wave_2]
    )

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 4

    assert result == [
        get_lms_populated_case_model(case_id="90001"),
        get_lms_populated_case_model(case_id="90002"),
        get_lms_populated_case_model(case_id="90003"),
        get_lms_populated_case_model(case_id="90004"),
    ]


def test_get_eligible_cases_logs_filtered_cases(
    mock_case_filter_wave_1, service: LMSEligibleCaseService, caplog
):
    # arrange
    cases = [
        get_lms_populated_case_model(case_id="90001"),
        get_lms_populated_case_model(case_id="90002"),
        get_lms_populated_case_model(case_id="90003"),
        get_lms_populated_case_model(case_id="90004"),
    ]

    mock_case_filter_wave_1.case_is_eligible.side_effect = [True, False, True, True]

    # act && assert
    with caplog.at_level(logging.INFO):
        service.get_eligible_cases(cases)
    assert (
        "root",
        logging.INFO,
        "Case '90001' in questionnaire 'LMS2101_AA1' was eligible and will be included",
    ) in caplog.record_tuples
    assert (
        "root",
        logging.INFO,
        "Case '90003' in questionnaire 'LMS2101_AA1' was eligible and will be included",
    ) in caplog.record_tuples
    assert (
        "root",
        logging.INFO,
        "Case '90004' in questionnaire 'LMS2101_AA1' was eligible and will be included",
    ) in caplog.record_tuples
