import logging
from unittest.mock import Mock

import pytest

from services.blaise_case_outcome_service import BlaiseCaseOutcomeService
from tests.helpers import get_blaise_case_model_helper


@pytest.fixture()
def mock_blaise_service():
    return Mock()


@pytest.fixture()
def service(mock_blaise_service) -> BlaiseCaseOutcomeService:
    return BlaiseCaseOutcomeService(blaise_service=mock_blaise_service)


def test_get_case_outcomes_for_questionnaire_calls_the_blaise_service_with_the_correct_parameters(
    mock_blaise_service, service
):
    questionnaire_name = "LMS2101_AA1"
    questionnaire_cases = [get_blaise_case_model_helper.get_populated_case_model()]

    mock_blaise_service.get_cases.return_value = questionnaire_cases

    # act
    service.get_case_outcomes_for_questionnaire(questionnaire_name)

    # assert
    mock_blaise_service.get_cases.assert_called_with(questionnaire_name)


def test_get_case_outcomes_for_questionnaire_returns_the_expected_dictionary(
    mock_blaise_service, service
):
    questionnaire_name = "LMS2101_AA1"
    questionnaire_cases = [
        get_blaise_case_model_helper.get_populated_case_model(
            questionnaire_name=questionnaire_name, case_id="12002", outcome_code=110
        ),
        get_blaise_case_model_helper.get_populated_case_model(
            questionnaire_name=questionnaire_name, case_id="14002", outcome_code=210
        ),
    ]

    mock_blaise_service.get_cases.return_value = questionnaire_cases

    # act
    result = service.get_case_outcomes_for_questionnaire(questionnaire_name)

    # assert
    assert len(result) == 2
    assert result == {"12002": 110, "14002": 210}


def test_get_case_outcomes_for_questionnaire_only_gets_the_questionnaire_data_once(
    mock_blaise_service, service
):
    questionnaire_name = "LMS2101_AA1"
    questionnaire_cases = [
        get_blaise_case_model_helper.get_populated_case_model(
            questionnaire_name=questionnaire_name, case_id="12002", outcome_code=110
        ),
        get_blaise_case_model_helper.get_populated_case_model(
            questionnaire_name=questionnaire_name, case_id="14002", outcome_code=210
        ),
    ]

    mock_blaise_service.get_cases.return_value = questionnaire_cases

    # act
    service.get_case_outcomes_for_questionnaire(questionnaire_name)
    service.get_case_outcomes_for_questionnaire(questionnaire_name)
    service.get_case_outcomes_for_questionnaire(questionnaire_name)

    # assert
    mock_blaise_service.get_cases.assert_called_once()


def test_get_case_outcomes_for_questionnaire_logs_error_if_blaise_errors(
    mock_blaise_service, service, caplog
):
    questionnaire_name = "LMS2101_AA1"
    mock_blaise_service.get_cases.side_effect = Exception()

    # act && assert
    with caplog.at_level(logging.ERROR):
        service.get_case_outcomes_for_questionnaire(questionnaire_name)
    assert (
        "root",
        logging.ERROR,
        f"Unable to retrieve cases from Blaise for questionnaire {questionnaire_name}",
    ) in caplog.record_tuples


def test_get_case_outcomes_for_questionnaire_does_not_store_empty_dict_if_blaise_errors(
    mock_blaise_service, service
):
    questionnaire_name = "LMS2101_AA1"
    mock_blaise_service.get_cases.side_effect = Exception()

    # act
    result = service.get_case_outcomes_for_questionnaire(questionnaire_name)

    # assert
    assert len(result) == 0


def test_get_case_outcomes_for_questionnaire_does_stores_data_second_time_if_blaise_errors_first_time_only(
    mock_blaise_service, service
):
    questionnaire_name = "LMS2101_AA1"
    questionnaire_cases = [
        get_blaise_case_model_helper.get_populated_case_model(
            questionnaire_name=questionnaire_name, case_id="12002", outcome_code=110
        ),
        get_blaise_case_model_helper.get_populated_case_model(
            questionnaire_name=questionnaire_name, case_id="14002", outcome_code=210
        ),
    ]

    mock_blaise_service.get_cases.side_effect = [Exception(), questionnaire_cases]

    # act
    service.get_case_outcomes_for_questionnaire(questionnaire_name)
    result = service.get_case_outcomes_for_questionnaire(questionnaire_name)

    # assert
    assert len(result) == 2
    assert result == {"12002": 110, "14002": 210}
