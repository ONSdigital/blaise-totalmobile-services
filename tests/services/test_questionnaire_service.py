import pytest

from models.case_model import CaseModel
from services.questionnaire_service import get_eligible_cases, get_wave_from_questionnaire_name
from unittest import mock
from tests.helpers import config_helper


@mock.patch("services.blaise_restapi_service.get_cases")
def test_get_eligible_cases_calls_the_service_with_the_correct_parameters(mock_restapi_service):
    # arrange
    config = config_helper.get_default_config()
    questionnaire_name = "LMS2101_AA1"

    # act
    get_eligible_cases(questionnaire_name, config)

    # assert
    mock_restapi_service.assert_called_with(questionnaire_name, config)


@mock.patch("services.blaise_restapi_service.get_cases")
def test_get_eligible_cases_returns_a_list_of_eligible_case_models_from_the_client(mock_restapi_service):
    # arrange
    config = config_helper.get_default_config()
    case_models = [
        # should return
        CaseModel(
            telephone_number_1="",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
        # should not return
        CaseModel(
            telephone_number_1="123435",
            telephone_number_2="",
            appointment_telephone_number="",
            wave="1",
            priority="1",
            outcome_code="310"
        ),
    ]

    mock_restapi_service.return_value = case_models

    questionnaire_name = "LMS2101_AA1"

    # act
    result = get_eligible_cases(questionnaire_name, config)

    # assert
    assert result == [case_models[0]]


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