import logging
from unittest.mock import Mock

import pytest

from models.create.blaise.blaiise_lms_create_case_model import BlaiseLMSCreateCaseModel
from services.create.eligibility.case_filters.case_filter_base import CaseFilterBase
from services.create.eligibility.lms_eligible_case_service import LMSEligibleCaseService
from tests.helpers.blaise_case_model_helper import BlaiseCaseModelHelper


def get_case(
    case_id: str,
) -> BlaiseLMSCreateCaseModel:
    return BlaiseCaseModelHelper.get_populated_lms_create_case_model(case_id=case_id)


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
        get_case(case_id="90001"),
        get_case(case_id="90002"),
        get_case(case_id="90003"),
        get_case(case_id="90004"),
    ]

    mock_case_filter_wave_1.case_is_eligible.side_effect = [True, False, True, True]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 3

    assert result[0].case_id == "90001"
    assert result[1].case_id == "90003"
    assert result[2].case_id == "90004"


def test_get_eligible_cases_returns_expected_list_of_cases_with_two_filters(
    mock_case_filter_wave_1, mock_case_filter_wave_2
):
    # arrange
    cases = [
        get_case(case_id="90001"),
        get_case(case_id="90002"),
        get_case(case_id="90003"),
        get_case(case_id="90004"),
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

    assert result[0].case_id == "90001"
    assert result[1].case_id == "90002"
    assert result[2].case_id == "90003"
    assert result[3].case_id == "90004"


def test_get_eligible_cases_logs_filtered_cases(
    mock_case_filter_wave_1, service: LMSEligibleCaseService, caplog
):
    # arrange
    cases = [
        get_case(case_id="90001"),
        get_case(case_id="90002"),
        get_case(case_id="90003"),
        get_case(case_id="90004"),
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
