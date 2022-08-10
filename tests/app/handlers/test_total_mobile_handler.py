from unittest import mock

from app.handlers.total_mobile_handler import submit_form_result_request_handler
from appconfig.config import Config


@mock.patch("services.questionnaire_service.update_case_field")
def test_submit_form_result_request_handler_passes_the_correct_parameters_to_update_case_telephone_number(
    mock_update_case_field, submit_form_result_request_sample
):
    # arrange
    mock_request = mock.Mock()
    mock_request.get_json.return_value = submit_form_result_request_sample

    # act
    submit_form_result_request_handler(mock_request)

    # assert
    mock_update_case_field.assert_called_with(
        "DST2111Z-AA1", "1001011", 'qDataBag.TelNo', '07000000000', Config.from_env()
    )
