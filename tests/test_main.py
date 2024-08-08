import flask

from unittest import mock

import pytest

from main import create_totalmobile_jobs_trigger


class TestCreateTotalmobileJobsTrigger:
    @mock.patch("factories.service_instance_factory.ServiceInstanceFactory.create_totalmobile_jobs_service")
    @mock.patch("cloud_functions.create_totalmobile_jobs_trigger.create_totalmobile_jobs_trigger")
    def test_create_totalmobile_jobs_trigger_logs_an_error_and_throws_an_exception_when_request_json_is_empty(
            self,
            _mock_create_totalmobile_jobs_trigger,
            _mock_create_totalmobile_jobs_service,
            caplog
    ):
        # act & assert
        with pytest.raises(Exception):
            create_totalmobile_jobs_trigger(None)

        assert "Could not parse JSON request: 'NoneType' object has no attribute 'get_json'" in caplog.messages


    @pytest.mark.parametrize(
        "survey_type",
        [
            None,
            0,
            "",
            "FFS",
        ],
    )
    @mock.patch("factories.service_instance_factory.ServiceInstanceFactory.create_totalmobile_jobs_service")
    @mock.patch("cloud_functions.create_totalmobile_jobs_trigger.create_totalmobile_jobs_trigger")
    def test_create_totalmobile_jobs_trigger_throws_an_exception_when_survey_type_not_in_lms_or_frs(
            self,
            _mock_create_totalmobile_jobs_trigger,
            _mock_create_totalmobile_jobs_service,
            survey_type,
            caplog
    ):
        # arrange
        mock_request = flask.Request.from_values(
            json={"survey_type": survey_type}
        )

        # act & assert
        with pytest.raises(Exception):
            create_totalmobile_jobs_trigger(mock_request)

        assert f"survey_type of '{survey_type}' is invalid" in caplog.messages


class TestCreateTotalmobileJobsTriggerLMS:
    mock_request = flask.Request.from_values(
        json={"survey_type": "LMS"}
    )

    @mock.patch("factories.service_instance_factory.ServiceInstanceFactory.create_totalmobile_jobs_service")
    @mock.patch("cloud_functions.create_totalmobile_jobs_trigger.create_totalmobile_jobs_trigger")
    def test_create_totalmobile_jobs_trigger_logs_the_entry_point_and_survey_type(
            self,
            _mock_create_totalmobile_jobs_trigger,
            _mock_create_totalmobile_jobs_service,
            caplog
    ):
        # act & assert
        create_totalmobile_jobs_trigger(self.mock_request)

        assert "BTS Create Jobs triggered for survey: 'LMS'" in caplog.messages

    @mock.patch("factories.service_instance_factory.ServiceInstanceFactory.create_totalmobile_jobs_service")
    @mock.patch("cloud_functions.create_totalmobile_jobs_trigger.create_totalmobile_jobs_trigger")
    def test_create_totalmobile_jobs_trigger_is_called_the_correct_number_of_times_with_the_correct_information(
            self,
            mock_create_totalmobile_jobs_trigger,
            mock_create_totalmobile_jobs_service
    ):
        # arrange
        mock_totalmobile_jobs_service_instance = mock_create_totalmobile_jobs_service.return_value

        # act
        create_totalmobile_jobs_trigger(self.mock_request)

        # assert
        assert mock_create_totalmobile_jobs_trigger.call_count == 1
        mock_create_totalmobile_jobs_trigger.assert_called_with(
            create_totalmobile_jobs_service=mock_totalmobile_jobs_service_instance
        )

    @mock.patch("factories.service_instance_factory.ServiceInstanceFactory.create_totalmobile_jobs_service")
    @mock.patch("cloud_functions.create_totalmobile_jobs_trigger.create_totalmobile_jobs_trigger")
    def test_create_totalmobile_jobs_service_is_called_the_correct_number_of_times_with_the_correct_information(
            self,
            _mock_create_totalmobile_jobs_trigger,
            mock_create_totalmobile_jobs_service
    ):
        # act
        create_totalmobile_jobs_trigger(self.mock_request)

        # assert
        assert mock_create_totalmobile_jobs_service.call_count == 1
        mock_create_totalmobile_jobs_service.assert_called_with("LMS")


class TestCreateTotalmobileJobsTriggerFRS:
    mock_request = flask.Request.from_values(
        json={"survey_type": "FRS"}
    )

    @mock.patch("factories.service_instance_factory.ServiceInstanceFactory.create_totalmobile_jobs_service")
    @mock.patch("cloud_functions.create_totalmobile_jobs_trigger.create_totalmobile_jobs_trigger")
    def test_create_totalmobile_jobs_trigger_logs_the_entry_point_and_survey_type(
            self,
            _mock_create_totalmobile_jobs_trigger,
            _mock_create_totalmobile_jobs_service,
            caplog
    ):
        # act & assert
        create_totalmobile_jobs_trigger(self.mock_request)

        assert "BTS Create Jobs triggered for survey: 'FRS'" in caplog.messages

    @mock.patch("factories.service_instance_factory.ServiceInstanceFactory.create_totalmobile_jobs_service")
    @mock.patch("cloud_functions.create_totalmobile_jobs_trigger.create_totalmobile_jobs_trigger")
    def test_create_totalmobile_jobs_trigger_is_called_the_correct_number_of_times_with_the_correct_information(
            self,
            mock_create_totalmobile_jobs_trigger,
            mock_create_totalmobile_jobs_service
    ):
        # arrange
        mock_totalmobile_jobs_service_instance = mock_create_totalmobile_jobs_service.return_value

        # act
        create_totalmobile_jobs_trigger(self.mock_request)

        # assert
        assert mock_create_totalmobile_jobs_trigger.call_count == 1
        mock_create_totalmobile_jobs_trigger.assert_called_with(
            create_totalmobile_jobs_service=mock_totalmobile_jobs_service_instance
        )

    @mock.patch("factories.service_instance_factory.ServiceInstanceFactory.create_totalmobile_jobs_service")
    @mock.patch("cloud_functions.create_totalmobile_jobs_trigger.create_totalmobile_jobs_trigger")
    def test_create_totalmobile_jobs_service_is_called_the_correct_number_of_times_with_the_correct_information(
            self,
            _mock_create_totalmobile_jobs_trigger,
            mock_create_totalmobile_jobs_service
    ):
        # act
        create_totalmobile_jobs_trigger(self.mock_request)

        # assert
        assert mock_create_totalmobile_jobs_service.call_count == 1
        mock_create_totalmobile_jobs_service.assert_called_with("FRS")
