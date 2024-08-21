from typing import Dict

import pytest

from services.delete.mappers.blaise_delete_case_imapper_service import (
    BlaiseDeleteCaseMapperService,
)


class TestDeleteCaseMapping:
    @pytest.fixture()
    def service(self) -> BlaiseDeleteCaseMapperService:
        return BlaiseDeleteCaseMapperService()

    def test_map_delete_case_information_models_maps_the_correct_list_of_models(
        self, service: BlaiseDeleteCaseMapperService
    ):
        # arrange
        case1_id = "10010"
        case1_outcome_code = 110

        case2_id = "20010"
        case2_outcome_code = 210

        cases = [
            {
                "qiD.Serial_Number": case1_id,
                "hOut": str(case1_outcome_code),
            },
            {
                "qiD.Serial_Number": case2_id,
                "hOut": str(case2_outcome_code),
            },
        ]

        # act
        result = service.map_blaise_delete_case_models(cases)

        # assert
        assert result[0].case_id == case1_id
        assert result[0].outcome_code == case1_outcome_code

        assert result[1].case_id == case2_id
        assert result[1].outcome_code == case2_outcome_code

    @pytest.mark.parametrize(
        "case_id, outcome_code",
        [
            ("10010", 301),
            ("9000", 110),
            ("1002", 210),
        ],
    )
    def test_map_delete_case_information_model_maps_the_correct_model(
        self, service: BlaiseDeleteCaseMapperService, case_id: str, outcome_code: int
    ):
        # arrange
        case = {
            "qiD.Serial_Number": case_id,
            "hOut": str(outcome_code),
        }

        # act
        result = service.map_blaise_delete_case_model(case)

        # assert
        assert result.case_id == case_id
        assert result.outcome_code == outcome_code
