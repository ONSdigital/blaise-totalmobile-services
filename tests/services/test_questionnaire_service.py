from unittest import mock

import pytest

from models.blaise.uac_model import UacChunks, UacModel
from services.questionnaire_service import (
    get_cases,
    get_eligible_cases,
    get_wave_from_questionnaire_name,
    questionnaire_exists,
    update_case,
)
from tests.helpers import config_helper, get_blaise_case_model_helper


@mock.patch("services.questionnaire_service.get_cases")
@mock.patch("services.eligible_case_service.get_eligible_cases")
def test_get_eligible_cases_calls_the_services_with_the_correct_parameters(
    mock_get_eligible_cases, mock_get_cases
):
    # arrange
    config = config_helper.get_default_config()

    questionnaire_cases = [
        get_blaise_case_model_helper.get_populated_case_model(),  # eligible
        get_blaise_case_model_helper.get_populated_case_model(),  # not eligible
    ]

    eligible_cases = [questionnaire_cases[0]]

    mock_get_cases.return_value = questionnaire_cases
    mock_get_eligible_cases.return_value = eligible_cases

    questionnaire_name = "LMS2101_AA1"

    # act
    get_eligible_cases(questionnaire_name, config)

    # assert
    mock_get_cases.assert_called_with(questionnaire_name, config)
    mock_get_eligible_cases.assert_called_with(questionnaire_cases)


@mock.patch("services.questionnaire_service.get_cases")
@mock.patch("services.eligible_case_service.get_eligible_cases")
def test_get_eligible_cases_returns_the_list_of_eligible_cases_from_the_eligible_case_service(
    mock_get_eligible_cases, mock_get_cases
):
    # arrange
    config = config_helper.get_default_config()

    questionnaire_cases = [
        get_blaise_case_model_helper.get_populated_case_model(),  # eligible
        get_blaise_case_model_helper.get_populated_case_model(),  # not eligible
    ]

    eligible_cases = [questionnaire_cases[0]]

    mock_get_cases.return_value = questionnaire_cases
    mock_get_eligible_cases.return_value = eligible_cases

    questionnaire_name = "LMS2101_AA1"

    # act
    result = get_eligible_cases(questionnaire_name, config)

    # assert
    assert result == eligible_cases


@mock.patch("services.uac_service.get_uacs")
@mock.patch("services.blaise_service.get_cases")
def test_get_cases_returns_a_list_of_fully_populated_cases(
    mock_blaise_service, mock_uac_service
):
    # arrange
    config = config_helper.get_default_config()

    questionnaire_cases = [
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="20001", uac_chunks=UacChunks(uac1="", uac2="", uac3="")
        ),
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="20003", uac_chunks=UacChunks(uac1="", uac2="", uac3="")
        ),
    ]

    questionnaire_uacs = [
        UacModel(
            case_id="20001", uac_chunks=UacChunks(uac1="2324", uac2="6744", uac3="5646")
        ),
        UacModel(
            case_id="20002", uac_chunks=UacChunks(uac1="3324", uac2="7744", uac3="6646")
        ),
        UacModel(
            case_id="20003", uac_chunks=UacChunks(uac1="4324", uac2="8744", uac3="7646")
        ),
    ]

    mock_blaise_service.return_value = questionnaire_cases
    mock_uac_service.return_value = questionnaire_uacs

    questionnaire_name = "LMS2101_AA1"

    # act
    result = get_cases(questionnaire_name, config)

    # assert
    assert result == [
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="20001", uac_chunks=UacChunks(uac1="2324", uac2="6744", uac3="5646")
        ),
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="20003", uac_chunks=UacChunks(uac1="4324", uac2="8744", uac3="7646")
        ),
    ]


def test_get_wave_from_questionnaire_name_errors_for_non_lms_questionnaire():
    # arrange
    questionnaire_name = "OPN2101A"

    # act
    with pytest.raises(Exception) as err:
        get_wave_from_questionnaire_name(questionnaire_name)

    # assert
    assert str(err.value) == "Invalid format for questionnaire name: OPN2101A"


def test_get_wave_from_questionnaire_name():
    # assert
    assert get_wave_from_questionnaire_name("LMS2101_AA1") == "1"
    assert get_wave_from_questionnaire_name("LMS1234_ZZ2") == "2"


def test_get_wave_from_questionnaire_name_with_invalid_format_raises_error():
    # assert
    with pytest.raises(Exception) as err:
        get_wave_from_questionnaire_name("ABC1234_AA1")

    assert str(err.value) == "Invalid format for questionnaire name: ABC1234_AA1"


@mock.patch("services.blaise_service.questionnaire_exists")
def test_questionnaire_exists_calls_the_blaise_service_with_the_correct_parameters(
    mock_blaise_service,
):
    config = config_helper.get_default_config()
    questionnaire_name = "LMS2101_AA1"

    # act
    questionnaire_exists(questionnaire_name, config)

    # assert
    mock_blaise_service.assert_called_with(questionnaire_name, config)


@pytest.mark.parametrize(
    "api_response, expected_response", [(False, False), (True, True)]
)
@mock.patch("services.blaise_service.questionnaire_exists")
def test_questionnaire_exists_returns_correct_response(
    mock_blaise_service, api_response, expected_response
):
    config = config_helper.get_default_config()
    questionnaire_name = "LMS2101_AA1"
    mock_blaise_service.return_value = api_response

    # act
    result = questionnaire_exists(questionnaire_name, config)

    # assert
    assert result == expected_response


@mock.patch("services.blaise_service.update_case")
def test_update_case_calls_the_blaise_service_with_the_correct_parameters(
    mock_blaise_service,
):
    config = config_helper.get_default_config()
    questionnaire_name = "LMS2101_AA1"
    case_id = "900001"
    data_fields = [
        {"hOut": "110"},
        {"dMktnName": "John Smith"},
        {"qDataBag.TelNo": "01234 567890"},
        {"qDataBag.TelNo2": "07734 567890"},
    ]

    # act
    update_case(questionnaire_name, case_id, data_fields, config)

    # assert
    mock_blaise_service.assert_called_with(
        questionnaire_name, case_id, data_fields, config
    )
