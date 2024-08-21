from datetime import datetime
from typing import Dict

import pytest

from services.create.mappers.blaise_frs_case_mapper_service import (
    BlaiseFRSCaseMapperService,
)


class TestFRSCaseMapping:
    @pytest.fixture()
    def service(self) -> BlaiseFRSCaseMapperService:
        return BlaiseFRSCaseMapperService()

    @pytest.fixture()
    def valid_case_data_dictionary(self) -> Dict:
        return {
            "qiD.Serial_Number": "90000000",
            "dataModelName": "LM2007",
            "qDataBag.Prem1": "12 Blaise Street",
            "qDataBag.Prem2": "Blaise Hill",
            "qDataBag.Prem3": "Blaiseville",
            "qDataBag.District": "Gwent",
            "qDataBag.PostTown": "Newport",
            "qDataBag.PostCode": "FML134D",
            "hOut": "301",
            "qDataBag.UPRN": "100012675377",
            "qDataBag.UPRN_Latitude": "10020202",
            "qDataBag.UPRN_Longitude": "34949494",
            "qDataBag.Priority": "1",
            "qDataBag.FieldCase": "Y",
            "qDataBag.FieldRegion": "gwent",
            "qDataBag.FieldTeam": "B-Team",
            "qDataBag.WaveComDTE": "31-01-2023",
            "qDataBag.TLA": "FRS",
            "qDataBag.DivAddInd": "",
            "qDataBag.Rand": "1",
        }

    def test_map_frs_case_information_model_maps_the_correct_model(
        self, service, valid_case_data_dictionary
    ):

        # arrange
        questionnaire_name = "FRS2101"

        # act
        result = service.map_frs_case_information_model(
            questionnaire_name, valid_case_data_dictionary
        )

        # assert
        assert result.questionnaire_name == "FRS2101"
        assert result.case_id == "90000000"
        assert result.data_model_name == "LM2007"
        assert result.address_details.address.address_line_1 == "12 Blaise Street"
        assert result.address_details.address.address_line_2 == "Blaise Hill"
        assert result.address_details.address.address_line_3 == "Blaiseville"
        assert result.address_details.address.county == "Gwent"
        assert result.address_details.address.town == "Newport"
        assert result.address_details.address.postcode == "FML134D"
        assert result.address_details.reference == "100012675377"
        assert result.address_details.address.coordinates.latitude == "10020202"
        assert result.address_details.address.coordinates.longitude == "34949494"
        assert result.priority == "1"
        assert result.field_region == "gwent"
        assert result.field_case == "Y"
        assert result.field_team == "B-Team"
        assert result.wave_com_dte == datetime(2023, 1, 31)
        assert result.tla == "FRS"
        assert result.divided_address_indicator == ""
        assert result.uac_chunks is None
        assert result.rand == 1

    def test_map_frs_case_information_model_returns_a_valid_object_with_the_field_set_to_none_when_a_blaise_field_is_incorrectly_typed(
        self,
        service,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "FRS2101"

        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary.pop("qiD.Serial_Number")
        case_data_dictionary["qdatabag.Serial_Number"] = "90000000"

        # act
        result = service.map_frs_case_information_model(
            questionnaire_name, valid_case_data_dictionary
        )

        # assert
        assert result.questionnaire_name == "FRS2101"
        assert result.case_id is None

    def test_map_frs_case_information_model_returns_a_valid_object_with_the_field_set_to_none_when_an_optional_blaise_field_is_missing(
        self,
        service,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "FRS2101"

        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary.pop("qiD.Serial_Number")

        # act
        result = service.map_frs_case_information_model(
            questionnaire_name, valid_case_data_dictionary
        )

        # assert
        assert result.questionnaire_name == "FRS2101"
        assert result.case_id is None

    def test_map_frs_case_information_model_sets_date_to_none_if_date_is_an_empty_string(
        self, service, valid_case_data_dictionary
    ):
        # arrange
        questionnaire_name = "FRS2101"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary["qDataBag.WaveComDTE"] = ""

        # act
        result = service.map_frs_case_information_model(
            questionnaire_name, case_data_dictionary
        )

        # assert
        assert result.wave_com_dte is None

    def test_map_frs_case_information_model_sets_address_reference_to_an_empty_string_when_the_uprn_field_does_not_exist(
        self,
        service,
        valid_case_data_dictionary,
    ):
        # arrange
        questionnaire_name = "FRS2101"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary.pop("qDataBag.UPRN")

        # act
        result = service.map_frs_case_information_model(
            questionnaire_name, case_data_dictionary
        )

        # assert
        assert result.address_details.reference == ""

    def test_map_frs_case_information_model_sets_rand_to_zero_when_the_field_is_not_set(
            self,
            service,
            valid_case_data_dictionary
    ):
        # arrange
        questionnaire_name = "FRS2101"
        case_data_dictionary = valid_case_data_dictionary
        case_data_dictionary["qDataBag.Rand"] = ""

        # act
        result = service.map_frs_case_information_model(
            questionnaire_name, case_data_dictionary
        )

        # assert
        assert result.rand == 0
