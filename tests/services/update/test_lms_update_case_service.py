from unittest.mock import Mock, patch

import pytest

from models.update.blaise_update_case_model import BlaiseUpdateCase
from services.update.lms_update_case_service import LMSUpdateCaseService
from tests.helpers.totalmobile_incoming_update_request_helper import lms_totalmobile_incoming_update_request_helper


@pytest.fixture()
def mock_blaise_service():
    return Mock()


@pytest.fixture()
def mock_case_update_service(mock_blaise_service):
    return LMSUpdateCaseService(mock_blaise_service)


@pytest.fixture()
def mock_blaise_case():
    blaise_case = Mock(spec=BlaiseUpdateCase)
    blaise_case.outcome_code = 0
    blaise_case.case_id = "90001"
    return blaise_case


@patch.object(LMSUpdateCaseService, "validate_questionnaire_exists")
@patch.object(LMSUpdateCaseService, "get_existing_blaise_case")
@patch.object(LMSUpdateCaseService, "_should_update_case_contact_information", return_value=False)
@patch.object(LMSUpdateCaseService, "_should_update_case_outcome_code", return_value=False)
@patch.object(LMSUpdateCaseService, "_log_no_update")
def test_update_case_calls_validate_questionnaire_exists_once_with_correct_parameters(
        _mock_log_no_update,            # patch
        _mock_should_update_outcome,    # patch
        _mock_should_update_contact,    # patch
        mock_get_existing_blaise_case,  # patch
        mock_validate,                  # patch
        mock_case_update_service,       # fixture
):
    # arrange
    questionnaire_name = "LMS2101_AA1"
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper(questionnaire_name)
    mock_get_existing_blaise_case.return_value = BlaiseUpdateCase(questionnaire_name, {})

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_validate.assert_called_once_with(mock_totalmobile_request.questionnaire_name)


def test_update_case_calls_get_existing_blaise_case_once_with_correct_parameters(
    mock_case_update_service
):
    # arrange
    mock_case_update_service.get_existing_blaise_case = Mock()
    mock_totalmobile_request = lms_totalmobile_incoming_update_request_helper()

    # act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # assert
    mock_case_update_service.get_existing_blaise_case.assert_called_once_with(
        mock_totalmobile_request.questionnaire_name, mock_totalmobile_request.case_id
    )
