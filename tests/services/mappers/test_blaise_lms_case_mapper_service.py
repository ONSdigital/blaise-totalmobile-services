from datetime import datetime
from typing import Dict

import pytest

from client.bus import Uac
from models.blaise.questionnaire_uac_model import QuestionnaireUacModel, UacChunks
from services.mappers.blaise_lms_case_mapper_service import BlaiseLMSCaseMapperService


class TestLMSCaseMapping:
    @pytest.fixture()
    def service(self) -> BlaiseLMSCaseMapperService:
        return BlaiseLMSCaseMapperService()

    @pytest.fixture()
    def questionnaire_uac_model(self) -> QuestionnaireUacModel:
        uac_data_dictionary: Dict[str, Uac] = {
            "10010": {
                "instrument_name": "OPN2101A",
                "case_id": "10010",
                "uac_chunks": {
                    "uac1": "8175",
                    "uac2": "4725",
                    "uac3": "3990",
                    "uac4": "None",
                },
                "full_uac": "817647263991",
            }
        }

        questionnaire_uac_model = QuestionnaireUacModel.import_uac_data(
            uac_data_dictionary
        )
        return questionnaire_uac_model

    @pytest.fixture()
    def valid_case_data_dictionary(self) -> Dict:
        return {
            "qiD.Serial_Number": "10010",
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
            "qDataBag.UPRN": "100012675377",
            "qDataBag.UPRN_Latitude": "10020202",
            "qDataBag.UPRN_Longitude": "34949494",
            "qDataBag.Priority": "1",
            "qDataBag.FieldCase": "Y",
            "qDataBag.FieldRegion": "gwent",
            "qDataBag.FieldTeam": "B-Team",
            "qDataBag.WaveComDTE": "31-01-2023",
            "catiMana.CatiCall.RegsCalls[1].DialResult": "1",
            "qRotate.RDMktnIND": "2",
            "qRotate.RHOut": "310",
            "qDataBag.TLA": "LMB",
        }

    def test_map_lms_case_information_model_maps_the_correct_model(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):

        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_id = "10010"
        valid_case_data_dictionary["qiD.Serial_Number"] = case_id

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, valid_case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.questionnaire_name == "LMS2101_AA1"
        assert result.case_id == case_id
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
        assert result.address_details.reference == "100012675377"
        assert result.address_details.address.coordinates.latitude == "10020202"
        assert result.address_details.address.coordinates.longitude == "34949494"
        assert result.priority == "1"
        assert result.field_region == "gwent"
        assert result.field_case == "Y"
        assert result.field_team == "B-Team"
        assert result.wave_com_dte == datetime(2023, 1, 31)
        assert result.has_call_history is True
        assert result.has_uac is True
        assert result.rotational_knock_to_nudge_indicator == "N"
        assert result.rotational_outcome_code == 310
        assert result.tla == "LMS"
        assert result.uac_chunks == UacChunks(
            uac1="8175", uac2="4725", uac3="3990", uac4="None"
        )

    def test_map_lms_case_information_model_maps_the_correct_model_when_no_uacs_are_available(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):

        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_id = "20010"  # no uac in uac dictionary above
        valid_case_data_dictionary["qiD.Serial_Number"] = case_id

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, valid_case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.questionnaire_name == "LMS2101_AA1"
        assert result.case_id == case_id
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
        assert result.address_details.reference == "100012675377"
        assert result.address_details.address.coordinates.latitude == "10020202"
        assert result.address_details.address.coordinates.longitude == "34949494"
        assert result.priority == "1"
        assert result.field_region == "gwent"
        assert result.field_case == "Y"
        assert result.field_team == "B-Team"
        assert result.wave_com_dte == datetime(2023, 1, 31)
        assert result.has_call_history is True
        assert result.has_uac is True
        assert result.rotational_knock_to_nudge_indicator == "N"
        assert result.rotational_outcome_code == 310
        assert result.tla == "LMS"
        assert result.uac_chunks is None

    def test_map_lms_case_information_model_maps_the_correct_model_when_no_uac_model_is_passed_through(
        self,
        service,
        valid_case_data_dictionary,
    ):

        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_id = "20010"  # no uac in uac dictionary above
        valid_case_data_dictionary["qiD.Serial_Number"] = case_id

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, valid_case_data_dictionary, None
        )

        # assert
        assert result.questionnaire_name == "LMS2101_AA1"
        assert result.case_id == case_id
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
        assert result.address_details.reference == "100012675377"
        assert result.address_details.address.coordinates.latitude == "10020202"
        assert result.address_details.address.coordinates.longitude == "34949494"
        assert result.priority == "1"
        assert result.field_region == "gwent"
        assert result.field_case == "Y"
        assert result.field_team == "B-Team"
        assert result.wave_com_dte == datetime(2023, 1, 31)
        assert result.has_call_history is True
        assert result.has_uac is True
        assert result.rotational_knock_to_nudge_indicator == "N"
        assert result.rotational_outcome_code == 310
        assert result.tla == "LMS"
        assert result.uac_chunks is None

    def test_map_lms_case_information_model_returns_a_valid_object_with_the_field_set_to_none_when_a_blaise_field_is_incorrectly_typed(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"

        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary.pop("qiD.Serial_Number")
        case_data_dictionary["qdatabag.Serial_Number"] = "90000000"

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, valid_case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.questionnaire_name == "LMS2101_AA1"
        assert result.case_id is None

    def test_map_lms_case_information_model_returns_a_valid_object_with_the_field_set_to_none_when_an_optional_blaise_field_is_missing(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"

        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary.pop("qiD.Serial_Number")

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, valid_case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.questionnaire_name == "LMS2101_AA1"
        assert result.case_id is None

    def test_map_lms_case_information_model_sets_outcome_code_to_zero_if_empty(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary["hOut"] = ""

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, valid_case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.outcome_code == 0

    def test_map_lms_case_information_model_sets_outcome_code_to_zero_if_not_supplied(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary.pop("hOut")

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, valid_case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.outcome_code == 0

    def test_map_lms_case_information_model_sets_has_call_history_to_true_when_blaise_case_has_call_history(
        self, service, questionnaire_uac_model
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"

        case_data_dictionary = {
            "qDataBag.WaveComDTE": "31-01-2023",
            "catiMana.CatiCall.RegsCalls[1].DialResult": "1",
        }

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.has_call_history is True

    def test_map_lms_case_information_model_sets_has_call_history_to_false_when_blaise_case_has_no_call_history(
        self, service, questionnaire_uac_model
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"

        case_data_dictionary = {
            "qDataBag.WaveComDTE": "31-01-2023",
            "catiMana.CatiCall.RegsCalls[1].DialResult": "",
        }

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.has_call_history is False

    def test_map_lms_case_information_model_sets_has_call_history_to_false_when_blaise_case_is_missing_call_history(
        self, service, questionnaire_uac_model
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"

        case_data_dictionary = {
            "qDataBag.WaveComDTE": "31-01-2023",
        }

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.has_call_history is False

    def test_map_lms_case_information_model_sets_date_to_none_if_date_is_an_empty_string(
        self, service, questionnaire_uac_model, valid_case_data_dictionary
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary["qDataBag.WaveComDTE"] = ""

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.wave_com_dte is None

    def test_map_lms_case_information_model_sets_rotational_outcome_code_to_zero_if_empty(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary["qRotate.RHOut"] = ""

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.rotational_outcome_code == 0

    def test_map_lms_case_information_model_sets_rotational_knock_to_nudge_indicator_to_empty_if_not_supplied(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary.pop("qRotate.RDMktnIND")

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.rotational_knock_to_nudge_indicator == ""

    def test_map_lms_case_information_model_sets_rotational_knock_to_nudge_indicator_to_empty_if_not_it_doesnt_have_a_value(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary["qRotate.RDMktnIND"] = ""

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.rotational_knock_to_nudge_indicator == ""

    def test_map_lms_case_information_model_sets_rotational_knock_to_nudge_indicator_to_y_if_its_value_is_1(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary["qRotate.RDMktnIND"] = "1"

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.rotational_knock_to_nudge_indicator == "Y"

    def test_map_lms_case_information_model_sets_rotational_knock_to_nudge_indicator_to_n_if_its_value_is_2(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary["qRotate.RDMktnIND"] = "2"

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.rotational_knock_to_nudge_indicator == "N"

    def test_map_lms_case_information_model_sets_rotational_outcome_code_to_zero_if_not_supplied(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary.pop("qRotate.RHOut")

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.rotational_outcome_code == 0

    def test_map_lms_case_information_model_sets_address_reference_to_an_empty_string_when_the_uprn_field_does_not_exist(
        self,
        service,
        questionnaire_uac_model,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary.pop("qDataBag.UPRN")

        # act
        result = service.map_lms_case_information_model(
            questionnaire_name, case_data_dictionary, questionnaire_uac_model
        )

        # assert
        assert result.address_details.reference == ""
