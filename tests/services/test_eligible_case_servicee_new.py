import logging

import pytest

from unittest.mock import create_autospec

from services.case_filters.case_filter_base import CaseFilterBase
from services.eligible_case_service import EligibleCaseService
from tests.helpers.get_blaise_case_model_helper import get_populated_case_model


@pytest.fixture()
def mock_case_filter():
    return create_autospec(CaseFilterBase)


@pytest.fixture()
def service(mock_case_filter) -> EligibleCaseService:
    return EligibleCaseService(wave_filters=[mock_case_filter])


def test_get_eligible_cases_returns_expected_list_of_cases(
    mock_case_filter: CaseFilterBase,
    service: EligibleCaseService,
):
    # arrange
    cases = [
        get_populated_case_model(case_id="90001"),
        get_populated_case_model(case_id="90002"),
        get_populated_case_model(case_id="90003"),
        get_populated_case_model(case_id="90004")
    ]

    mock_case_filter.case_is_eligible.side_effect = [True, False, True, True]

    # act
    result = service.get_eligible_cases(cases)

    # assert
    assert len(result) == 3

    assert result == [
        get_populated_case_model(case_id="90001"),
        get_populated_case_model(case_id="90003"),
        get_populated_case_model(case_id="90004")
    ]


def test_get_eligible_cases_logs_filtered_cases(
    mock_case_filter: CaseFilterBase,
    service: EligibleCaseService,
    caplog
):
    # arrange
    cases = [
        get_populated_case_model(case_id="90001"),
        get_populated_case_model(case_id="90002"),
        get_populated_case_model(case_id="90003"),
        get_populated_case_model(case_id="90004")
    ]

    mock_case_filter.case_is_eligible.side_effect = [True, False, True, True]

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





