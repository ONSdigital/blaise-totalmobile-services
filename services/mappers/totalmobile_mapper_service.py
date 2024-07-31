import logging
from typing import List
from models.blaise.blaise_case_information_model import BlaiseCaseInformationModel
from models.cloud_tasks.totalmobile_create_job_model import TotalmobileCreateJobModel
from models.totalmobile.totalmobile_outgoing_create_job_payload_model import TotalMobileOutgoingCreateJobPayloadModel
from models.totalmobile.totalmobile_world_model import TotalmobileWorldModel
from services.uac_service import UacService


class TotalmobileMapperService:
    def __init__(
        self,
        uac_service: UacService,
    ):
        self._uac_service = uac_service
    
    def map_totalmobile_create_job_models(
        self,
        questionnaire_name: str,
        cases: List[BlaiseCaseInformationModel],
        world_model: TotalmobileWorldModel,
    ) -> List[TotalmobileCreateJobModel]:
        questionnaire_uac_model = self._uac_service.get_questionnaire_uac_model(
            questionnaire_name
        )

        job_models = [
            TotalmobileCreateJobModel(
                questionnaire_name,
                world_model.get_world_id(case.field_region),
                case.case_id,
                TotalMobileOutgoingCreateJobPayloadModel.import_case(
                    questionnaire_name,
                    case,
                    questionnaire_uac_model.get_uac_chunks(case.case_id),
                ).to_payload(),
            )
            for case in cases
        ]

        logging.info(
            f"Finished mapping Totalmobile jobs for questionnaire {questionnaire_name}"
        )

        return job_models    