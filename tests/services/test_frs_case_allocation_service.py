import logging
from typing import List
from unittest.mock import Mock

import pytest
from app.config import Config
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
from models.update.cma.totalmobile_incoming_frs_unallocation_request_model import TotalMobileIncomingFRSUnallocationRequestModel
from services.create.cma.frs_case_allocation_service import FRSCaseAllocationService

class TestFRSCaseAllocationService:
    
    @pytest.fixture()
    def mock_cma_blaise_service(self):
        return Mock()
    
    @pytest.fixture()
    def service(self,mock_cma_blaise_service) -> FRSCaseAllocationService:
        return FRSCaseAllocationService(cma_blaise_service=mock_cma_blaise_service)
    
    def test_create_case_creates_new_case_if_case_doesnot_exist_and_returns_successfully_with_right_parameters(
        self,
        mock_cma_blaise_service,
        service: FRSCaseAllocationService,
        caplog,
        mock_frs_questionnaire_from_blaise
    ):
        # arrange
        questionnaire = mock_frs_questionnaire_from_blaise
        totalmobile_request = TotalMobileIncomingFRSRequestModel(
                    questionnaire_name= questionnaire["name"], 
                    case_id="100100", 
                    interviewer_name="Interviewer1", 
                    interviewer_blaise_login="User1"
                    )
        mock_cma_blaise_service.questionnaire_exists.return_value = (questionnaire)
        mock_cma_blaise_service.case_exists.return_value = False

        # act
        with caplog.at_level(logging.INFO):
            service.create_case(totalmobile_request)

        # assert
        assert (
            "root",
            logging.INFO,
            f"Case {totalmobile_request.case_id} for questionnaire {totalmobile_request.questionnaire_name} "
            f"has been created in CMA Launcher database and allocated to {totalmobile_request.interviewer_name}, "
            f"with Blaise Logins ={totalmobile_request.interviewer_blaise_login})",
        ) in caplog.record_tuples


    def test_create_case_fails_if_case_exists_and_already_allocated_to_some_interviewer(
        self,
        mock_cma_blaise_service,
        mock_frs_questionnaire_from_blaise,
        mock_frs_allocated_case_from_cma_launcher,
        service: FRSCaseAllocationService,
        caplog,
    ):
        # arrange
        case = mock_frs_allocated_case_from_cma_launcher
        questionnaire = mock_frs_questionnaire_from_blaise
        totalmobile_request = TotalMobileIncomingFRSRequestModel(
                    questionnaire_name= questionnaire["name"], 
                    case_id="100100", 
                    interviewer_name="User2", 
                    interviewer_blaise_login="User2"
                    )
        mock_cma_blaise_service.questionnaire_exists.return_value = (questionnaire)
        mock_cma_blaise_service.case_exists.return_value = case

        case_id = str(case["fieldData"]["id"])
        cmA_ForWhom = str(case["fieldData"]["cmA_ForWhom"])

        # act
        with caplog.at_level(logging.ERROR) and pytest.raises(CaseReAllocationException) :
            service.create_case(totalmobile_request)

        # assert
        assert (
            "root",
            logging.ERROR,
            f"Reallocation Scenario Found. Case with case_id {case_id} is already in Possession "
            f"of {cmA_ForWhom}! Reallocation Failed."
        ) in caplog.record_tuples

    def test_create_case_successfully_reallocates_case_if_case_exists_and_already_reset_to_defaults(
        self,
        mock_cma_blaise_service,
        mock_frs_questionnaire_from_blaise,
        mock_frs_unallocated_case_reset_to_defaults_from_cma_launcher,
        service: FRSCaseAllocationService,
        caplog,
    ):
        # arrange
        case = mock_frs_unallocated_case_reset_to_defaults_from_cma_launcher
        questionnaire = mock_frs_questionnaire_from_blaise
        totalmobile_request = TotalMobileIncomingFRSRequestModel(
                    questionnaire_name= questionnaire["name"], 
                    case_id="100100", 
                    interviewer_name="User2", 
                    interviewer_blaise_login="User2"
                    )
        mock_cma_blaise_service.questionnaire_exists.return_value = (questionnaire)
        mock_cma_blaise_service.case_exists.return_value = case

        # act
        with caplog.at_level(logging.INFO) :
            service.create_case(totalmobile_request)

        # assert
        assert (
            "root",
            logging.INFO,
            f"Successfull reallocation of Case {totalmobile_request.case_id} to User: '{totalmobile_request.interviewer_blaise_login}' in Questionnaire {totalmobile_request.questionnaire_name}"
        ) in caplog.record_tuples