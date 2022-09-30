import logging
from datetime import datetime
from unittest import mock
from unittest.mock import Mock

import pytest

from appconfig import Config
from services.datastore_service import DatastoreService
from services.questionnaire_service import QuestionnaireService
from tests.helpers import config_helper, get_blaise_case_model_helper
from tests.helpers.datastore_helper import DatastoreHelper


@pytest.fixture()
def mock_blaise_service():
    return Mock()


@pytest.fixture()
def mock_eligible_case_service():
    return Mock()


@pytest.fixture()
def config() -> Config:
    return config_helper.get_default_config()


@pytest.fixture()
def service(
    config, mock_blaise_service, mock_eligible_case_service
) -> QuestionnaireService:
    return QuestionnaireService(
        config,
        blaise_service=mock_blaise_service,
        eligible_case_service=mock_eligible_case_service,
    )


@mock.patch.object(QuestionnaireService, "get_cases")
def test_get_eligible_cases_calls_the_services_with_the_correct_parameters(
    mock_get_cases,
    mock_eligible_case_service,
    service: QuestionnaireService,
):
    questionnaire_cases = [
        get_blaise_case_model_helper.get_populated_case_model(),  # eligible
        get_blaise_case_model_helper.get_populated_case_model(),  # not eligible
    ]

    eligible_cases = [questionnaire_cases[0]]

    mock_get_cases.return_value = questionnaire_cases
    mock_eligible_case_service.get_eligible_cases.return_value = eligible_cases

    questionnaire_name = "LMS2101_AA1"

    # act
    service.get_eligible_cases(questionnaire_name)

    # assert
    mock_get_cases.assert_called_with(questionnaire_name)
    mock_eligible_case_service.get_eligible_cases.assert_called_with(
        questionnaire_cases
    )


@mock.patch.object(QuestionnaireService, "get_cases")
def test_get_eligible_cases_returns_the_list_of_eligible_cases_from_the_eligible_case_service(
    mock_get_cases,
    mock_eligible_case_service,
    service: QuestionnaireService,
):
    questionnaire_cases = [
        get_blaise_case_model_helper.get_populated_case_model(),  # eligible
        get_blaise_case_model_helper.get_populated_case_model(),  # not eligible
    ]

    eligible_cases = [questionnaire_cases[0]]

    mock_get_cases.return_value = questionnaire_cases
    mock_eligible_case_service.get_eligible_cases.return_value = eligible_cases

    questionnaire_name = "LMS2101_AA1"

    # act
    result = service.get_eligible_cases(questionnaire_name)

    # assert
    assert result == eligible_cases


def test_get_cases_returns_a_list_of_fully_populated_cases(
    service: QuestionnaireService,
    mock_blaise_service,
):
    questionnaire_cases = [
        get_blaise_case_model_helper.get_populated_case_model(case_id="20001"),
        get_blaise_case_model_helper.get_populated_case_model(case_id="20003"),
    ]

    mock_blaise_service.get_cases.return_value = questionnaire_cases

    questionnaire_name = "LMS2101_AA1"

    # act
    result = service.get_cases(questionnaire_name)

    # assert
    assert result == questionnaire_cases


def test_get_case_returns_a_case(
    service: QuestionnaireService,
    mock_blaise_service,
):
    questionnaire_case = get_blaise_case_model_helper.get_populated_case_model(
        case_id="10010"
    )

    mock_blaise_service.get_case.return_value = questionnaire_case

    questionnaire_name = "LMS2101_AA1"
    case_id = "10010"

    # act
    result = service.get_case(questionnaire_name, case_id)

    # assert
    assert result == questionnaire_case


def test_get_wave_from_questionnaire_name_errors_for_non_lms_questionnaire(
    service: QuestionnaireService,
):
    # arrange
    questionnaire_name = "OPN2101A"

    # act
    with pytest.raises(Exception) as err:
        service.get_wave_from_questionnaire_name(questionnaire_name)

    # assert
    assert str(err.value) == "Invalid format for questionnaire name: OPN2101A"


def test_get_wave_from_questionnaire_name(service: QuestionnaireService):
    # assert
    assert service.get_wave_from_questionnaire_name("LMS2101_AA1") == "1"
    assert service.get_wave_from_questionnaire_name("LMS1234_ZZ2") == "2"


def test_get_wave_from_questionnaire_name_with_invalid_format_raises_error(
    service: QuestionnaireService,
):
    # assert
    with pytest.raises(Exception) as err:
        service.get_wave_from_questionnaire_name("ABC1234_AA1")

    assert str(err.value) == "Invalid format for questionnaire name: ABC1234_AA1"


def test_questionnaire_exists_calls_the_blaise_service_with_the_correct_parameters(
    mock_blaise_service,
    service: QuestionnaireService,
    config,
):
    questionnaire_name = "LMS2101_AA1"

    # act
    service.questionnaire_exists(questionnaire_name)

    # assert
    mock_blaise_service.questionnaire_exists.assert_called_with(questionnaire_name)


