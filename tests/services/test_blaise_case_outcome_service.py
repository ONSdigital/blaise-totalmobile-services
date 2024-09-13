import logging
from unittest.mock import Mock

import pytest

from enums.blaise_fields import BlaiseFields
from models.delete.blaise_delete_case_model import BlaiseDeleteCase
from services.delete.blaise_case_outcome_service import BlaiseCaseOutcomeService


class TestGetCaseOutcomesForLMS:
    @pytest.fixture()
    def mock_blaise_service(self):
        return Mock()

    @pytest.fixture()
    def service(self, mock_blaise_service) -> BlaiseCaseOutcomeService:
        return BlaiseCaseOutcomeService(blaise_service=mock_blaise_service)

    def test_get_case_outcomes_for_lms_questionnaire_calls_the_blaise_service_with_the_correct_parameters(
        self, mock_blaise_service, service
    ):
        questionnaire_name = "LMS2101_AA1"
        case_data = [
            {
                BlaiseFields.case_id: "12002",
                BlaiseFields.outcome_code: "110",
            },
            {
                BlaiseFields.case_id: "14002",
                BlaiseFields.outcome_code: "210",
            },
        ]
        mock_blaise_service.get_cases.return_value = case_data
        required_fields = BlaiseDeleteCase.required_fields()

        # act
        service.get_case_outcomes_for_questionnaire(questionnaire_name)

        # assert
        mock_blaise_service.get_cases.assert_called_with(
            questionnaire_name, required_fields
        )

    def test_get_case_outcomes_for_questionnaire_returns_the_expected_dictionary(
        self, mock_blaise_service, service
    ):
        questionnaire_name = "LMS2101_AA1"
        case_data = [
            {
                BlaiseFields.case_id: "12002",
                BlaiseFields.outcome_code: "110",
            },
            {
                BlaiseFields.case_id: "14002",
                BlaiseFields.outcome_code: "210",
            },
        ]
        mock_blaise_service.get_cases.return_value = case_data

        # act
        result = service.get_case_outcomes_for_questionnaire(questionnaire_name)

        # assert
        assert len(result) == 2
        assert result == {"12002": 110, "14002": 210}

    def test_get_case_outcomes_for_questionnaire_only_gets_the_questionnaire_data_once(
        self, mock_blaise_service, service
    ):
        questionnaire_name = "LMS2101_AA1"
        case_data = [
            {
                BlaiseFields.case_id: "12002",
                BlaiseFields.outcome_code: "110",
            },
            {
                BlaiseFields.case_id: "14002",
                BlaiseFields.outcome_code: "210",
            },
        ]
        mock_blaise_service.get_cases.return_value = case_data

        # act
        service.get_case_outcomes_for_questionnaire(questionnaire_name)
        service.get_case_outcomes_for_questionnaire(questionnaire_name)
        service.get_case_outcomes_for_questionnaire(questionnaire_name)

        # assert
        mock_blaise_service.get_cases.assert_called_once()

    def test_get_case_outcomes_for_questionnaire_logs_error_if_blaise_errors(
        self, mock_blaise_service, service, caplog
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
        self, mock_blaise_service, service
    ):
        questionnaire_name = "LMS2101_AA1"
        mock_blaise_service.get_cases.side_effect = Exception()

        # act
        result = service.get_case_outcomes_for_questionnaire(questionnaire_name)

        # assert
        assert len(result) == 0

    def test_get_case_outcomes_for_questionnaire_does_stores_data_second_time_if_blaise_errors_first_time_only(
        self, mock_blaise_service, service
    ):
        questionnaire_name = "LMS2101_AA1"
        case_data = [
            {
                BlaiseFields.case_id: "12002",
                BlaiseFields.outcome_code: "110",
            },
            {
                BlaiseFields.case_id: "14002",
                BlaiseFields.outcome_code: "210",
            },
        ]
        mock_blaise_service.get_cases.return_value = case_data

        mock_blaise_service.get_cases.side_effect = [Exception(), case_data]

        # act
        service.get_case_outcomes_for_questionnaire(questionnaire_name)
        result = service.get_case_outcomes_for_questionnaire(questionnaire_name)

        # assert
        assert len(result) == 2
        assert result == {"12002": 110, "14002": 210}
