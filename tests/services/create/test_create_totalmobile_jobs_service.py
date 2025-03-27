import logging
from unittest.mock import Mock

import pytest

from models.create.blaise.blaise_lms_create_case_model import BlaiseLMSCreateCaseModel
from models.create.totalmobile.totalmobile_create_job_model import (
    TotalmobileCreateJobModel,
)
from services.create.create_totalmobile_jobs_service import CreateTotalmobileJobsService
from tests.helpers.blaise_case_model_helper import BlaiseCaseModelHelper


class TestLMSCreateTotalmobileJobsService:
    @pytest.fixture()
    def mock_totalmobile_service(self):
        return Mock()

    @pytest.fixture()
    def mock_questionnaire_service(self):
        return Mock()

    @pytest.fixture()
    def mock_cloud_task_service(self):
        return Mock()

    @pytest.fixture()
    def service(
        self,
        mock_totalmobile_service,
        mock_questionnaire_service,
        mock_cloud_task_service,
    ) -> CreateTotalmobileJobsService:
        return CreateTotalmobileJobsService(
            totalmobile_service=mock_totalmobile_service,
            questionnaire_service=mock_questionnaire_service,
            cloud_task_service=mock_cloud_task_service,
        )

    def test_check_questionnaire_release_date_logs_when_there_are_no_questionnaires_for_release(
        self,
        mock_questionnaire_service,
        service: CreateTotalmobileJobsService,
        caplog,
    ):
        # arrange
        mock_questionnaire_service.get_questionnaires_with_totalmobile_release_date_of_today.return_value = (
            []
        )
        mock_questionnaire_service.get_cases.return_value = []
        # act
        result = service.create_totalmobile_jobs()

        # assert
        assert result == "There are no questionnaires with a release date of today"
        with caplog.at_level(logging.INFO):
            service.create_totalmobile_jobs()
        assert (
            "root",
            logging.INFO,
            "There are no questionnaires with a release date of today",
        ) in caplog.record_tuples

    def test_create_totalmobile_jobs_for_eligible_questionnaire_cases(
        self,
        mock_questionnaire_service,
        mock_totalmobile_service,
        mock_cloud_task_service,
        service: CreateTotalmobileJobsService,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_lms_create_case_model(
            questionnaire_name="LMS2101_AA1", case_id="10010"
        )
        questionnaire_cases = [questionnaire_case]

        mock_questionnaire_service.get_eligible_cases.return_value = questionnaire_cases

        mock_questionnaire_service.get_cases.return_value = []

        totalmobile_create_job_model = TotalmobileCreateJobModel(
            questionnaire=questionnaire_name,
            world_id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
            case_id=questionnaire_cases[0].case_id,
            payload={"test-key": "test-value"},
        )

        mock_totalmobile_service.map_totalmobile_create_job_models.return_value = [
            totalmobile_create_job_model
        ]

        # act
        result = service.create_totalmobile_jobs_for_eligible_questionnaire_cases(
            questionnaire_name=questionnaire_name
        )

        # assert
        mock_questionnaire_service.get_eligible_cases.assert_called_with("LMS2101_AA1")

        mock_cloud_task_service.create_and_run_tasks.assert_called_once()
        kwargs = mock_cloud_task_service.create_and_run_tasks.call_args.kwargs
        assert kwargs["cloud_function"] == "bts-create-totalmobile-jobs-processor"
        assert len(kwargs["task_request_models"]) == 1
        task_request_model = kwargs["task_request_models"][0]
        assert task_request_model.task_name.startswith("LMS")
        assert (
            task_request_model.task_body == totalmobile_create_job_model.json().encode()
        )
        assert result == "Done"

    def test_create_cloud_tasks_when_no_eligible_cases(
        self,
        mock_questionnaire_service,
        mock_cloud_task_service,
        service: CreateTotalmobileJobsService,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"

        mock_questionnaire_service.get_eligible_cases.return_value = []

        # act
        result = service.create_totalmobile_jobs_for_eligible_questionnaire_cases(
            questionnaire_name=questionnaire_name
        )

        # assert
        mock_cloud_task_service.create_and_run_tasks.assert_not_called()
        assert (
            result
            == "Exiting as no eligible cases to send for questionnaire LMS2101_AA1"
        )
