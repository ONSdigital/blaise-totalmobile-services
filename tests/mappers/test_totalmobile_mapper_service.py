
from typing import Dict
from unittest.mock import Mock
import pytest
from client.bus import Uac
from models.blaise.questionnaire_uac_model import QuestionnaireUacModel
from models.totalmobile.totalmobile_outgoing_create_job_payload_model import TotalMobileOutgoingCreateJobPayloadModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.mappers.totalmobile_mapper_service import TotalmobileMapperService
from tests.helpers.get_blaise_case_model_helper import get_populated_case_model


@pytest.fixture()
def mock_uac_service():
    return Mock()

@pytest.fixture()
def service(
        mock_uac_service,
) -> TotalmobileMapperService:
    return TotalmobileMapperService(
        uac_service=mock_uac_service,
    )

#lms
def test_map_totalmobile_job_models_maps_the_correct_list_of_models(
            mock_uac_service, service: TotalmobileMapperService
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"

        case_data = [
            get_populated_case_model(
                case_id="10010", outcome_code=110, field_region="region1"
            ),
            get_populated_case_model(
                case_id="10020", outcome_code=120, field_region="region2"
            ),
            get_populated_case_model(
                case_id="10030", outcome_code=130, field_region="region3"
            ),
        ]

        uac_data_dictionary: Dict[str, Uac] = {
            "10010": {
                "instrument_name": "OPN2101A",
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
                "instrument_name": "OPN2101A",
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

        questionnaire_uac_model = QuestionnaireUacModel.import_uac_data(uac_data_dictionary)
        mock_uac_service.get_questionnaire_uac_model.return_value = questionnaire_uac_model

        world_model = TotalmobileWorldModel(
            worlds=[
                World(region="region1", id="3fa85f64-5717-4562-b3fc-2c963f66afa6"),
                World(region="region2", id="3fa85f64-5717-4562-b3fc-2c963f66afa7"),
                World(region="region3", id="3fa85f64-5717-4562-b3fc-2c963f66afa9"),
            ]
        )

        # act
        result = service.map_totalmobile_create_job_models(
            questionnaire_name=questionnaire_name, cases=case_data, world_model=world_model
        )

        # assert
        assert len(result) == 3

        assert result[0].questionnaire == "LMS2101_AA1"
        assert result[0].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa6"
        assert result[0].case_id == "10010"
        assert (
                result[0].payload
                == TotalMobileOutgoingCreateJobPayloadModel.import_case(
            questionnaire_name,
            case_data[0],
            questionnaire_uac_model.get_uac_chunks("10010"),
        ).to_payload()
        )
        assert result[0].payload["description"].startswith("UAC: 8175 4725 3990")

        assert result[1].questionnaire == "LMS2101_AA1"
        assert result[1].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        assert result[1].case_id == "10020"
        assert (
                result[1].payload
                == TotalMobileOutgoingCreateJobPayloadModel.import_case(
            questionnaire_name,
            case_data[1],
            questionnaire_uac_model.get_uac_chunks("10020"),
        ).to_payload()
        )
        assert result[1].payload["description"].startswith("UAC: 4175 5725 6990")

        assert result[2].questionnaire == "LMS2101_AA1"
        assert result[2].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa9"
        assert result[2].case_id == "10030"
        assert (
                result[2].payload
                == TotalMobileOutgoingCreateJobPayloadModel.import_case(
            questionnaire_name,
            case_data[2],
            questionnaire_uac_model.get_uac_chunks("10030"),
        ).to_payload()
        )
        assert result[2].payload["description"].startswith("UAC: \nDue Date")