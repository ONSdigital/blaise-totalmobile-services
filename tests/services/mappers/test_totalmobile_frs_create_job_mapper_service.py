from unittest.mock import Mock

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
from services.create.mappers.totalmobile_payload_mapper_service import (
    TotalmobilePayloadMapperService,
)
from tests.helpers.frs_case_model_helper import get_frs_populated_case_model
from tests.helpers.totalmobile_payload_helper import frs_totalmobile_payload_helper


class TestTotalmobileFRSCreateJobMapping:
    @pytest.fixture()
    def payload_mapper(self) -> TotalmobilePayloadMapperService:
        return TotalmobilePayloadMapperService()

    @pytest.fixture()
    def service(self, payload_mapper) -> TotalmobileCreateJobMapperService:
        return TotalmobileCreateJobMapperService(payload_mapper)

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
