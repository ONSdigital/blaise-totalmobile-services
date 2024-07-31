import logging
from typing import Dict, List
from client.bus import UacChunks
from models.blaise.case_information_base_model import CaseInformationBaseModel
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
    
    def get_uac_chunks(
            self,
            questionnaire_name: str,
            case_id: str,
    ) -> UacChunks:
        questionnaire_uac_model = self._uac_service.get_questionnaire_uac_model(questionnaire_name)
        return questionnaire_uac_model.get_uac_chunks(case_id)

    def map_totalmobile_job_payload(
        self,
        questionnaire_name: str,
        case: CaseInformationBaseModel
        ) -> Dict[str, str]:

        uac_chunks = self.get_uac_chunks(questionnaire_name, case.case_id) if case.has_uac else None

        totalmobile_outgoing_payload_model = TotalMobileOutgoingCreateJobPayloadModel.import_case(
                    questionnaire_name,
                    case,
                    uac_chunks,
                )
        
        return totalmobile_outgoing_payload_model.to_payload()

    def map_totalmobile_create_job_models(
        self,
        questionnaire_name: str,
        cases: List[CaseInformationBaseModel],
        world_model: TotalmobileWorldModel,
    ) -> List[TotalmobileCreateJobModel]:

        job_models = [
            TotalmobileCreateJobModel(
                questionnaire_name,
                world_model.get_world_id(case.field_region),
                case.case_id,
                self.map_totalmobile_job_payload(questionnaire_name, case),
            )
            for case in cases
        ]

        logging.info(
            f"Finished mapping Totalmobile jobs for questionnaire {questionnaire_name}"
        )

        return job_models    
    