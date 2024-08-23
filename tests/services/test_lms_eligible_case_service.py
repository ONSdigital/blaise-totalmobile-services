import logging
from unittest.mock import Mock

import pytest

from models.create.blaise.blaiise_lms_case_model import BlaiseLMSCaseModel
from services.create.eligibility.case_filters.case_filter_base import CaseFilterBase
from services.create.eligibility.lms_eligible_case_service import LMSEligibleCaseService


def get_case(
    case_id: str,
) -> BlaiseLMSCaseModel:
    return BlaiseLMSCaseModel(
        "LMS2101_AA1",
        {
            "qiD.Serial_Number": case_id,
            "qDataBag.FieldRegion": "Region 1",
            "hOut": "0",
            "qDataBag.TelNo": "07900990901",
            "qDataBag.TelNo2": "07900990902",
            "telNoAppt": "07900990903",
            "qDataBag.FieldTeam": "B-Team",
            "dataModelName": "LM2007",
            "qDataBag.Prem1": "12 Blaise Street",
            "qDataBag.Prem2": "Blaise Hill",
            "qDataBag.Prem3": "Blaiseville",
            "qDataBag.District": "Gwent",
            "qDataBag.PostTown": "Newport",
            "qDataBag.PostCode": "CM1ASD",
            "qDataBag.UPRN_Latitude": "10020202",
            "qDataBag.UPRN_Longitude": "34949494",
            "qDataBag.WaveComDTE": "31-01-2023",
            "qDataBag.priority": "1",
        },
        uac_chunks=None,
    )


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
