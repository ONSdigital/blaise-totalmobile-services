from unittest import mock

from app.services.total_mobile_service import update_case_telephone_number
from appconfig import Config


@mock.patch("blaise_restapi.Client.patch_case_data")
@mock.patch.object(Config, "from_env")
def test_update_case_telephone_number_passes_the_correct_parameters_to_the_restapi(
    _mock_config_from_env, mock_blaise_restapi_patch_case_data
):
    # arrange
    questionnaire_name = "DST2101Z"
    case_id = "1110111"
    telephone_number = "07123456789"
    data_fields = {"qDataBag.TelNo": telephone_number}

    server_park = "gusty"
    _mock_config_from_env.return_value = Config(
        "", "", "", "", "", "", "", "", "", server_park, "", "", ""
    )

    # act
    update_case_telephone_number(questionnaire_name, case_id, telephone_number)

    # assert
    mock_blaise_restapi_patch_case_data.assert_called_with(
        server_park, questionnaire_name, case_id, data_fields
    )
