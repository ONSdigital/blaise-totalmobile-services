import logging

from datetime import datetime
from services.cma_blaise_service import CMABlaiseService
from app.exceptions.custom_exceptions import SpecialInstructionCreationFailedException
from models.create.cma.blaise_cma_frs_create_case_model import FRSCaseModel # TODO: BL - Should be generic?


class CaseInstructionService:
    def __init__(self, cma_blaise_service: CMABlaiseService):
        self._cma_blaise_service = cma_blaise_service

    def create_new_entry_for_special_instructions(self, case, questionnaire_name: str) -> None:

        guid = case["fieldData"]["mainSurveyID"]
        questionnaire_name = questionnaire_name
        unique_case_id = case["fieldData"]["id"]
        prev_interviewer = case["fieldData"]["cmA_ForWhom"]
        current_timestamp = datetime.now()
        formatted_date_time = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        frs_case = FRSCaseModel(
            user=prev_interviewer,
            questionnaire_name=questionnaire_name,
            guid="00000000-0000-0000-0000-000000000000",
            case_id=f"{questionnaire_name}-{unique_case_id}-{prev_interviewer}-{formatted_date_time}",
            custom_use=f"{guid};{unique_case_id};",
            location="RELEASE_SOME",
            in_posession="",
            prem1="",
            prem2="",
            town="",
            postcode="",
        )
        try:
            self._cma_blaise_service.create_frs_case(frs_case)
            logging.info(
                f"Special Instructions entry created for Case {unique_case_id} for Questionnaire {questionnaire_name}"
            )
        except:
            logging.error(
                f"Special Instructions entry creation for Case {unique_case_id} for Questionnaire {questionnaire_name} failed"
            )
            raise SpecialInstructionCreationFailedException()