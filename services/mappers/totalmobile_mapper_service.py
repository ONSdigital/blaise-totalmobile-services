import logging
from typing import Dict, List, Sequence

from models.blaise.blaise_case_information_base_model import (
    BlaiseCaseInformationBaseModel,
)
from models.cloud_tasks.totalmobile_create_job_model import TotalmobileCreateJobModel
from models.totalmobile.totalmobile_outgoing_create_job_payload_model import (
    TotalMobileOutgoingCreateJobPayloadModel,
)
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel


class TotalmobileMapperService:
    def map_totalmobile_create_job_models(
        self,
        questionnaire_name: str,
        cases: Sequence[BlaiseCaseInformationBaseModel],
        world_model: TotalmobileWorldModel,
    ) -> List[TotalmobileCreateJobModel]:

        job_models = [
            TotalmobileCreateJobModel(
                questionnaire_name,
                world_model.get_world_id(case.field_region),
                case.case_id,
                self._map_totalmobile_job_payload(questionnaire_name, case),
            )
            for case in cases
        ]

        logging.info(f"Finished mapping Totalmobile jobs for questionnaire {questionnaire_name}")

        return job_models

    @staticmethod
    def _map_totalmobile_job_payload(
            questionnaire_name: str, case: BlaiseCaseInformationBaseModel
    ) -> Dict[str, str]:
        logging.info(f"_map_totalmobile_job_payload for questionnaire {questionnaire_name} and case {case.case_id}")
        totalmobile_outgoing_payload_model = (
            TotalMobileOutgoingCreateJobPayloadModel.import_case(
                questionnaire_name, case
            )
        )

        return totalmobile_outgoing_payload_model.to_payload()
