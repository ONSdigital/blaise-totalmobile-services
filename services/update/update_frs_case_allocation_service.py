import logging
from typing import Any, Dict

from app.exceptions.custom_exceptions import (
    CaseCreationException,
    QuestionnaireDoesNotExistError,
)

from models.create.cma.blaise_cma_frs_create_case_model import FRSCaseModel
from models.update.totalmobile_incoming_update_frs_request_model import (
    TotalMobileIncomingUpdateFRSRequestModel,
)
from services.cma_blaise_service import CMABlaiseService


class UpdateFRSCaseService:
    def __init__(self, cma_blaise_service: CMABlaiseService):
        self._cma_blaise_service = cma_blaise_service

    def update_case(
        self, totalmobile_request: TotalMobileIncomingUpdateFRSRequestModel
    ) -> None:
        self._validate_questionnaire_exists(totalmobile_request.questionnaire_name)

        case = self._cma_blaise_service.validate_if_case_exist_in_cma_launcher(totalmobile_request.questionnaire_guid,
            totalmobile_request.questionnaire_name, totalmobile_request.case_id
        )
        
        if case:
            previousInterviewer = str(case["fieldData"]["cmA_ForWhom"])
            logging.info(
            f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name}"
            f"already exists in CMA Launcher database and allocated to {previousInterviewer} "
            )
            self._update_frs_case_with_business_logic(totalmobile_request, case)
            return

        else:
            self._create_new_frs_case(totalmobile_request)
            logging.info(
            f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
            f"has been created in CMA Launcher database and allocated to {totalmobile_request.interviewer_name}, "
            f"with Blaise Logins ={totalmobile_request.interviewer_blaise_login})")
            return

       
    def _validate_questionnaire_exists(self, questionnaire_name: str) -> None:
        if not self._cma_blaise_service.validate_questionnaire_exists(questionnaire_name):
            logging.error(
                f"Could not find questionnaire {questionnaire_name} in Blaise"
            )
            raise QuestionnaireDoesNotExistError()

        logging.info(f"Successfully found questionnaire {questionnaire_name} in Blaise")

    def _update_frs_case_with_business_logic(self, totalmobile_request:TotalMobileIncomingUpdateFRSRequestModel, case) -> None:
        
        #Step-1: create a Special Instructions entry in CMA_Launcher DB for previous allocated interviewer to release the case
        self._create_new_entry_for_special_instructions(case, totalmobile_request.questionnaire_name)
        logging.info(
            f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
            f"is ready to be reallocated to {totalmobile_request.interviewer_name}, "
            f"with Blaise Logins ={totalmobile_request.interviewer_blaise_login})")
            
        #Step-2: edit the already existing case that was assigned to previous allocated interviewer to the new interviewer by updating CMA_ForWhom, CMA_InPossession, CMA_Location fields
        self._reallocate_existing_case_to_new_interviewer(case, totalmobile_request)
        logging.info(
            f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
            f"successfully reallocated to {totalmobile_request.interviewer_name}, "
            f"with Blaise Logins ={totalmobile_request.interviewer_blaise_login})")
        return

    def _create_new_frs_case(self, frsCaseFromTotalMobileRequest: TotalMobileIncomingUpdateFRSRequestModel) -> None:
        frsCase = FRSCaseModel(user = frsCaseFromTotalMobileRequest.interviewer_blaise_login, questionnaire_name = frsCaseFromTotalMobileRequest.questionnaire_name, guid =  frsCaseFromTotalMobileRequest.questionnaire_guid, case_id = frsCaseFromTotalMobileRequest.case_id,custom_use="",location="", inPosession="")
        try:
            self._cma_blaise_service.create_frs_case_for_user(frsCase)
            logging.info(f"Successfully created case for {frsCaseFromTotalMobileRequest.interviewer_name} User "
            f"with Blaise Login = {frsCaseFromTotalMobileRequest.interviewer_blaise_login} within Questionnaire "
            f"{frsCaseFromTotalMobileRequest.questionnaire_name} in Blaise, CMA_Launcher"
        )
        except:
            logging.error(
                f"Could not create a case for {frsCaseFromTotalMobileRequest.interviewer_name} User"
                f"with Blaise Login = {frsCaseFromTotalMobileRequest.interviewer_blaise_login} within Questionnaire"
                f"{frsCaseFromTotalMobileRequest.questionnaire_name} in Blaise, CMA_Launcher...."
            )
            raise CaseCreationException()
        

    def _create_new_entry_for_special_instructions(self, case, questionnaireName) -> None:

        guid = case["fieldData"]["mainSurveyID"]
        questionnaire_name = questionnaireName
        unique_case_id = case["fieldData"]["id"]
        prev_interviewer = case["fieldData"]["cmA_ForWhom"]


        frsCase = FRSCaseModel(
            user = prev_interviewer,
            questionnaire_name = questionnaire_name, 
            guid =  "00000000-0000-0000-0000-000000000000", 
            case_id = f"{guid}-{questionnaire_name}-{unique_case_id}-{prev_interviewer}",
            custom_use = f"{guid};{unique_case_id}",
            location = "RELEASE_SOME",
            inPosession=""
            )
        try:
            self._cma_blaise_service.create_frs_case_for_user(frsCase)
            logging.info(f"Successfully created Special Instructions entry for reallocation"
        )
        except:
            logging.error(
                f"Could not create a Special Instructions entry for reallocation"
            )
            raise CaseCreationException()

    def _reallocate_existing_case_to_new_interviewer(self, old_allocated_case, new_totalmobile_allocation_request:TotalMobileIncomingUpdateFRSRequestModel):
    
        frsCase = FRSCaseModel(
            user = new_totalmobile_allocation_request.interviewer_blaise_login,
            questionnaire_name = old_allocated_case["fieldData"]["surveyDisplayName"], 
            guid = old_allocated_case["fieldData"]["mainSurveyID"], 
            case_id =  old_allocated_case["fieldData"]["id"],
            custom_use = "",
            location = "SERVER",
            inPosession= ""
            )
        try:
            self._cma_blaise_service.update_frs_case_for_user(frsCase)
            logging.info(f"Successfully created Special Instructions entry for reallocation"
        )
        except:
            logging.error(
                f"Could not create a Special Instructions entry for reallocation"
            )
            raise CaseCreationException()

