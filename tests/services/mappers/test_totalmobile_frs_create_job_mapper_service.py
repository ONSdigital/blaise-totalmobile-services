from datetime import datetime

import pytest

from models.common.totalmobile.totalmobile_world_model import (
    TotalmobileWorldModel,
    World,
)
from models.create.totalmobile.totalmobile_create_job_model import (
    TotalmobileCreateJobModelRequestJson,
)
from services.create.mappers.totalmobile_create_job_mapper_service import (
    TotalmobileCreateJobMapperService,
)
from tests.helpers.frs_case_model_helper import get_frs_populated_case_model
from tests.helpers.totalmobile_payload_helper import frs_totalmobile_payload_helper


class TestTotalmobileFrsCreateJobMapping:
    @pytest.fixture()
    def service(self) -> TotalmobileCreateJobMapperService:
        return TotalmobileCreateJobMapperService()

    def test_map_totalmobile_job_models_maps_the_correct_list_of_models(
        self, service: TotalmobileCreateJobMapperService
    ):
        # arrange
        questionnaire_name = "FRS2101"

        case_data = [
            get_frs_populated_case_model(
                case_id="10010",
                field_region="region1",
                postcode="AB12 3CD",
            ),
            get_frs_populated_case_model(
                case_id="10020",
                field_region="region2",
                postcode="EF45 6GH",
            ),
            get_frs_populated_case_model(
                case_id="10030",
                field_region="region3",
                postcode="IJ78 9KL",
            ),
        ]

        world_model = TotalmobileWorldModel(
            worlds=[
                World(region="region1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
                World(region="region2", id="3fa85f64-5717-4562-b3fc-2c963f66afa7"),
                World(region="region3", id="3fa85f64-5717-4562-b3fc-2c963f66afa9"),
            ]
        )

        # act
        result = service.map_totalmobile_create_job_models(
            questionnaire_name=questionnaire_name,
            cases=case_data,
            world_model=world_model,
        )

        # assert
        assert len(result) == 3

        assert result[0].questionnaire == "FRS2101"
        assert result[0].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        assert result[0].case_id == "10010"
        assert result[0].payload == frs_totalmobile_payload_helper(
            questionnaire_name=questionnaire_name,
            case=case_data[0],
        )
        assert result[0].payload["description"] == ""

        assert result[1].questionnaire == "FRS2101"
        assert result[1].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        assert result[1].case_id == "10020"
        assert result[1].payload == frs_totalmobile_payload_helper(
            questionnaire_name=questionnaire_name,
            case=case_data[1],
        )
        assert result[1].payload["description"] == ""

        assert result[2].questionnaire == "FRS2101"
        assert result[2].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa9"
        assert result[2].case_id == "10030"
        assert result[2].payload == frs_totalmobile_payload_helper(
            questionnaire_name=questionnaire_name, case=case_data[2]
        )
        assert result[2].payload["description"] == ""

    def test_map_totalmobile_job_model_maps_the_correct_model(
        self, service: TotalmobileCreateJobMapperService
    ):
        # arrange
        questionnaire_name = "FRS2101"

        case = get_frs_populated_case_model(
            case_id="10010",
            field_region="region1",
            postcode="AB12 3CD",
        )

        world_model = TotalmobileWorldModel(
            worlds=[
                World(region="region1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            ]
        )

        # act
        result = service.map_totalmobile_create_job_model(
            questionnaire_name=questionnaire_name,
            case=case,
            world_model=world_model,
        )

        # assert
        assert result.questionnaire == "FRS2101"
        assert result.world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        assert result.case_id == "10010"
        assert result.payload == frs_totalmobile_payload_helper(
            questionnaire_name=questionnaire_name,
            case=case,
        )
        assert result.payload["description"] == ""

    def test_map_totalmobile_create_job_model_from_json_maps_the_correct_model(
        self, service: TotalmobileCreateJobMapperService
    ):
        # arrange
        questionnaire_name = "FRS2101"
        world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        case_id = "10010"
        case = get_frs_populated_case_model(
            case_id="10010",
            field_region="region1",
            postcode="AB12 3CD",
        )

        payload = frs_totalmobile_payload_helper(questionnaire_name, case)

        request_json = TotalmobileCreateJobModelRequestJson(
            questionnaire=questionnaire_name,
            case_id=case_id,
            world_id=world_id,
            payload=payload,  # type: ignore
        )

        # act
        result = service.map_totalmobile_create_job_model_from_json(request_json)

        # assert
        assert result.questionnaire == questionnaire_name
        assert result.case_id == case_id
        assert result.world_id == world_id
        assert result.payload == payload

    def test_map_totalmobile_payload_model_returns_a_populated_model(
        self, service: TotalmobileCreateJobMapperService
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
        assert result.additionalProperties[1].name == "tla"
        assert result.additionalProperties[1].value == "FRS"
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
        assert result.additionalProperties[5].name == "postCode"
        assert result.additionalProperties[5].value == "FML134D"

        # divided address description
        assert result.description == "Warning Divided Address"

        # rand
        assert result.additionalProperties[6].name == "rand"
        assert result.additionalProperties[6].value == "1"

        # lat and long
        assert result.location.addressDetail.coordinates.latitude == "10020202"
        assert result.location.addressDetail.coordinates.longitude == "34949494"

        # field region
        assert result.additionalProperties[3].name == "fieldRegion"
        assert result.additionalProperties[3].value == "Gwent"

        # field team
        assert result.additionalProperties[4].name == "fieldTeam"
        assert result.additionalProperties[4].value == "B-Team"

        # mandatory field per BLAIS5-3238 and BLAIS5-3181
        assert result.duration == 15

        # TODO
        # LMS fields listed in BLAIS5-3181 but not listed in BLAIS5-4331 for FRS
        assert result.dueDate.end == datetime(2023, 1, 31)
        assert result.contact.name == "FML134D"

        assert result.additionalProperties[0].name == "surveyName"
        assert result.additionalProperties[0].value == "FRS2101"

        assert result.additionalProperties[2].name == "priority"
        assert result.additionalProperties[2].value == "1"

        # Not listed in BLAIS5-3181 or BLAIS5-4331
        assert result.origin == "ONS"

        assert result.attributes[0].name == "Region"
        assert result.attributes[0].value == "Gwent"

        assert result.attributes[1].name == "Team"
        assert result.attributes[1].value == "B-Team"

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
        self, service: TotalmobileCreateJobMapperService, latitude: str, longitude: str
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
        self, service: TotalmobileCreateJobMapperService
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
        self, service: TotalmobileCreateJobMapperService
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
        self, service: TotalmobileCreateJobMapperService
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
        self, service: TotalmobileCreateJobMapperService
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
        self, service: TotalmobileCreateJobMapperService
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
        self, service: TotalmobileCreateJobMapperService
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
