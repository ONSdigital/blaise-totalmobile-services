import logging
from datetime import datetime
from typing import Dict

from app.exceptions.custom_exceptions import (
    CaseAllocationException,
    CaseNotFoundException,
    CaseReAllocationException,
    CaseResetFailedException,
    QuestionnaireDoesNotExistError,
    SpecialInstructionCreationFailedException,
)
from appconfig import Config
from models.create.cma.blaise_cma_frs_create_case_model import FRSCaseModel
from models.create.cma.totalmobile_incoming_frs_request_model import (
    TotalMobileIncomingFRSRequestModel,
)
from models.update.cma.totalmobile_incoming_frs_unallocation_request_model import (
    TotalMobileIncomingFRSUnallocationRequestModel,
)
from services.cma_blaise_service import CMABlaiseService


class FRSCaseAllocationService:
    def __init__(self, cma_blaise_service: CMABlaiseService):
        self._cma_blaise_service = cma_blaise_service

    def create_case(
        self, totalmobile_request: TotalMobileIncomingFRSRequestModel
    ) -> None:

        try:
            questionnaire = self._cma_blaise_service.questionnaire_exists(
                totalmobile_request.questionnaire_name
            )
            logging.info(
                f"Successfully found questionnaire {totalmobile_request.questionnaire_name} in Blaise"
            )
        except:
            logging.error(
                f"Could not find Questionnaire {totalmobile_request.questionnaire_name} in Blaise"
            )
            raise QuestionnaireDoesNotExistError()

        case = self._cma_blaise_service.case_exists(
            questionnaire["id"], totalmobile_request.case_id
        )

        if case and isinstance(case, Dict):
            logging.info(
                f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
                f"already exists in CMA Launcher database"
            )

            case_id = str(case["fieldData"]["id"])
            cmA_ForWhom = str(case["fieldData"]["cmA_ForWhom"])
            cma_InPossession = str(case["fieldData"]["cmA_InPossession"])
            cma_Location = str(case["fieldData"]["cmA_Location"])

            # Scenario 1: Assumption: Special Instructions entry exists as a result of Unallocation
            if (
                cmA_ForWhom == ""
                and cma_InPossession == ""
                and cma_Location == "SERVER"
            ):
                self._reallocate_existing_case_to_new_interviewer(
                    case, totalmobile_request
                )
            # Scenario 2: Fail the allocation because Special Instructions entry does not exist as suggested by cmA_ForWhom, cma_InPossession and cma_Location
            else:
                logging.error(
                    f"Reallocation Scenario Found. Case with case_id {case_id} is already in Possession of {cmA_ForWhom}! Reallocation Failed."
                )
                raise CaseReAllocationException()

        else:
            self._create_new_frs_case(totalmobile_request, questionnaire["id"])
            logging.info(
                f"Case {totalmobile_request.case_id} for Questionnaire {totalmobile_request.questionnaire_name} "
                f"has been created in CMA Launcher database and allocated to {totalmobile_request.interviewer_name}, "
                f"with Blaise Logins ={totalmobile_request.interviewer_blaise_login})"
            )

    def unallocate_case(
        self,
        totalmobile_unallocation_request: TotalMobileIncomingFRSUnallocationRequestModel,
    ) -> None:

        try:
            questionnaire = self._cma_blaise_service.questionnaire_exists(
                totalmobile_unallocation_request.questionnaire_name
            )
            logging.info(
                f"Successfully found questionnaire {totalmobile_unallocation_request.questionnaire_name} in Blaise"
            )
        except:
            logging.error(
                f"Could not find Questionnaire {totalmobile_unallocation_request.questionnaire_name} in Blaise"
            )
            raise QuestionnaireDoesNotExistError()

        old_case = self._cma_blaise_service.case_exists(
            questionnaire["id"], totalmobile_unallocation_request.case_id
        )

        if old_case:
            self._create_new_entry_for_special_instructions(
                old_case, totalmobile_unallocation_request.questionnaire_name
            )
            self._reset_existing_case_to_defaults(old_case)
        else:
            logging.info(
                f"Case {totalmobile_unallocation_request.case_id} within Questionnaire "
                f"{totalmobile_unallocation_request.questionnaire_name} does not exist in CMA_Launcher. "
                f"Unallocation failed."
            )
            raise CaseNotFoundException()

    def _create_new_frs_case(
        self,
        frsCaseFromTotalMobileRequest: TotalMobileIncomingFRSRequestModel,
        questionnaire_guid: str,
    ) -> None:
        frsCase = FRSCaseModel(
            user=frsCaseFromTotalMobileRequest.interviewer_blaise_login,
            questionnaire_name=frsCaseFromTotalMobileRequest.questionnaire_name,
            guid=questionnaire_guid,
            case_id=frsCaseFromTotalMobileRequest.case_id,
            custom_use="",
            location="",
            inPosession="",
        )
        try:
            self._cma_blaise_service.create_frs_case(frsCase)
        except:
            raise CaseAllocationException

    def _create_new_entry_for_special_instructions(
        self, case, questionnaireName
    ) -> None:

        guid = case["fieldData"]["mainSurveyID"]
        questionnaire_name = questionnaireName
        unique_case_id = case["fieldData"]["id"]
        prev_interviewer = case["fieldData"]["cmA_ForWhom"]
        current_timestamp = datetime.now()
        formatted_date_time = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        frsCase = FRSCaseModel(
            user=prev_interviewer,
            questionnaire_name=questionnaire_name,
            guid="00000000-0000-0000-0000-000000000000",
            case_id=f"{questionnaire_name}-{unique_case_id}-{prev_interviewer}-{formatted_date_time}",
            custom_use=f"{guid};{unique_case_id};",
            location="RELEASE_SOME",
            inPosession="",
        )
        try:
            self._cma_blaise_service.create_frs_case(frsCase)
            logging.info(
                f"Special Instructions entry created for Case {unique_case_id} for Questionnaire {questionnaire_name}"
            )
        except:
            logging.error(
                f"Special Instructions entry creation for Case {unique_case_id} for Questionnaire {questionnaire_name} failed"
            )
            raise SpecialInstructionCreationFailedException()

    def _reallocate_existing_case_to_new_interviewer(
        self,
        old_allocated_case,
        new_totalmobile_allocation_request: TotalMobileIncomingFRSRequestModel,
    ):

        case_id = old_allocated_case["fieldData"]["id"]
        new_Interviewer = new_totalmobile_allocation_request.interviewer_blaise_login

        frsCase = FRSCaseModel(
            user=new_Interviewer,
            questionnaire_name=old_allocated_case["fieldData"]["surveyDisplayName"],
            guid=old_allocated_case["fieldData"]["mainSurveyID"],
            case_id=case_id,
            custom_use="",
            location="SERVER",
            inPosession="",
        )
        try:
            self._cma_blaise_service.update_frs_case(frsCase)
            logging.info(
                f"Successfull reallocation of Case {frsCase.case_id} to User: '{frsCase.user}' in Questionnaire {frsCase.questionnaire_name}"
            )
        except:
            raise CaseAllocationException()

    def _reset_existing_case_to_defaults(self, old_allocated_case):

        case_id = old_allocated_case["fieldData"]["id"]
        questionnaire_name = old_allocated_case["fieldData"]["surveyDisplayName"]

        frsCase = FRSCaseModel(
            user="",
            questionnaire_name=questionnaire_name,
            guid=old_allocated_case["fieldData"]["mainSurveyID"],
            case_id=case_id,
            custom_use="",
            location="SERVER",
            inPosession="",
        )
        try:
            self._cma_blaise_service.update_frs_case(frsCase)
            logging.info(
                f"Reset successful for Case: {case_id} within Questionnaire {questionnaire_name} in CMA_Launcher"
            )
        except:
            logging.error(
                f"Reset failed. Failed in resetting Case: {case_id} within Questionnaire {questionnaire_name} in CMA_Launcher"
            )
            raise CaseResetFailedException()
