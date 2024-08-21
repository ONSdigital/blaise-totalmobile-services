from typing import Dict, List

from models.delete.blaise_delete_case_information__model import (
    BlaiseDeleteCaseInformationBaseModel,
)
from services.create.mappers.blaise_mapper_base import MapperServiceBase


class BlaiseDeleteCaseMapperService(MapperServiceBase):
    def map_blaise_delete_case_models(
        self, cases: List[Dict[str, str]]
    ) -> list[BlaiseDeleteCaseInformationBaseModel]:
        delete_models = [self.map_blaise_delete_case_model(case) for case in cases]

        return delete_models

    def map_blaise_delete_case_model(
        self, case: Dict[str, str]
    ) -> BlaiseDeleteCaseInformationBaseModel:
        return BlaiseDeleteCaseInformationBaseModel(
            case_id=self.get_case_id(case), outcome_code=self.get_outcome_code(case)
        )
