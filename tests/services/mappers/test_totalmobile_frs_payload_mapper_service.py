from datetime import datetime

import pytest

from services.create.mappers.totalmobile_payload_mapper_service import (
    TotalmobilePayloadMapperService,
)
from tests.helpers.frs_case_model_helper import get_frs_populated_case_model


class TestTotalmobileFRSPayloadMapping:
    @pytest.fixture()
    def service(self) -> TotalmobilePayloadMapperService:
        return TotalmobilePayloadMapperService()

    def test_map_totalmobile_payload_model_returns_a_populated_model(
        self, service: TotalmobilePayloadMapperService
    ):
        # arrange
        questionnaire_name = "FRS2101"

        questionnaire_case = get_frs_populated_case_model(
            case_id="90001",
            data_model_name="FRS2101",
            address_line_1="12 Blaise Street",
            address_line_2="Blaise Hill",
            address_line_3="Blaiseville",
            county="Gwent",
            town="Newport",
            postcode="FML134D",
            latitude="10020202",
            longitude="34949494",
            priority="1",
            field_region="Gwent",
            field_team="B-Team",
            wave_com_dte=datetime(2023, 1, 31),
            divided_address_indicator="1",
        )

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
        self, service: TotalmobilePayloadMapperService, latitude: str, longitude: str
    ):
        # arrange
        questionnaire_name = "FRS2101"

        questionnaire_case = get_frs_populated_case_model(
            latitude=latitude, longitude=longitude
        )

        # act
        result = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        assert result.location.addressDetail.coordinates.latitude is None
        assert result.location.addressDetail.coordinates.longitude is None

    def test_concatenate_address_returns_a_concatenated_address_as_a_string_when_all_fields_are_populated(
        self, service: TotalmobilePayloadMapperService
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = get_frs_populated_case_model(
            questionnaire_name="FRS2101",
            case_id="1234",
            address_line_1="123 Blaise Street",
            address_line_2="Blaisville",
            address_line_3="Upper Blaise",
            town="Blaisingdom",
            postcode="BS1 1BS",
        )

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
        self, service: TotalmobilePayloadMapperService
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = get_frs_populated_case_model(
            questionnaire_name="FRS2101",
            case_id="1234",
            address_line_1="123 Blaise Street",
            address_line_2="",
            address_line_3=None,
            town="Blaisingdom",
            postcode="BS1 1BS",
        )

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert case.location.address == "123 Blaise Street, Blaisingdom, BS1 1BS"

    def test_concatenate_address_line1_returns_a_concatenated_address_of_50_characters_when_a_longer_address_is_provided(
        self, service: TotalmobilePayloadMapperService
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = get_frs_populated_case_model(
            questionnaire_name="FRS2101",
            case_id="1234",
            address_line_1="123 Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch",
            address_line_2="Ynys Môn",
        )

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
        self, service: TotalmobilePayloadMapperService
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = get_frs_populated_case_model(
            questionnaire_name="FRS2101",
            case_id="1234",
            address_line_1="123 Blaise Street",
            address_line_2=None,
        )

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert case.location.addressDetail.addressLine1 == "123 Blaise Street"

    def test_concatenate_address_line1_returns_a_concatenated_address_without_a_comma_and_space_when_address_line_2_is_an_empty_string(
        self, service: TotalmobilePayloadMapperService
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = get_frs_populated_case_model(
            questionnaire_name="FRS2101",
            case_id="1234",
            address_line_1="123 Blaise Street",
            address_line_2="",
        )

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert case.location.addressDetail.addressLine1 == "123 Blaise Street"

    def test_location_reference_is_set_to_an_empty_string_if_location_reference_is_none(
        self, service: TotalmobilePayloadMapperService
    ):
        # arrange
        questionnaire_name = "FRS2101"

        questionnaire_case = get_frs_populated_case_model(
            questionnaire_name="FRS2101", reference=None
        )

        # act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        assert case.location.reference is ""
