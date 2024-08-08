import flask

from unittest import mock

from main import create_totalmobile_jobs_trigger


class TestMainLMS:
    mock_request = flask.Request.from_values(
        json={"survey_type": "LMS"}
    )

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


class TestMainFRS:
    mock_request = flask.Request.from_values(
        json={"survey_type": "FRS"}
    )

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