@pytest.mark.parametrize(
    "api_response, expected_response", [(False, False), (True, True)]
)
def test_questionnaire_exists_returns_correct_response(
    api_response,
    mock_blaise_service,
    expected_response,
    service: QuestionnaireService,
):
    questionnaire_name = "LMS2101_AA1"
    mock_blaise_service.questionnaire_exists.return_value = api_response

    # act
    result = service.questionnaire_exists(questionnaire_name)

    # assert
    assert result == expected_response


def test_update_case_calls_the_blaise_service_with_the_correct_parameters(
    mock_blaise_service,
    service: QuestionnaireService,
    config,
):
    questionnaire_name = "LMS2101_AA1"
    case_id = "900001"
    data_fields = {
        "hOut": "110",
        "dMktnName": "John Smith",
        "qDataBag.TelNo": "01234 567890",
        "qDataBag.TelNo2": "07734 567890",
    }

    # act
    service.update_case(questionnaire_name, case_id, data_fields)

    # assert
    mock_blaise_service.update_case.assert_called_with(
        questionnaire_name, case_id, data_fields
    )


def test_update_case_does_not_log_personal_identifiable_information(
    mock_blaise_service, service: QuestionnaireService, caplog
):
    # arrange
    mock_blaise_service.update_case.return_value = None
    questionnaire_name = "LMS2101_AA1"
    case_id = "900001"
    data_fields = {
        "hOut": "110",
        "dMktnName": "John Smith",
        "qDataBag.TelNo": "01234 567890",
        "qDataBag.TelNo2": "07734 567890",
    }

    # act & assert
    with caplog.at_level(logging.INFO):
        service.update_case(questionnaire_name, case_id, data_fields)
    assert (
        "root",
        logging.INFO,
        "Attempting to update case 900001 in questionnaire LMS2101_AA1 in Blaise",
    ) in caplog.record_tuples

    with caplog.at_level(logging.INFO):
        service.update_case(questionnaire_name, case_id, data_fields)
    assert (
        not (
            "root",
            logging.INFO,
            "John Smith",
        )
        in caplog.record_tuples
    )

    with caplog.at_level(logging.INFO):
        service.update_case(questionnaire_name, case_id, data_fields)
    assert (
        not (
            "root",
            logging.INFO,
            "01234 567890",
        )
        in caplog.record_tuples
    )

    with caplog.at_level(logging.INFO):
        service.update_case(questionnaire_name, case_id, data_fields)
    assert (
        not (
            "root",
            logging.INFO,
            "07734 567890",
        )
        in caplog.record_tuples
    )


@mock.patch.object(DatastoreService, "get_totalmobile_release_date_records")
def test_get_questionnaires_with_totalmobile_release_date_of_today_only_returns_questionnaires_with_todays_date(
    mock_datastore_service,
    service: QuestionnaireService,
):
    # arrange
    mock_datastore_entity_list = [
        DatastoreHelper.totalmobile_release_date_entity_builder(
            1, "LMS2111Z", datetime.today()
        ),
        DatastoreHelper.totalmobile_release_date_entity_builder(
            2, "LMS2000Z", datetime(2021, 12, 31)
        ),
    ]
    mock_datastore_service.return_value = mock_datastore_entity_list

    # act
    result = service.get_questionnaires_with_totalmobile_release_date_of_today()

    # assert
    assert result == ["LMS2111Z"]


@mock.patch.object(DatastoreService, "get_totalmobile_release_date_records")
def test_get_questionnaires_with_totalmobile_release_date_of_today_returns_an_empty_list_when_there_are_no_release_dates_for_today(
    mock_datastore_service,
    service: QuestionnaireService,
):
    # arrange
    mock_datastore_entity_list = [
        DatastoreHelper.totalmobile_release_date_entity_builder(
            1, "LMS2111Z", datetime(2021, 12, 31)
        ),
        DatastoreHelper.totalmobile_release_date_entity_builder(
            2, "LMS2000Z", datetime(2021, 12, 31)
        ),
    ]

    mock_datastore_service.return_value = mock_datastore_entity_list

    # act
    result = service.get_questionnaires_with_totalmobile_release_date_of_today()

    # assert
    assert result == []


@mock.patch.object(DatastoreService, "get_totalmobile_release_date_records")
def test_get_questionnaires_with_totalmobile_release_date_of_today_returns_an_empty_list_when_there_are_no_records_in_datastore(
    mock_datastore_service,
    service: QuestionnaireService,
):
    # arrange
    mock_datastore_service.return_value = []

    # act
    result = service.get_questionnaires_with_totalmobile_release_date_of_today()

    # assert
    assert result == []
