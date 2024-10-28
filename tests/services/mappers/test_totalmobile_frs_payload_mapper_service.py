from datetime import datetime

import pytest

from services.create.mappers.totalmobile_payload_mapper_service import (
    TotalmobilePayloadMapperService,
)
from tests.helpers.blaise_case_model_helper import BlaiseCaseModelHelper


class TestTotalmobileFRSPayloadMapping:
    @pytest.fixture()
    def service(self) -> TotalmobilePayloadMapperService:
        return TotalmobilePayloadMapperService()

    def test_map_totalmobile_payload_model_returns_a_populated_model(
        self,
        service: TotalmobilePayloadMapperService,
    ):
        # arrange
        questionnaire_name = "FRS2101"
        case_id = "90001"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_frs_create_case_model(
            questionnaire_name=questionnaire_name,
            case_id=case_id,
            divided_address="1",
            start_date="01-01-2021",
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
            == "12 Blaise Street, Blaise Hill, Blaiseville, Newport, cf99rsd"
        )

        # postcode
        assert result.location.addressDetail.postCode == "cf99rsd"

        # divided address description
        assert (
            result.description == f"Warning - Divided Address\nStart date: 01-01-2021"
        )

        # lat and long
        assert result.location.addressDetail.coordinates.latitude == "10020202"
        assert result.location.addressDetail.coordinates.longitude == "34949494"

        # contact name per BLAIS5-4479
        assert result.contact.name == "cf99rsd"

        # origin per BLAIS5-4474
        assert result.origin == "ONS"

        # due date per BLAIS5-4348
        assert result.dueDate.end == datetime(2024, 1, 31, 0, 0)

        # misc
        assert result.attributes == []

        assert len(result.additionalProperties) == 5

        assert result.additionalProperties[0].name == "tla"
        assert result.additionalProperties[0].value == "FRS"

        assert result.additionalProperties[1].name == "rand"
        assert result.additionalProperties[1].value == "1"

        assert result.additionalProperties[2].name == "fieldRegion"
        assert result.additionalProperties[2].value == "Region 1"
        assert result.additionalProperties[2].value == "Region 1"

        assert result.additionalProperties[3].name == "fieldTeam"
        assert result.additionalProperties[3].value == "B-Team"

        assert result.additionalProperties[4].name == "postCode"
        assert result.additionalProperties[4].value == "cf99rsd"

        # mandatory field per BLAIS5-3238 and BLAIS5-3181
        assert result.duration == 15

    def test_map_totalmobile_payload_model_returns_a_payload_with_valid_description_without_warning_if_divided_address_is_zero(
        self,
        service: TotalmobilePayloadMapperService,
    ):
        # arrange
        questionnaire_name = "FRS2101"
        case_id = "90001"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_frs_create_case_model(
            questionnaire_name=questionnaire_name,
            case_id=case_id,
            divided_address="0",
            start_date="01-01-2021",
        )

        # act
        result = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        # divided address description
        assert result.description == f"Start date: 01-01-2021"

    def test_map_totalmobile_payload_model_returns_a_payload_with_start_date_in_description_if_divided_address_is_not_1_or_0(
        self,
        service: TotalmobilePayloadMapperService,
    ):
        # arrange
        questionnaire_name = "FRS2101"
        case_id = "90001"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_frs_create_case_model(
            questionnaire_name=questionnaire_name,
            case_id=case_id,
            divided_address="foo",
        )

        # act
        result = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        # divided address description
        assert result.description == "Start date: 01-01-2024"

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
        latitude: str,
        longitude: str,
    ):
        # arrange
        questionnaire_name = "FRS2101"
        case_id = "10010"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_frs_create_case_model(
            questionnaire_name=questionnaire_name,
            case_id=case_id,
            latitude=latitude,
            longitude=longitude,
        )

        # act
        result = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        assert result.location.addressDetail.coordinates.latitude is None
        assert result.location.addressDetail.coordinates.longitude is None

    def test_concatenate_address_returns_a_concatenated_address_as_a_string_when_all_fields_are_populated(
        self,
        service: TotalmobilePayloadMapperService,
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_frs_create_case_model(
            questionnaire_name=questionnaire_name,
            address_line1="123 Blaise Street",
            address_line2="Blaisville",
            address_line3="Upper Blaise",
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
        self,
        service: TotalmobilePayloadMapperService,
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_frs_create_case_model(
            questionnaire_name=questionnaire_name,
            address_line1="123 Blaise Street",
            address_line2="",
            address_line3="",
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
        self,
        service: TotalmobilePayloadMapperService,
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_frs_create_case_model(
            questionnaire_name=questionnaire_name,
            address_line1="123 Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch",
            address_line2="Ynys Môn",
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
        self,
        service: TotalmobilePayloadMapperService,
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_frs_create_case_model(
            questionnaire_name=questionnaire_name,
            address_line1="123 Blaise Street",
            address_line2=None,  # type: ignore
        )

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert case.location.addressDetail.addressLine1 == "123 Blaise Street"

    def test_concatenate_address_line1_returns_a_concatenated_address_without_a_comma_and_space_when_address_line_2_is_an_empty_string(
        self,
        service: TotalmobilePayloadMapperService,
    ):
        # Arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_frs_create_case_model(
            questionnaire_name=questionnaire_name,
            address_line1="123 Blaise Street",
            address_line2="",
        )

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert case.location.addressDetail.addressLine1 == "123 Blaise Street"

    def test_location_reference_is_set_to_an_empty_string_if_location_reference_is_none(
        self,
        service: TotalmobilePayloadMapperService,
    ):
        # arrange
        questionnaire_name = "FRS2101"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_frs_create_case_model(
            questionnaire_name=questionnaire_name, reference=None  # type: ignore
        )

        # act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        assert case.location.reference is ""
