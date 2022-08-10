from unittest import mock

from app.handlers.total_mobile_handler import submit_form_result_request_handler


@mock.patch("app.handlers.total_mobile_handler.update_case_telephone_number")
def test_submit_form_result_request_handler_passes_the_correct_parameters_to_update_case_telephone_number(
    mock_update_case_telephone_number, submit_form_result_request_sample
):
    # arrange
    mock_request = mock.Mock()
    mock_request.get_json.return_value = submit_form_result_request_sample

    # act
    submit_form_result_request_handler(mock_request)

    # assert
    mock_update_case_telephone_number.assert_called_with(
        "DST2111Z-AA1", "1001011", "07000000000"
    )
