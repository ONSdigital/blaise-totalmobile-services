from datetime import datetime

import pytest

from models.create.blaise.questionnaire_uac_model import UacChunks
from services.create.mappers.totalmobile_payload_mapper_service import (
    TotalmobilePayloadMapperService,
)
from tests.helpers.blaise_case_model_helper import BlaiseCaseModelHelper


class TestTotalmobileLMSPayloadMapping:
    @pytest.fixture()
    def service(self) -> TotalmobilePayloadMapperService:
        return TotalmobilePayloadMapperService()

    def test_map_totalmobile_payload_model_returns_a_populated_model(
        self, service: TotalmobilePayloadMapperService
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        uac_chunks = UacChunks(uac1="3456", uac2="3453", uac3="4546")
        questionnaire_case = BlaiseCaseModelHelper.get_populated_lms_create_case_model(
            questionnaire_name=questionnaire_name,
            case_id="90001",
            uac_chunks=uac_chunks,
        )

        # act
        result = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        assert result.identity.reference == "LMS2101-AA1.90001"
        assert result.description == (
            "UAC: 3456 3453 4546\n"
            "Due Date: 31/01/2023\n"
            "Study: LMS2101_AA1\n"
            "Case ID: 90001\n"
            "Wave: 1"
        )
        assert result.origin == "ONS"
        assert result.duration == 15
        assert result.workType == "LMS"
        assert result.skills[0].identity.reference == "LMS"
        assert result.dueDate.end == datetime(2023, 1, 31)
        assert (
            result.location.addressDetail.addressLine1
            == "12 Blaise Street, Blaise Hill"
        )
        assert result.location.addressDetail.addressLine2 == "Blaiseville"
        assert result.location.addressDetail.addressLine3 == "Gwent"
        assert result.location.addressDetail.addressLine4 == "Newport"
        assert result.location.addressDetail.postCode == "cf99rsd"
        assert result.location.addressDetail.coordinates.latitude == "10020202"
        assert result.location.addressDetail.coordinates.longitude == "34949494"
        assert result.contact.name == "cf99rsd"

        assert len(result.attributes) == 3

        assert result.attributes[0].name == "Region"
        assert result.attributes[0].value == "Region 1"

        assert result.attributes[1].name == "Team"
        assert result.attributes[1].value == "B-Team"

        assert result.attributes[2].name == "LAUA"
        assert result.attributes[2].value == "Loco"

        assert len(result.additionalProperties) == 10

        assert result.additionalProperties[0].name == "surveyName"
        assert result.additionalProperties[0].value == "LM2007"

        assert result.additionalProperties[1].name == "tla"
        assert result.additionalProperties[1].value == "LMS"

        assert result.additionalProperties[2].name == "wave"
        assert result.additionalProperties[2].value == "1"

        assert result.additionalProperties[3].name == "priority"
        assert result.additionalProperties[3].value == "1"

        assert result.additionalProperties[4].name == "fieldRegion"
        assert result.additionalProperties[4].value == "Region 1"

        assert result.additionalProperties[5].name == "fieldTeam"
        assert result.additionalProperties[5].value == "B-Team"

        assert result.additionalProperties[6].name == "postCode"
        assert result.additionalProperties[6].value == "cf99rsd"

        assert result.additionalProperties[7].name == "uac1"
        assert result.additionalProperties[7].value == "3456"

        assert result.additionalProperties[8].name == "uac2"
        assert result.additionalProperties[8].value == "3453"

        assert result.additionalProperties[9].name == "uac3"
        assert result.additionalProperties[9].value == "4546"

    def test_map_totalmobile_payload_model_returns_a_model_with_no_uac_additional_properties_if_no_uacs_are_set_for_an_lms_case(
        self, service: TotalmobilePayloadMapperService
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_lms_create_case_model(
            questionnaire_name=questionnaire_name, uac_chunks=None
        )

        # act
        result = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        for additional_property in result.additionalProperties:
            assert additional_property.name.startswith("uac") is False

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
        questionnaire_name = "LMS2101_AA1"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_lms_create_case_model(
            questionnaire_name=questionnaire_name,
            latitude=latitude,
            longitude=longitude,
            uac_chunks=None,
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
        questionnaire_name = "LMS2201_AA1"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_lms_create_case_model(
            questionnaire_name=questionnaire_name, uac_chunks=None
        )

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert (
            case.location.address
            == "12 Blaise Street, Blaise Hill, Blaiseville, Newport, cf99rsd"
        )

    def test_concatenate_address_returns_a_concatenated_address_as_a_string_when_not_all_fields_are_populated(
        self, service: TotalmobilePayloadMapperService
    ):
        # Arrange
        questionnaire_name = "LMS2201_AA1"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_lms_create_case_model(
            questionnaire_name=questionnaire_name,
            address_line1="12 Blaise Street",
            address_line2="",
            address_line3="",
            town="Newport",
            postcode="cf99rsd",
            uac_chunks=None,
        )

        # Act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # Assert
        assert case.location.address == "12 Blaise Street, Newport, cf99rsd"

    def test_concatenate_address_line1_returns_a_concatenated_address_of_50_characters_when_a_longer_address_is_provided(
        self, service: TotalmobilePayloadMapperService
    ):
        # Arrange
        questionnaire_name = "LMS2201_AA1"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_lms_create_case_model(
            questionnaire_name=questionnaire_name,
            address_line1="123 Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch",
            address_line2="Ynys Môn",
            uac_chunks=None,
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
        questionnaire_name = "LMS2201_AA1"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_lms_create_case_model(
            questionnaire_name=questionnaire_name,
            address_line1="123 Blaise Street",
            address_line2=None,  # type: ignore
            uac_chunks=None,
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
        questionnaire_name = "LMS2201_AA1"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_lms_create_case_model(
            questionnaire_name=questionnaire_name,
            address_line1="123 Blaise Street",
            address_line2="",
            uac_chunks=None,
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
        questionnaire_name = "LMS2201_AA1"
        questionnaire_case = BlaiseCaseModelHelper.get_populated_lms_create_case_model(
            questionnaire_name=questionnaire_name,
            reference=None,  # type: ignore
            uac_chunks=None,
        )

        # act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        assert case.location.reference is ""
