import pytest

from models.common.totalmobile.totalmobile_world_model import (
    TotalmobileWorldModel,
    World,
)
from models.create.blaise.blaise_frs_create_case_model import BlaiseFRSCreateCaseModel
from models.create.totalmobile.totalmobile_create_job_model import (
    TotalmobileCreateJobModelRequestJson,
)
from services.create.mappers.totalmobile_create_job_mapper_service import (
    TotalmobileCreateJobMapperService,
)
from services.create.mappers.totalmobile_payload_mapper_service import (
    TotalmobilePayloadMapperService,
)
from tests.helpers.blaise_case_model_helper import BlaiseCaseModelHelper
from tests.helpers.totalmobile_payload_helper import frs_totalmobile_payload_helper


class TestTotalmobileFRSCreateJobMapping:
    def get_case(
        self,
        questionnaire_name: str,
        case_id: str,
        field_region: str,
        postcode: str,
    ) -> BlaiseFRSCreateCaseModel:
        case_helper = BlaiseCaseModelHelper()
        return case_helper.get_populated_frs_create_case_model(
            questionnaire_name=questionnaire_name,
            case_id=case_id,
            field_region=field_region,
            postcode=postcode,
        )

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
        case1 = self.get_case(
            questionnaire_name=questionnaire_name,
            case_id="10010",
            field_region="region1",
            postcode="AB12 3CD",
        )
        case2 = self.get_case(
            questionnaire_name=questionnaire_name,
            case_id="10020",
            field_region="region2",
            postcode="EF45 6GH",
        )
        case3 = self.get_case(
            questionnaire_name=questionnaire_name,
            case_id="10030",
            field_region="region3",
            postcode="IJ78 9KL",
        )

        cases = [case1, case2, case3]

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
            cases=cases,
            world_model=world_model,
        )

        # assert
        assert len(result) == 3

        assert result[0].questionnaire == "FRS2101"
        assert result[0].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        assert result[0].case_id == "10010"
        assert result[0].payload == frs_totalmobile_payload_helper(
            questionnaire_name=questionnaire_name,
            case=cases[0],
        )
        assert result[0].payload["description"] == ""

        assert result[1].questionnaire == "FRS2101"
        assert result[1].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        assert result[1].case_id == "10020"
        assert result[1].payload == frs_totalmobile_payload_helper(
            questionnaire_name=questionnaire_name,
            case=cases[1],
        )
        assert result[1].payload["description"] == ""

        assert result[2].questionnaire == "FRS2101"
        assert result[2].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa9"
        assert result[2].case_id == "10030"
        assert result[2].payload == frs_totalmobile_payload_helper(
            questionnaire_name=questionnaire_name, case=cases[2]
        )
        assert result[2].payload["description"] == ""

    def test_map_totalmobile_job_model_maps_the_correct_model(
        self, service: TotalmobileCreateJobMapperService
    ):
        # arrange
        questionnaire_name = "FRS2101"
        case = self.get_case(
            questionnaire_name=questionnaire_name,
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
        case = self.get_case(
            questionnaire_name=questionnaire_name,
            case_id=case_id,
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
