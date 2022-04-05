from unittest.mock import patch

import blaise_restapi

from app.services.total_mobile_service import update_case_telephone_number


@patch("blaise_restapi.Client.patch_case_data")
def test_update_case_telephone_number_passes_the_correct_parameters_to_the_restapi(mock_blaise_restapi_patch_case_data):
    # arrange
    instrument_name = "DST2101Z"
    case_id = "1110111"
    telephone_number = "07123456789"
    data_fields = {"qDataBag.TelNo": telephone_number}

    # act
    update_case_telephone_number(instrument_name, case_id, telephone_number)

    # assert
    mock_blaise_restapi_patch_case_data.assert_called_with("gusty", instrument_name, case_id, data_fields)
