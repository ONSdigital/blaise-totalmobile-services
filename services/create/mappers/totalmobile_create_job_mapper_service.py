import logging
from typing import Dict, List, Sequence

from models.common.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from models.create.blaise.blaise_create_case_model import BlaiseCreateCaseModelBase
from models.create.totalmobile.totalmobile_create_job_model import (
    TotalmobileCreateJobModel,
    TotalmobileCreateJobModelRequestJson,
)
from services.create.mappers.totalmobile_payload_mapper_service import (
    TotalmobilePayloadMapperService,
)


class TotalmobileCreateJobMapperService:
    def __init__(
        self,
        payload_mapper: TotalmobilePayloadMapperService,
    ):
        self._payload_mapper = payload_mapper

    def map_totalmobile_create_job_models(
        self,
        questionnaire_name: str,
        cases: Sequence[BlaiseCreateCaseModelBase],
        world_model: TotalmobileWorldModel,
    ) -> List[TotalmobileCreateJobModel]:

        job_models = [
            self.map_totalmobile_create_job_model(questionnaire_name, case, world_model)
            for case in cases
        ]

        logging.info(
            f"Finished mapping Totalmobile jobs for questionnaire {questionnaire_name}"
        )

        return job_models

    def map_totalmobile_create_job_model(
        self,
        questionnaire_name: str,
        case: BlaiseCreateCaseModelBase,
        world_model: TotalmobileWorldModel,
    ) -> TotalmobileCreateJobModel:

        return TotalmobileCreateJobModel(
            questionnaire_name,
            world_model.get_world_id(case.field_region),
            case.case_id,
            self.map_totalmobile_job_payload(questionnaire_name, case),
        )

    def map_totalmobile_create_job_model_from_json(
        self, request_json: TotalmobileCreateJobModelRequestJson
    ) -> TotalmobileCreateJobModel:

        return TotalmobileCreateJobModel(
            questionnaire=request_json["questionnaire"],
            world_id=request_json["world_id"],
            case_id=request_json["case_id"],
            payload=request_json["payload"],
        )

    def map_totalmobile_job_payload(
        self, questionnaire_name: str, case: BlaiseCreateCaseModelBase
    ) -> Dict[str, str]:
        logging.info(
            f"_map_totalmobile_job_payload for questionnaire {questionnaire_name} and case {case.case_id}"
        )
        totalmobile_outgoing_payload_model = (
            self._payload_mapper.map_totalmobile_payload_model(questionnaire_name, case)
        )

        return totalmobile_outgoing_payload_model.to_payload()
