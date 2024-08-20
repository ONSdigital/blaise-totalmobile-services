from datetime import datetime
from typing import Dict

import pytest

from client.bus import Uac
from models.blaise.questionnaire_uac_model import QuestionnaireUacModel, UacChunks
from models.cloud_tasks.totalmobile_create_job_model import (
    TotalmobileCreateJobModelRequestJson,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.mappers.totalmobile_create_job_mapper_service import (
    TotalmobileCreateJobMapperService,
)
from tests.helpers.lms_case_model_helper import get_lms_populated_case_model
from tests.helpers.totalmobile_payload_helper import lms_totalmobile_payload_helper


class TestTotalmobileLmsCreateJobMapping:
    @pytest.fixture()
    def questionnaire_uac_model(self) -> QuestionnaireUacModel:
        uac_data_dictionary: Dict[str, Uac] = {
            "10010": {
                "instrument_name": "LMS2101_AA1",
                "case_id": "10010",
                "uac_chunks": {
                    "uac1": "8175",
                    "uac2": "4725",
                    "uac3": "3990",
                    "uac4": "None",
                },
                "full_uac": "817647263991",
            },
            "10020": {
                "instrument_name": "LMS2101_AA1",
                "case_id": "10020",
                "uac_chunks": {
                    "uac1": "4175",
                    "uac2": "5725",
                    "uac3": "6990",
                    "uac4": "None",
                },
                "full_uac": "417657266991",
            },
        }

        questionnaire_uac_model = QuestionnaireUacModel.import_uac_data(
            uac_data_dictionary
        )
        return questionnaire_uac_model

    @pytest.fixture()
    def service(self) -> TotalmobileCreateJobMapperService:
        return TotalmobileCreateJobMapperService()

    def test_map_totalmobile_job_models_maps_the_correct_list_of_models(
        self, service: TotalmobileCreateJobMapperService, questionnaire_uac_model
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"

        case_data = [
            get_lms_populated_case_model(
                case_id="10010",
                outcome_code=110,
                field_region="region1",
                uac_chunks=questionnaire_uac_model.get_uac_chunks("10010"),
                postcode="AB12 3CD",
            ),
            get_lms_populated_case_model(
                case_id="10020",
                outcome_code=120,
                field_region="region2",
                uac_chunks=questionnaire_uac_model.get_uac_chunks("10020"),
                postcode="EF45 6GH",
            ),
            get_lms_populated_case_model(
                case_id="10030",
                outcome_code=130,
                field_region="region3",
                uac_chunks=questionnaire_uac_model.get_uac_chunks("10030"),
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

        assert result[0].questionnaire == "LMS2101_AA1"
        assert result[0].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        assert result[0].case_id == "10010"
        assert result[0].payload == lms_totalmobile_payload_helper(
            questionnaire_name=questionnaire_name,
            case=case_data[0],
            uac_chunks=questionnaire_uac_model.get_uac_chunks(case_data[0].case_id),
        )
        assert result[0].payload["description"].startswith("UAC: 8175 4725 3990")

        assert result[1].questionnaire == "LMS2101_AA1"
        assert result[1].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        assert result[1].case_id == "10020"
        assert result[1].payload == lms_totalmobile_payload_helper(
            questionnaire_name=questionnaire_name,
            case=case_data[1],
            uac_chunks=questionnaire_uac_model.get_uac_chunks(case_data[1].case_id),
        )
        assert result[1].payload["description"].startswith("UAC: 4175 5725 6990")

        assert result[2].questionnaire == "LMS2101_AA1"
        assert result[2].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa9"
        assert result[2].case_id == "10030"
        assert result[2].payload == lms_totalmobile_payload_helper(
            questionnaire_name=questionnaire_name, case=case_data[2], uac_chunks=None
        )
        assert result[2].payload["description"].startswith("UAC: \nDue Date")

    def test_map_totalmobile_job_model_maps_the_correct_model(
        self, service: TotalmobileCreateJobMapperService, questionnaire_uac_model
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"

        case = get_lms_populated_case_model(
            case_id="10010",
            outcome_code=110,
            field_region="region1",
            uac_chunks=questionnaire_uac_model.get_uac_chunks("10010"),
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

        assert result.questionnaire == "LMS2101_AA1"
        assert result.world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        assert result.case_id == "10010"
        assert result.payload == lms_totalmobile_payload_helper(
            questionnaire_name=questionnaire_name,
            case=case,
            uac_chunks=questionnaire_uac_model.get_uac_chunks(case.case_id),
        )
        assert result.payload["description"].startswith("UAC: 8175 4725 3990")

    def test_map_totalmobile_create_job_model_from_json_maps_the_correct_model(
        self, service: TotalmobileCreateJobMapperService, questionnaire_uac_model
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        world_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        case_id = "10010"
        case = get_lms_populated_case_model(
            case_id="10010",
            outcome_code=110,
            field_region="region1",
            uac_chunks=questionnaire_uac_model.get_uac_chunks("10010"),
            postcode="AB12 3CD",
        )
        payload = lms_totalmobile_payload_helper(
            questionnaire_name,
            case,
            uac_chunks=questionnaire_uac_model.get_uac_chunks(case_id),
        )

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
        questionnaire_name = "LMS2101_AA1"

        questionnaire_case = get_lms_populated_case_model(
            case_id="90001",
            data_model_name="LM2007",
            wave=1,
            address_line_1="12 Blaise Street",
            address_line_2="Blaise Hill",
            address_line_3="Blaiseville",
            county="Gwent",
            town="Newport",
            postcode="FML134D",
            telephone_number_1="07900990901",
            telephone_number_2="07900990902",
            appointment_telephone_number="07900990903",
            outcome_code=301,
            latitude="10020202",
            longitude="34949494",
            priority="1",
            field_region="Gwent",
            field_team="B-Team",
            wave_com_dte=datetime(2023, 1, 31),
            uac_chunks=UacChunks(uac1="3456", uac2="3453", uac3="4546"),
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
        assert result.location.addressDetail.postCode == "FML134D"
        assert result.location.addressDetail.coordinates.latitude == "10020202"
        assert result.location.addressDetail.coordinates.longitude == "34949494"
        assert result.contact.name == "FML134D"

        assert result.attributes[0].name == "Region"
        assert result.attributes[0].value == "Gwent"

        assert result.attributes[1].name == "Team"
        assert result.attributes[1].value == "B-Team"

        assert result.additionalProperties[0].name == "surveyName"
        assert result.additionalProperties[0].value == "LM2007"

        assert result.additionalProperties[1].name == "tla"
        assert result.additionalProperties[1].value == "LMS"

        assert result.additionalProperties[2].name == "wave"
        assert result.additionalProperties[2].value == "1"

        assert result.additionalProperties[3].name == "priority"
        assert result.additionalProperties[3].value == "1"

        assert result.additionalProperties[4].name == "fieldRegion"
        assert result.additionalProperties[4].value == "Gwent"

        assert result.additionalProperties[5].name == "fieldTeam"
        assert result.additionalProperties[5].value == "B-Team"

        assert result.additionalProperties[6].name == "postCode"
        assert result.additionalProperties[6].value == "FML134D"

        assert result.additionalProperties[7].name == "uac1"
        assert result.additionalProperties[7].value == "3456"

        assert result.additionalProperties[8].name == "uac2"
        assert result.additionalProperties[8].value == "3453"

        assert result.additionalProperties[9].name == "uac3"
        assert result.additionalProperties[9].value == "4546"

    def test_map_totalmobile_payload_model_returns_a_model_with_no_uac_additional_properties_if_no_uacs_are_set_for_an_lms_case(
        self, service: TotalmobileCreateJobMapperService
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"

        questionnaire_case = get_lms_populated_case_model(uac_chunks=None)

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
        self, service: TotalmobileCreateJobMapperService, latitude: str, longitude: str
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"

        questionnaire_case = get_lms_populated_case_model(
            latitude=latitude, longitude=longitude, uac_chunks=None
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
        questionnaire_name = "LMS2201_AA1"
        questionnaire_case = get_lms_populated_case_model(
            questionnaire_name="LMS2201_AA1",
            case_id="1234",
            address_line_1="123 Blaise Street",
            address_line_2="Blaisville",
            address_line_3="Upper Blaise",
            town="Blaisingdom",
            postcode="BS1 1BS",
            uac_chunks=None,
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
        questionnaire_name = "LMS2201_AA1"
        questionnaire_case = get_lms_populated_case_model(
            questionnaire_name="LMS2201_AA1",
            case_id="1234",
            address_line_1="123 Blaise Street",
            address_line_2="",
            address_line_3=None,
            town="Blaisingdom",
            postcode="BS1 1BS",
            uac_chunks=None,
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
        questionnaire_name = "LMS2201_AA1"
        questionnaire_case = get_lms_populated_case_model(
            questionnaire_name="LMS2201_AA1",
            case_id="1234",
            address_line_1="123 Llanfairpwllgwyngyllgogerychwyrndrobwllllantysiliogogogoch",
            address_line_2="Ynys Môn",
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
        self, service: TotalmobileCreateJobMapperService
    ):
        # Arrange
        questionnaire_name = "LMS2201_AA1"
        questionnaire_case = get_lms_populated_case_model(
            questionnaire_name="LMS2201_AA1",
            case_id="1234",
            address_line_1="123 Blaise Street",
            address_line_2=None,
            uac_chunks=None,
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
        questionnaire_name = "LMS2201_AA1"
        questionnaire_case = get_lms_populated_case_model(
            questionnaire_name="LMS2201_AA1",
            case_id="1234",
            address_line_1="123 Blaise Street",
            address_line_2="",
            uac_chunks=None,
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
        questionnaire_name = "LMS2101_AA1"

        questionnaire_case = get_lms_populated_case_model(
            questionnaire_name="LMS2201_AA1", reference=None, uac_chunks=None
        )

        # act
        case = service.map_totalmobile_payload_model(
            questionnaire_name, questionnaire_case
        )

        # assert
        assert case.location.reference is ""
