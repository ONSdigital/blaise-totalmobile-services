from typing import Dict, Optional

import pytest

from client.bus import Uac
from models.blaise.blaise_frs_case_information_model import (
    BlaiseFRSCaseInformationModel,
)
from models.blaise.blaise_lms_case_information_model import (
    BlaiseLMSCaseInformationModel,
)
from models.blaise.questionnaire_uac_model import QuestionnaireUacModel, UacChunks
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel, World
from services.mappers.totalmobile_mapper_service import TotalmobileMapperService
from tests.helpers.get_blaise_frs_case_model_helper import get_frs_populated_case_model
from tests.helpers.get_blaise_lms_case_model_helper import get_populated_case_model


@pytest.fixture()
def service() -> TotalmobileMapperService:
    return TotalmobileMapperService()


class TestMapTotalmobileJobModelsForLMS:
    def get_questionnaire_uac_model(self) -> QuestionnaireUacModel:
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

        questionnaire_uac_model = QuestionnaireUacModel.import_uac_data(
            uac_data_dictionary
        )
        return questionnaire_uac_model

    @staticmethod
    def totalmobile_payload_helper(
        questionnaire_name: str,
        case: BlaiseLMSCaseInformationModel,
        uac_chunks: Optional[UacChunks],
    ) -> dict[str, object]:

        payload_dictionary = {
            "additionalProperties": [
                {"name": "surveyName", "value": case.data_model_name},
                {"name": "tla", "value": case.tla},
                {"name": "wave", "value": f"{case.wave}"},
                {"name": "priority", "value": case.priority},
                {"name": "fieldRegion", "value": case.field_region},
                {"name": "fieldTeam", "value": case.field_team},
                {"name": "postCode", "value": case.address_details.address.postcode},
            ],
            "attributes": [
                {"name": "Region", "value": case.field_region},
                {"name": "Team", "value": case.field_team},
            ],
            "contact": {"name": case.address_details.address.postcode},
            "description": f'UAC: {uac_chunks.formatted_chunks() if uac_chunks is not None else ""}\n'
            f'Due Date: {case.wave_com_dte.strftime("%d/%m/%Y") if case.wave_com_dte is not None else ""}\n'
            f"Study: {questionnaire_name}\n"
            f"Case ID: {case.case_id}\n"
            f"Wave: {case.wave}",
            "dueDate": {
                "end": case.wave_com_dte.strftime("%Y-%m-%d")
                if case.wave_com_dte is not None
                else ""
            },
            "duration": 15,
            "identity": {
                "reference": f'{questionnaire_name.replace("_", "-")}.{case.case_id}'
            },
            "location": {
                "address": "12 Blaise Street, Blaise Hill, Blaiseville, Newport, "
                f"{case.address_details.address.postcode}",
                "addressDetail": {
                    "addressLine1": "12 Blaise Street, Blaise Hill",
                    "addressLine2": "Blaiseville",
                    "addressLine3": "Gwent",
                    "addressLine4": "Newport",
                    "coordinates": {"latitude": "10020202", "longitude": "34949494"},
                    "postCode": case.address_details.address.postcode,
                },
                "reference": case.address_details.reference,
            },
            "origin": "ONS",
            "skills": [{"identity": {"reference": case.tla}}],
            "workType": case.tla,
        }

        if uac_chunks is not None:
            payload_dictionary["additionalProperties"].append({"name": "uac1", "value": uac_chunks.uac1})  # type: ignore
            payload_dictionary["additionalProperties"].append({"name": "uac2", "value": uac_chunks.uac2})  # type: ignore
            payload_dictionary["additionalProperties"].append({"name": "uac3", "value": uac_chunks.uac3})  # type: ignore

        return payload_dictionary

    def test_map_totalmobile_job_models_maps_the_correct_list_of_models(
        self, service: TotalmobileMapperService
    ):
        # arrange
        questionnaire_name = "LMS2101_AA1"
        questionnaire_uac_model = self.get_questionnaire_uac_model()

        case_data = [
            get_populated_case_model(
                case_id="10010",
                outcome_code=110,
                field_region="region1",
                uac_chunks=questionnaire_uac_model.get_uac_chunks("10010"),
                postcode="AB12 3CD",
            ),
            get_populated_case_model(
                case_id="10020",
                outcome_code=120,
                field_region="region2",
                uac_chunks=questionnaire_uac_model.get_uac_chunks("10020"),
                postcode="EF45 6GH",
            ),
            get_populated_case_model(
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
        assert result[0].payload == self.totalmobile_payload_helper(
            questionnaire_name=questionnaire_name,
            case=case_data[0],
            uac_chunks=questionnaire_uac_model.get_uac_chunks(case_data[0].case_id),
        )
        assert result[0].payload["description"].startswith("UAC: 8175 4725 3990")

        assert result[1].questionnaire == "LMS2101_AA1"
        assert result[1].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        assert result[1].case_id == "10020"
        assert result[1].payload == self.totalmobile_payload_helper(
            questionnaire_name=questionnaire_name,
            case=case_data[1],
            uac_chunks=questionnaire_uac_model.get_uac_chunks(case_data[1].case_id),
        )
        assert result[1].payload["description"].startswith("UAC: 4175 5725 6990")

        assert result[2].questionnaire == "LMS2101_AA1"
        assert result[2].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa9"
        assert result[2].case_id == "10030"
        assert result[2].payload == self.totalmobile_payload_helper(
            questionnaire_name=questionnaire_name, case=case_data[2], uac_chunks=None
        )
        assert result[2].payload["description"].startswith("UAC: \nDue Date")


class TestMapTotalmobileJobModelsForFRS:
    @staticmethod
    def totalmobile_payload_helper(
        questionnaire_name: str, case: BlaiseFRSCaseInformationModel
    ) -> Dict[str, object]:

        due_date = (
            case.wave_com_dte.strftime("%d/%m/%Y")
            if case.wave_com_dte is not None
            else ""
        )

        payload_dictionary = {
            "additionalProperties": [
                {"name": "surveyName", "value": case.data_model_name},
                {"name": "tla", "value": case.tla},
                {"name": "priority", "value": case.priority},
                {"name": "fieldRegion", "value": case.field_region},
                {"name": "fieldTeam", "value": case.field_team},
                {"name": "postCode", "value": case.address_details.address.postcode},
            ],
            "attributes": [
                {"name": "Region", "value": case.field_region},
                {"name": "Team", "value": case.field_team},
            ],
            "contact": {"name": case.address_details.address.postcode},
            "description": (
                "Warning Divided Address"
                if case.divided_address_indicator == "1"
                else ""
            ),
            "dueDate": {"end": due_date},
            "duration": 15,
            "identity": {
                "reference": f'{questionnaire_name.replace("_", "-")}.{case.case_id}'
            },
            "location": {
                "address": "12 Blaise Street, Blaise Hill, Blaiseville, Newport, "
                f"{case.address_details.address.postcode}",
                "addressDetail": {
                    "addressLine1": "12 Blaise Street, Blaise Hill",
                    "addressLine2": "Blaiseville",
                    "addressLine3": "Gwent",
                    "addressLine4": "Newport",
                    "coordinates": {"latitude": "10020202", "longitude": "34949494"},
                    "postCode": f"{case.address_details.address.postcode}",
                },
                "reference": case.address_details.reference,
            },
            "origin": "ONS",
            "skills": [{"identity": {"reference": case.tla}}],
            "workType": case.tla,
        }

        return payload_dictionary

    def test_map_totalmobile_job_models_maps_the_correct_list_of_models(
        self, service: TotalmobileMapperService
    ):
        # arrange
        questionnaire_name = "FRS2101"

        case_data = [
            get_frs_populated_case_model(
                case_id="10010",
                field_region="region1",
                postcode="AB12 3CD",
                divided_address_indicator="1",
            ),
            get_frs_populated_case_model(
                case_id="10020",
                field_region="region2",
                postcode="EF45 6GH",
                divided_address_indicator="0",
            ),
            get_frs_populated_case_model(
                case_id="10030",
                field_region="region3",
                postcode="IJ78 9KL",
                divided_address_indicator="",
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
        assert result[0].payload["description"] == "Warning Divided Address"
        assert result[0].payload == self.totalmobile_payload_helper(
            questionnaire_name=questionnaire_name, case=case_data[0]
        )

        assert result[1].questionnaire == "FRS2101"
        assert result[1].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa7"
        assert result[1].case_id == "10020"
        assert result[1].payload["description"] == ""
        assert result[1].payload == self.totalmobile_payload_helper(
            questionnaire_name=questionnaire_name, case=case_data[1]
        )

        assert result[2].questionnaire == "FRS2101"
        assert result[2].world_id == "3fa85f64-5717-4562-b3fc-2c963f66afa9"
        assert result[2].case_id == "10030"
        assert result[2].payload["description"] == ""
        assert result[2].payload == self.totalmobile_payload_helper(
            questionnaire_name=questionnaire_name, case=case_data[2]
        )
