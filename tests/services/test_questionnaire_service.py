from unittest import mock
from unittest.mock import Mock

import pytest

from appconfig import Config
from models.blaise.uac_model import UacChunks, UacModel
from services.questionnaire_service import QuestionnaireService
from tests.helpers import config_helper, get_blaise_case_model_helper


@pytest.fixture()
def mock_blaise_service():
    return Mock()


@pytest.fixture()
def mock_eligible_case_service():
    return Mock()


@pytest.fixture()
def mock_uac_service():
    return Mock()


@pytest.fixture()
def config() -> Config:
    return config_helper.get_default_config()


@pytest.fixture()
def service(
    config, mock_blaise_service, mock_eligible_case_service, mock_uac_service
) -> QuestionnaireService:
    return QuestionnaireService(
        config,
        blaise_service=mock_blaise_service,
        eligible_case_service=mock_eligible_case_service,
        uac_service=mock_uac_service,
    )


@mock.patch.object(QuestionnaireService, "get_cases")
def test_get_eligible_cases_calls_the_services_with_the_correct_parameters(
    mock_get_cases,
    mock_eligible_case_service,
    service,
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
    service,
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
    mock_uac_service,
    service,
    mock_blaise_service,
):
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

    mock_blaise_service.get_cases.return_value = questionnaire_cases
    mock_uac_service.get_uacs.return_value = questionnaire_uacs

    questionnaire_name = "LMS2101_AA1"

    # act
    result = service.get_cases(questionnaire_name)

    # assert
    assert result == [
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="20001", uac_chunks=UacChunks(uac1="2324", uac2="6744", uac3="5646")
        ),
        get_blaise_case_model_helper.get_populated_case_model(
            case_id="20003", uac_chunks=UacChunks(uac1="4324", uac2="8744", uac3="7646")
        ),
    ]


def test_get_wave_from_questionnaire_name_errors_for_non_lms_questionnaire(service):
    # arrange
    questionnaire_name = "OPN2101A"

    # act
    with pytest.raises(Exception) as err:
        service.get_wave_from_questionnaire_name(questionnaire_name)

    # assert
    assert str(err.value) == "Invalid format for questionnaire name: OPN2101A"


def test_get_wave_from_questionnaire_name(service):
    # assert
    assert service.get_wave_from_questionnaire_name("LMS2101_AA1") == "1"
    assert service.get_wave_from_questionnaire_name("LMS1234_ZZ2") == "2"


def test_get_wave_from_questionnaire_name_with_invalid_format_raises_error(service):
    # assert
    with pytest.raises(Exception) as err:
        service.get_wave_from_questionnaire_name("ABC1234_AA1")

    assert str(err.value) == "Invalid format for questionnaire name: ABC1234_AA1"


def test_questionnaire_exists_calls_the_blaise_service_with_the_correct_parameters(
    mock_blaise_service,
    service,
    config,
):
    questionnaire_name = "LMS2101_AA1"

    # act
    service.questionnaire_exists(questionnaire_name)

    # assert
    mock_blaise_service.questionnaire_exists.assert_called_with(
        questionnaire_name, config
    )


@pytest.mark.parametrize(
    "api_response, expected_response", [(False, False), (True, True)]
)
def test_questionnaire_exists_returns_correct_response(
    api_response,
    mock_blaise_service,
    expected_response,
    service,
):
    questionnaire_name = "LMS2101_AA1"
    mock_blaise_service.questionnaire_exists.return_value = api_response

    # act
    result = service.questionnaire_exists(questionnaire_name)

    # assert
    assert result == expected_response


def test_update_case_calls_the_blaise_service_with_the_correct_parameters(
    mock_blaise_service,
    service,
    config,
):
    questionnaire_name = "LMS2101_AA1"
    case_id = "900001"
    data_fields = [
        {"hOut": "110"},
        {"dMktnName": "John Smith"},
        {"qDataBag.TelNo": "01234 567890"},
        {"qDataBag.TelNo2": "07734 567890"},
    ]

    # act
    service.update_case(questionnaire_name, case_id, data_fields)

    # assert
    mock_blaise_service.update_case.assert_called_with(
        questionnaire_name, case_id, data_fields, config
    )
