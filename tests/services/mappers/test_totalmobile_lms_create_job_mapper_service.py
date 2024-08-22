from datetime import datetime
from typing import Dict
from unittest.mock import Mock

import pytest

from client.bus import Uac
from models.common.totalmobile.totalmobile_world_model import (
    TotalmobileWorldModel,
    World,
)
from models.create.blaise.questionnaire_uac_model import QuestionnaireUacModel
from models.create.totalmobile.totalmobile_create_job_model import (
    TotalmobileCreateJobModelRequestJson,
)
from services.create.mappers.totalmobile_create_job_mapper_service import (
    TotalmobileCreateJobMapperService,
)
from services.create.mappers.totalmobile_payload_mapper_service import (
    TotalmobilePayloadMapperService,
)
from tests.helpers.lms_case_model_helper import get_lms_populated_case_model
from tests.helpers.totalmobile_payload_helper import lms_totalmobile_payload_helper


class TestTotalmobileLMSCreateJobMapping:
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
    def payload_mapper(self) -> TotalmobilePayloadMapperService:
        return TotalmobilePayloadMapperService()

    @pytest.fixture()
    def service(self, payload_mapper) -> TotalmobileCreateJobMapperService:
        return TotalmobileCreateJobMapperService(payload_mapper)

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
