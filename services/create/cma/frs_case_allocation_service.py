import logging
import re
from datetime import datetime
from typing import Any, Dict

from app.exceptions.custom_exceptions import (
    CaseAllocationException,
    CaseNotFoundException,
    CaseReAllocationException,
    CaseResetFailedException,
    QuestionnaireDoesNotExistError,
    SpecialInstructionCreationFailedException,
)
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

    @staticmethod
    def parse_contact_data_pii_values(contact_data_string: str) -> dict:
        pattern = re.compile(
            r"PII\.TLA\t(?P<TLA>\w+)\t"
            r"PII\.Month\t(?P<Month>\w+)\t"
            r"PII\.Year\t(?P<Year>\w+)\t"
            r"PII\.Prem1\t(?P<Prem1>.*?)\t"
            r"PII\.Prem2\t(?P<Prem2>.*?)\t"
            r"PII\.Town\t(?P<Town>.*?)\t"
            r"PII\.Postcode\t(?P<Postcode>.*?)"
        )

        match = pattern.search(contact_data_string)
        if match:
            return match.groupdict()
        else:
            return {}

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
            cma_for_whom = str(case["fieldData"]["cmA_ForWhom"])
            cma_in_possession = str(case["fieldData"]["cmA_InPossession"])
            cma_location = str(case["fieldData"]["cmA_Location"])

            # Scenario 1: Assumption: Special Instructions entry exists as a result of Unallocation
            if (
                cma_for_whom == ""
                and cma_in_possession == ""
                and cma_location == "SERVER"
            ):
                self._reallocate_existing_case_to_new_interviewer(
                    case, totalmobile_request
                )
            # Scenario 2: Fail the allocation because Special Instructions entry does not exist as suggested by cmA_ForWhom, cma_InPossession and cma_Location
            else:
                logging.error(
                    f"Reallocation Scenario Found. Case with case_id {case_id} is already in Possession of {cma_for_whom}! Reallocation Failed."
                )
                raise CaseReAllocationException()

        else:
            self._create_new_frs_case(totalmobile_request, questionnaire["id"])
            logging.info(
                f"Case {totalmobile_request.case_id} for Questionnaire {totalmobile_request.questionnaire_name} "
                f"has been created in CMA Launcher database and allocated to {totalmobile_request.interviewer_name}, "
                f"with Blaise Logins = {totalmobile_request.interviewer_blaise_login})"
            )

    def unallocate_case(
        self,
        totalmobile_unallocation_request: TotalMobileIncomingFRSUnallocationRequestModel,  # TODO: Need to call dis with this ting
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
        frs_case_from_totalmobile_request: TotalMobileIncomingFRSRequestModel,
        questionnaire_guid: str,
    ) -> None:
        frs_case = FRSCaseModel(
            user=frs_case_from_totalmobile_request.interviewer_blaise_login,
            questionnaire_name=frs_case_from_totalmobile_request.questionnaire_name,
            guid=questionnaire_guid,
            case_id=frs_case_from_totalmobile_request.case_id,
            custom_use="",
            location="",
            inPosession="",
            prem1=frs_case_from_totalmobile_request.prem1,
            prem2=frs_case_from_totalmobile_request.prem2,
            town=frs_case_from_totalmobile_request.town,
            postcode=frs_case_from_totalmobile_request.postcode,
        )
        try:
            self._cma_blaise_service.create_frs_case(frs_case)
        except:
            raise CaseAllocationException

    def _create_new_entry_for_special_instructions(
        self, case, questionnaire_name: str
    ) -> None:

        guid = case["fieldData"]["mainSurveyID"]
        questionnaire_name = questionnaire_name
        unique_case_id = case["fieldData"]["id"]
        prev_interviewer = case["fieldData"]["cmA_ForWhom"]
        current_timestamp = datetime.now()
        formatted_date_time = current_timestamp.strftime("%Y-%m-%d %H:%M:%S")

        frs_case = FRSCaseModel(
            user=prev_interviewer,  # TODO: needs to be the current interviewer's
            questionnaire_name=questionnaire_name,
            guid="00000000-0000-0000-0000-000000000000",  # TODO: special instruction entry
            case_id=f"{questionnaire_name}-{unique_case_id}-{prev_interviewer}-{formatted_date_time}",
            custom_use=f"{guid};{unique_case_id};",  # TODO: contains key value pairs to identify the case to fudge with
            location="RELEASE_SOME",  # TODO: dis ting releases cases from devices
            inPosession="",
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

    def _reallocate_existing_case_to_new_interviewer(
        self,
        old_allocated_case: Dict[str, Any],
        new_totalmobile_allocation_request: TotalMobileIncomingFRSRequestModel,
    ):

        case_id = old_allocated_case["fieldData"]["id"]
        new_interviewer = new_totalmobile_allocation_request.interviewer_blaise_login

        frs_case = FRSCaseModel(
            user=new_interviewer,
            questionnaire_name=old_allocated_case["fieldData"]["surveyDisplayName"],
            guid=old_allocated_case["fieldData"]["mainSurveyID"],
            case_id=case_id,
            custom_use="",
            location="SERVER",
            inPosession="",
            prem1=new_totalmobile_allocation_request.prem1,
            prem2=new_totalmobile_allocation_request.prem2,
            town=new_totalmobile_allocation_request.town,
            postcode=new_totalmobile_allocation_request.postcode,
        )
        try:
            self._cma_blaise_service.update_frs_case(frs_case)
            logging.info(
                f"Successfull reallocation of Case {frs_case.case_id} to User: '{frs_case.user}' in Questionnaire {frs_case.questionnaire_name}"
            )
        except:
            raise CaseReAllocationException()

    def _reset_existing_case_to_defaults(self, old_allocated_case):
        case_id = old_allocated_case["fieldData"]["id"]
        questionnaire_name = old_allocated_case["fieldData"]["surveyDisplayName"]
        contact_data = self.parse_contact_data_pii_values(
            old_allocated_case["fieldData"]["cmA_ContactData"]
        )

        frs_case = FRSCaseModel(
            user="",
            questionnaire_name=questionnaire_name,
            guid=old_allocated_case["fieldData"]["mainSurveyID"],
            case_id=case_id,
            custom_use="",
            location="SERVER",
            inPosession="",
            prem1=contact_data.get("Prem1"),
            prem2=contact_data.get("Prem2"),
            town=contact_data.get("Town"),
            postcode=contact_data.get("Postcode"),
        )
        try:
            self._cma_blaise_service.update_frs_case(frs_case)
            logging.info(
                f"Reset successful for Case: {case_id} within Questionnaire {questionnaire_name} in CMA_Launcher"
            )
        except:
            logging.error(
                f"Reset failed. Failed in resetting Case: {case_id} within Questionnaire {questionnaire_name} in CMA_Launcher"
            )
            raise CaseResetFailedException()
