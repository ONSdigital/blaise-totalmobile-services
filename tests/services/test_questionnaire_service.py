import pytest

from services.questionnaire_service import get_questionnaire_cases, get_wave_from_questionnaire_name, get_questionnaire_uacs
from unittest import mock
from tests.helpers import config_helper


@mock.patch("services.blaise_restapi_service.get_questionnaire_case_data")
def test_get_questionnaire_cases_calls_the_service_with_the_correct_parameters(mock_restapi_service):
    config = config_helper.get_default_config()
    questionnaire_name = "LMS2101_AA1"

    # act
    get_questionnaire_cases(questionnaire_name, config)

    # assert
    mock_restapi_service.assert_called_with(questionnaire_name, config)


@mock.patch("services.blaise_restapi_service.get_questionnaire_case_data")
def test_get_questionnaire_cases_returns_a_list_of_questionnaire_models(mock_questionnaire_service):
    # arrange
    config = config_helper.get_default_config()
    mock_questionnaire_service.return_value = [
            {"qiD.Serial_Number": "10010", "hOut": "110"},
            {"qiD.Serial_Number": "10020", "hOut": "210"},
            {"qiD.Serial_Number": "10030", "hOut": "310"},
        ]

    questionnaire_name = "LMS2101_AA1"

    # act
    result = get_questionnaire_cases(questionnaire_name, config)

    # assert
    assert len(result) == 3

    assert result[0].serial_number == "10010"
    assert result[0].outcome_code == "110"

    assert result[1].serial_number == "10020"
    assert result[1].outcome_code == "210"

    assert result[2].serial_number == "10030"
    assert result[2].outcome_code == "310"


@mock.patch("services.uac_restapi_service.get_questionnaire_uacs")
def test_get_questionnaire_uacs_calls_the_service_with_the_correct_parameters(mock_uac_service):
    config = config_helper.get_default_config()
    questionnaire_name = "LMS2101_AA1"

    # act
    get_questionnaire_uacs(questionnaire_name, config)

    # assert
    mock_uac_service.assert_called_with(questionnaire_name, config)


def test_get_wave_from_questionnaire_name_errors_for_non_lms_questionnaire():
    # arrange
    questionnaire_name = "OPN2101A"

    # act
    with pytest.raises(Exception) as err:
        get_wave_from_questionnaire_name(questionnaire_name)

    # assert
    assert str(err.value) == "Invalid format for questionnaire name: OPN2101A"


def test_get_wave_from_questionnaire_name():
    assert get_wave_from_questionnaire_name("LMS2101_AA1") == "1"
    assert get_wave_from_questionnaire_name("LMS1234_ZZ2") == "2"


def test_get_wave_from_questionnaire_name_with_invalid_format_raises_error():
    with pytest.raises(Exception) as err:
        get_wave_from_questionnaire_name("ABC1234_AA1")
    assert str(err.value) == "Invalid format for questionnaire name: ABC1234_AA1"