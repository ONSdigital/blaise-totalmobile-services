from unittest import mock

from app.handlers.total_mobile_handler import submit_form_result_request_handler
from appconfig.config import Config


def test_submit_form_result_request_handler_passes_the_correct_parameters_to_update_case_telephone_number(
    submit_form_result_request_sample
):
    # arrange
    mock_request = mock.Mock()
    mock_request.get_json.return_value = submit_form_result_request_sample
    mock_questionnaire_service = mock.Mock()
    
    # act
    submit_form_result_request_handler(mock_request, mock_questionnaire_service)

    # assert
    mock_questionnaire_service.update_case_field.assert_called_with(
        "DST2111Z-AA1", "1001011", 'qDataBag.TelNo', '07000000000', Config.from_env()
    )
