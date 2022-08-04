import blaise_restapi
import pytest

from services.questionnaire_service import get_questionnaire_cases
from unittest import mock
from tests.helpers import config_helper


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_case_data_calls_the_rest_api_client_with_the_correct_parameters(_mock_rest_api_client):
    config = config_helper.get_default_config()
    blaise_server_park = "gusty"
    questionnaire_name = "DST2106Z"
    fields = [
        "qiD.Serial_Number",
        "dataModelName",
        "qDataBag.TLA",
        "qDataBag.Wave",
        "qDataBag.Prem1",
        "qDataBag.Prem2",
        "qDataBag.Prem3",
        "qDataBag.District",
        "qDataBag.PostTown",
        "qDataBag.PostCode",
        "qDataBag.TelNo",
        "qDataBag.TelNo2",
        "telNoAppt",
        "hOut",
        "qDataBag.UPRN_Latitude",
        "qDataBag.UPRN_Longitude",
        "qDataBag.Priority",
        "qDataBag.FieldRegion",
        "qDataBag.FieldTeam",
        "qDataBag.WaveComDTE"
    ]

    # act
    get_questionnaire_cases(questionnaire_name, config)

    # assert
    _mock_rest_api_client.assert_called_with(
        blaise_server_park, questionnaire_name, fields
    )


@mock.patch.object(blaise_restapi.Client, "get_questionnaire_data")
def test_get_case_data_returns_the_case_data_supplied_by_the_rest_api_client(
        _mock_rest_api_client,
):
    # arrange
    config = config_helper.get_default_config()
    _mock_rest_api_client.return_value = {
        "questionnaireName": "DST2106Z",
        "questionnaireId": "12345-12345-12345-12345-12345",
        "reportingData": [
            {"qiD.Serial_Number": "10010", "hOut": "110"},
            {"qiD.Serial_Number": "10020", "hOut": "210"},
            {"qiD.Serial_Number": "10030", "hOut": "310"},
        ],
    }
    questionnaire_name = "OPN2101A"

    # act
    result = get_questionnaire_cases(questionnaire_name, config)

    # assert
    assert result[0].serial_number == "10010"
    assert result[0].outcome_code == "110"

    assert result[1].serial_number == "10020"
    assert result[1].outcome_code == "210"

    assert result[2].serial_number == "10030"
    assert result[2].outcome_code == "310"

