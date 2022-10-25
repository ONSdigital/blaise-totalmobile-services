from datetime import datetime
from typing import Dict

from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel


def valid_case_data_dictionary() -> Dict:
    return {
        "qiD.Serial_Number": "90000000",
        "dataModelName": "LM2007",
        "qDataBag.Wave": 1,
        "qDataBag.Prem1": "12 Blaise Street",
        "qDataBag.Prem2": "Blaise Hill",
        "qDataBag.Prem3": "Blaiseville",
        "qDataBag.District": "Gwent",
        "qDataBag.PostTown": "Newport",
        "qDataBag.PostCode": "FML134D",
        "qDataBag.TelNo": "07900990901",
        "qDataBag.TelNo2": "07900990902",
        "telNoAppt": "07900990903",
        "hOut": "301",
        "qDataBag.UPRN_Latitude": "10020202",
        "qDataBag.UPRN_Longitude": "34949494",
        "qDataBag.Priority": "1",
        "qDataBag.FieldCase": "Y",
        "qDataBag.FieldRegion": "gwent",
        "qDataBag.FieldTeam": "B-Team",
        "qDataBag.WaveComDTE": "31-01-2023",
        "catiMana.CatiCall.RegsCalls[1].DialResult": "1",
        "qRotate.RDMktnIND": "Y",
        "qRotate.RHOut": "310",
    }


def test_import_case_returns_a_populated_model():
    # arrange
    questionnaire_name = "LMS2101_AA1"

    case_data_dictionary = valid_case_data_dictionary()

    # act
    result = BlaiseCaseInformationModel.import_case(
        questionnaire_name, case_data_dictionary
    )

    # assert
    assert result.questionnaire_name == "LMS2101_AA1"
    assert result.case_id == "90000000"
    assert result.data_model_name == "LM2007"
    assert result.wave == 1
    assert result.address_details.address.address_line_1 == "12 Blaise Street"
    assert result.address_details.address.address_line_2 == "Blaise Hill"
    assert result.address_details.address.address_line_3 == "Blaiseville"
    assert result.address_details.address.county == "Gwent"
    assert result.address_details.address.town == "Newport"
    assert result.address_details.address.postcode == "FML134D"
    assert result.contact_details.telephone_number_1 == "07900990901"
    assert result.contact_details.telephone_number_2 == "07900990902"
    assert result.contact_details.appointment_telephone_number == "07900990903"
    assert result.outcome_code == 301
    assert result.address_details.address.coordinates.latitude == "10020202"
    assert result.address_details.address.coordinates.longitude == "34949494"
    assert result.priority == "1"
    assert result.field_region == "gwent"
    assert result.field_case == "Y"
    assert result.field_team == "B-Team"
    assert result.wave_com_dte == datetime(2023, 1, 31)
    assert result.has_call_history is True
    assert result.rotational_knock_to_nudge_indicator == "Y"
    assert result.rotational_outcome_code == 310


def test_import_case_returns_a_valid_object_with_the_field_set_to_none_when_a_blaise_field_is_incorrectly_typed():
    # arrange
    questionnaire_name = "LMS2101_AA1"

    case_data_dictionary = valid_case_data_dictionary()
    case_data_dictionary.pop("qiD.Serial_Number")
    case_data_dictionary["qdatabag.Serial_Number"] = "90000000"

    # act
    result = BlaiseCaseInformationModel.import_case(
        questionnaire_name, case_data_dictionary
    )

    # assert
    assert result.questionnaire_name == "LMS2101_AA1"
    assert result.case_id is None


def test_import_case_returns_a_valid_object_with_the_field_set_to_none_when_an_optional_blaise_field_is_missing():
    # arrange
    questionnaire_name = "LMS2101_AA1"

    case_data_dictionary = valid_case_data_dictionary()
    case_data_dictionary.pop("qiD.Serial_Number")

    # act
    result = BlaiseCaseInformationModel.import_case(
        questionnaire_name, case_data_dictionary
    )

    # assert
    assert result.questionnaire_name == "LMS2101_AA1"
    assert result.case_id is None


def test_import_case_sets_outcome_code_to_zero_if_empty():
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_data_dictionary = valid_case_data_dictionary()
    case_data_dictionary["hOut"] = ""

    # act
    result = BlaiseCaseInformationModel.import_case(
        questionnaire_name, case_data_dictionary
    )

    # assert
    assert result.outcome_code == 0


def test_import_case_sets_outcome_code_to_zero_if_not_supplied():
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_data_dictionary = valid_case_data_dictionary()
    case_data_dictionary.pop("hOut")

    # act
    result = BlaiseCaseInformationModel.import_case(
        questionnaire_name, case_data_dictionary
    )

    # assert
    assert result.outcome_code == 0


def test_import_case_sets_has_call_history_to_true_when_blaise_case_has_call_history():
    # arrange
    questionnaire_name = "LMS2101_AA1"

    case_data_dictionary = {
        "qDataBag.WaveComDTE": "31-01-2023",
        "catiMana.CatiCall.RegsCalls[1].DialResult": "1",
    }

    # act
    result = BlaiseCaseInformationModel.import_case(
        questionnaire_name, case_data_dictionary
    )

    # assert
    assert result.has_call_history is True


def test_import_case_sets_has_call_history_to_false_when_blaise_case_has_no_call_history():
    # arrange
    questionnaire_name = "LMS2101_AA1"

    case_data_dictionary = {
        "qDataBag.WaveComDTE": "31-01-2023",
        "catiMana.CatiCall.RegsCalls[1].DialResult": "",
    }

    # act
    result = BlaiseCaseInformationModel.import_case(
        questionnaire_name, case_data_dictionary
    )

    # assert
    assert result.has_call_history is False


def test_import_case_sets_has_call_history_to_false_when_blaise_case_is_missing_call_history():
    # arrange
    questionnaire_name = "LMS2101_AA1"

    case_data_dictionary = {
        "qDataBag.WaveComDTE": "31-01-2023",
    }

    # act
    result = BlaiseCaseInformationModel.import_case(
        questionnaire_name, case_data_dictionary
    )

    # assert
    assert result.has_call_history is False


def test_import_case_sets_date_to_none_if_date_is_an_empty_string():
    # arrange
    case_data_dictionary = valid_case_data_dictionary()
    case_data_dictionary["qDataBag.WaveComDTE"] = ""

    # act
    result = BlaiseCaseInformationModel.import_case("LMS", case_data_dictionary)

    # assert
    assert result.wave_com_dte is None


def test_import_case_sets_rotational_outcome_code_to_zero_if_empty():
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_data_dictionary = valid_case_data_dictionary()
    case_data_dictionary["qRotate.RHOut"] = ""

    # act
    result = BlaiseCaseInformationModel.import_case(
        questionnaire_name, case_data_dictionary
    )

    # assert
    assert result.rotational_outcome_code == 0


def test_import_case_sets_rotational_outcome_code_to_zero_if_not_supplied():
    # arrange
    questionnaire_name = "LMS2101_AA1"
    case_data_dictionary = valid_case_data_dictionary()
    case_data_dictionary.pop("qRotate.RHOut")

    # act
    result = BlaiseCaseInformationModel.import_case(
        questionnaire_name, case_data_dictionary
    )

    # assert
    assert result.rotational_outcome_code == 0
