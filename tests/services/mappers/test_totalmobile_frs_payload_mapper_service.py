from datetime import datetime
from typing import Dict

import pytest

from models.create.blaise.blaiise_frs_case_model import BlaiseFRSCaseModel
from services.create.mappers.totalmobile_payload_mapper_service import (
    TotalmobilePayloadMapperService,
)


class TestTotalmobileFRSPayloadMapping:
    @pytest.fixture()
    def case_data(self) -> Dict[str, str]:
        return {
            "qiD.Serial_Number": "90001",
            "qDataBag.Wave": "1",
            "hOut": "301",
            "qDataBag.TelNo": "07900990901",
            "qDataBag.TelNo2": "07900990902",
            "telNoAppt": "07900990903",
            "qDataBag.FieldRegion": "Gwent",
            "qDataBag.FieldTeam": "B-Team",
            "dataModelName": "LM2007",
            "qDataBag.Prem1": "12 Blaise Street",
            "qDataBag.Prem2": "Blaise Hill",
            "qDataBag.Prem3": "Blaiseville",
            "qDataBag.District": "Gwent",
            "qDataBag.PostTown": "Newport",
            "qDataBag.PostCode": "FML134D",
            "qDataBag.UPRN_Latitude": "10020202",
            "qDataBag.UPRN_Longitude": "34949494",
            "qDataBag.priority": "1",
            "qDataBag.DivAddInd": "",
            "qDataBag.Rand": "1",
        }

    @pytest.fixture()
    def service(self) -> TotalmobilePayloadMapperService:
        return TotalmobilePayloadMapperService()

    def test_map_totalmobile_payload_model_returns_a_populated_model(
        self, service: TotalmobilePayloadMapperService, case_data: Dict[str, str]
    ):
        # arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = BlaiseFRSCaseModel(questionnaire_name, case_data)

        # act
        result = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert

        # tla
        assert result.workType == "FRS"
        assert result.skills[0].identity.reference == "FRS"

        # reference
        assert result.identity.reference == "FRS2101.90001"

        # address lines
        assert (
            result.location.addressDetail.addressLine1
            == "12 Blaise Street, Blaise Hill"
        )
        assert result.location.addressDetail.addressLine2 == "Blaiseville"
        assert result.location.addressDetail.addressLine3 == "Gwent"
        assert result.location.addressDetail.addressLine4 == "Newport"

        # address
        assert (
            result.location.address
            == "12 Blaise Street, Blaise Hill, Blaiseville, Newport, FML134D"
        )

        # postcode
        assert result.location.addressDetail.postCode == "FML134D"

        # divided address description
        assert result.description == "Warning Divided Address"

        # lat and long
        assert result.location.addressDetail.coordinates.latitude == "10020202"
        assert result.location.addressDetail.coordinates.longitude == "34949494"

        assert result.origin == ""  # TODO are these mandatory fields?
        assert result.dueDate.end is None  # TODO are these mandatory fields?
        assert result.contact.name is None  # TODO are these mandatory fields?

        assert result.attributes == []

        assert len(result.additionalProperties) == 5

        assert result.additionalProperties[0].name == "tla"
        assert result.additionalProperties[0].value == "FRS"

        assert result.additionalProperties[1].name == "rand"
        assert result.additionalProperties[1].value == "1"

        assert result.additionalProperties[2].name == "fieldRegion"
        assert result.additionalProperties[2].value == "Gwent"

        assert result.additionalProperties[3].name == "fieldTeam"
        assert result.additionalProperties[3].value == "B-Team"

        assert result.additionalProperties[4].name == "postCode"
        assert result.additionalProperties[4].value == "FML134D"

        # mandatory field per BLAIS5-3238 and BLAIS5-3181
        assert result.duration == 15

    @pytest.mark.parametrize(
        "latitude, longitude",
        [
            ("", "10020202"),
            ("10020202", ""),
            (None, "10020202"),
            ("10020202", None),
            ("", ""),
            (None, None),
        ],
    )
    def test_map_totalmobile_payload_model_does_not_populate_lat_and_lon_if_both_are_not_supplied(
        self,
        service: TotalmobilePayloadMapperService,
        case_data: Dict[str, str],
        latitude: str,
        longitude: str,
    ):
        # arrange
        questionnaire_name = "FRS2101"
        case_data["qDataBag.UPRN_Latitude"] = latitude
        case_data["qDataBag.UPRN_Longitude"] = longitude
        questionnaire_case = BlaiseFRSCaseModel(questionnaire_name, case_data)

        # act
        result = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        assert result.location.addressDetail.coordinates.latitude is None
        assert result.location.addressDetail.coordinates.longitude is None

    def test_concatenate_address_returns_a_concatenated_address_as_a_string_when_all_fields_are_populated(
        self, service: TotalmobilePayloadMapperService, case_data: Dict[str, str]
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = BlaiseFRSCaseModel(questionnaire_name, case_data)

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert (
            case.location.address
            == "123 Blaise Street, Blaisville, Upper Blaise, Blaisingdom, BS1 1BS"
        )

    def test_concatenate_address_returns_a_concatenated_address_as_a_string_when_not_all_fields_are_populated(
        self, service: TotalmobilePayloadMapperService, case_data: Dict[str, str]
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = BlaiseFRSCaseModel(questionnaire_name, case_data)

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert case.location.address == "123 Blaise Street, Blaisingdom, BS1 1BS"

    def test_concatenate_address_line1_returns_a_concatenated_address_of_50_characters_when_a_longer_address_is_provided(
        self, service: TotalmobilePayloadMapperService, case_data: Dict[str, str]
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = BlaiseFRSCaseModel(questionnaire_name, case_data)

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert (
            case.location.addressDetail.addressLine1
            == "123 Llanfairpwllgwyngyllgogerychwyrndrobwllllantys"
        )

    def test_concatenate_address_line1_returns_a_concatenated_address_without_a_comma_and_space_when_address_line_2_is_none(
        self, service: TotalmobilePayloadMapperService, case_data: Dict[str, str]
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        case_data["qDataBag.Prem1"] = "123 Blaise Street"
        case_data["qDataBag.Prem2"] = ""
        questionnaire_case = BlaiseFRSCaseModel(questionnaire_name, case_data)

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert case.location.addressDetail.addressLine1 == "123 Blaise Street"

    def test_concatenate_address_line1_returns_a_concatenated_address_without_a_comma_and_space_when_address_line_2_is_an_empty_string(
        self, service: TotalmobilePayloadMapperService, case_data: Dict[str, str]
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        case_data["qDataBag.Prem1"] = "123 Blaise Street"
        case_data["qDataBag.Prem2"] = ""
        questionnaire_case = BlaiseFRSCaseModel(questionnaire_name, case_data)

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert case.location.addressDetail.addressLine1 == "123 Blaise Street"

    def test_location_reference_is_set_to_an_empty_string_if_location_reference_is_none(
        self, service: TotalmobilePayloadMapperService, case_data: Dict[str, str]
    ):
        # arrange
        questionnaire_name = "FRS2101"
        case_data["qDataBag.UPRN"] = ""
        questionnaire_case = BlaiseFRSCaseModel(questionnaire_name, case_data)

        # act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        assert case.location.reference is ""
