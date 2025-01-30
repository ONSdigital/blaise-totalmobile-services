from unittest.mock import Mock

import pytest

from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.update.lms_update_case_service import LMSUpdateCaseService


@pytest.fixture()
def mock_blaise_service():
    return Mock()


@pytest.fixture()
def mock_case_update_service(mock_blaise_service):
    return LMSUpdateCaseService(mock_blaise_service)


@pytest.fixture()
def mock_totalmobile_request():
    return TotalMobileIncomingUpdateRequestModel(
        questionnaire_name="LMS2101_AA1",
        case_id="90001",
        outcome_code=300,
        contact_name="Joe Bloggs",
        home_phone_number="01234567890",
        mobile_phone_number="07123123123",
    )


def test_update_case_calls_get_existing_blaise_case_with_correct_parameters(
    mock_case_update_service, mock_totalmobile_request
):
    # Arrange
    mock_case_update_service.get_existing_blaise_case = Mock()

    # Act
    mock_case_update_service.update_case(mock_totalmobile_request)

    # Assert
    mock_case_update_service.get_existing_blaise_case.assert_called_once_with(
        mock_totalmobile_request.questionnaire_name, mock_totalmobile_request.case_id
    )
