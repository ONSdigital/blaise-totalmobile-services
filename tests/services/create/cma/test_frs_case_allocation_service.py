import logging
from unittest.mock import Mock

import pytest

from app.exceptions.custom_exceptions import (
    CaseAllocationException,
    CaseNotFoundException,
    CaseReAllocationException,
    CaseResetFailedException,
    QuestionnaireDoesNotExistError,
)
from models.create.cma.totalmobile_incoming_frs_request_model import (
    TotalMobileIncomingFRSRequestModel,
)
from models.update.cma.totalmobile_incoming_frs_unallocation_request_model import (
    TotalMobileIncomingFRSUnallocationRequestModel,
)
from services.case_instruction_service import CaseInstructionService
from services.cma_blaise_service import CMABlaiseService
from services.create.cma.allocate_cma_case_service import AllocateCMACaseService


@pytest.fixture()
def mock_cma_blaise_service() -> CMABlaiseService:
    return Mock()


@pytest.fixture()
def mock_case_instruction_service() -> CaseInstructionService:
    return Mock()


@pytest.fixture()
def allocate_service(
    mock_cma_blaise_service, mock_case_instruction_service
) -> AllocateCMACaseService:
    service = AllocateCMACaseService(
        cma_blaise_service=mock_cma_blaise_service,
        case_instruction_service=mock_case_instruction_service,
    )
    return service


def test_create_case_creates_new_case_if_case_doesnot_exist_and_returns_successfully_with_right_parameters(
    allocate_service: AllocateCMACaseService,
    mock_cma_blaise_service,
    caplog,
    mock_frs_questionnaire_from_blaise,
):
    # arrange
    questionnaire = mock_frs_questionnaire_from_blaise
    totalmobile_request = TotalMobileIncomingFRSRequestModel(
        questionnaire_name=questionnaire["name"],
        case_id="100100",
        prem1="prem1",
        prem2="prem2",
        town="town",
        postcode="NP10 8XG",
        interviewer_name="Interviewer1",
        interviewer_blaise_login="User1",
    )
    mock_cma_blaise_service.questionnaire_exists.return_value = questionnaire
    mock_cma_blaise_service.case_exists.return_value = False

    # act
    with caplog.at_level(logging.INFO):
        allocate_service.create_case(totalmobile_request)

    # assert
    assert (
        "root",
        logging.INFO,
        f"Case {totalmobile_request.case_id} for Questionnaire {totalmobile_request.questionnaire_name} "
        f"has been created in CMA Launcher database and allocated to {totalmobile_request.interviewer_name}, "
        f"with Blaise Logins = {totalmobile_request.interviewer_blaise_login})",
    ) in caplog.record_tuples


def test_create_case_raises_questionnaire_doesnot_exist_exception_if_questionnaire_doesnot_exist(
    allocate_service, mock_cma_blaise_service, caplog
):
    # arrange
    totalmobile_request = TotalMobileIncomingFRSRequestModel(
        questionnaire_name="FRS2405A",
        case_id="100100",
        prem1="prem1",
        prem2="prem2",
        town="town",
        postcode="NP10 8XG",
        interviewer_name="User1",
        interviewer_blaise_login="User1",
    )
    mock_cma_blaise_service.questionnaire_exists.side_effect = ValueError(
        "Some error occured in blaise rest API while getting Questionnaire by name"
    )

    # act
    with caplog.at_level(logging.ERROR) and pytest.raises(
        QuestionnaireDoesNotExistError
    ):
        allocate_service.create_case(totalmobile_request)

    # assert
    assert (
        "root",
        logging.ERROR,
        f"Could not find Questionnaire FRS2405A in Blaise",
    ) in caplog.record_tuples


def test_create_case_raises_case_allocation_exception_if_rest_api_fails_creating_new_case(
    allocate_service,
    mock_cma_blaise_service,
    mock_frs_questionnaire_from_blaise,
):
    # arrange
    questionnaire = mock_frs_questionnaire_from_blaise
    totalmobile_request = TotalMobileIncomingFRSRequestModel(
        questionnaire_name="FRS2405A",
        case_id="100100",
        prem1="prem1",
        prem2="prem2",
        town="town",
        postcode="NP10 8XG",
        interviewer_name="User1",
        interviewer_blaise_login="User1",
    )
    mock_cma_blaise_service.questionnaire_exists.return_value = questionnaire
    mock_cma_blaise_service.case_exists.return_value = False
    mock_cma_blaise_service.create_frs_case.side_effect = CaseAllocationException

    # act
    with pytest.raises(CaseAllocationException):
        allocate_service.create_case(totalmobile_request)


def test_create_case_fails_if_case_exists_and_already_allocated_to_some_interviewer(
    allocate_service,
    mock_cma_blaise_service,
    mock_frs_questionnaire_from_blaise,
    mock_frs_allocated_case_from_cma_launcher,
    caplog,
):
    # arrange
    case = mock_frs_allocated_case_from_cma_launcher
    questionnaire = mock_frs_questionnaire_from_blaise
    totalmobile_request = TotalMobileIncomingFRSRequestModel(
        questionnaire_name=questionnaire["name"],
        case_id="100100",
        prem1="prem1",
        prem2="prem2",
        town="town",
        postcode="NP10 8XG",
        interviewer_name="User2",
        interviewer_blaise_login="User2",
    )
    mock_cma_blaise_service.questionnaire_exists.return_value = questionnaire
    mock_cma_blaise_service.case_exists.return_value = case

    case_id = str(case["fieldData"]["id"])
    cmA_ForWhom = str(case["fieldData"]["cmA_ForWhom"])

    # act
    with caplog.at_level(logging.ERROR) and pytest.raises(CaseReAllocationException):
        allocate_service.create_case(totalmobile_request)

    # assert
    assert (
        "root",
        logging.ERROR,
        f"Reallocation Scenario Found. Case with case_id {case_id} is already in Possession of {cmA_ForWhom}! Reallocation Failed.",
    ) in caplog.record_tuples


def test_create_case_successfully_reallocates_case_if_case_exists_and_already_reset_to_defaults(
    allocate_service,
    mock_cma_blaise_service,
    mock_frs_questionnaire_from_blaise,
    mock_frs_unallocated_case_reset_to_defaults_from_cma_launcher,
    caplog,
):
    # arrange
    case = mock_frs_unallocated_case_reset_to_defaults_from_cma_launcher
    questionnaire = mock_frs_questionnaire_from_blaise
    totalmobile_request = TotalMobileIncomingFRSRequestModel(
        questionnaire_name=questionnaire["name"],
        case_id="100100",
        prem1="prem1",
        prem2="prem2",
        town="town",
        postcode="NP10 8XG",
        interviewer_name="User2",
        interviewer_blaise_login="User2",
    )
    mock_cma_blaise_service.questionnaire_exists.return_value = questionnaire
    mock_cma_blaise_service.case_exists.return_value = case

    # act
    with caplog.at_level(logging.INFO):
        allocate_service.create_case(totalmobile_request)

    # assert
    assert (
        "root",
        logging.INFO,
        f"Successfull reallocation of Case {totalmobile_request.case_id} to User: '{totalmobile_request.interviewer_blaise_login}' in Questionnaire {totalmobile_request.questionnaire_name}",
    ) in caplog.record_tuples


def test_unallocate_case_creates_special_instruction_entry_and_resets_case_and_returns_successfully_with_right_parameters(
    allocate_service,
    mock_cma_blaise_service,
    mock_frs_questionnaire_from_blaise,
    mock_frs_allocated_case_from_cma_launcher,
    caplog,
):
    # arrange
    questionnaire = mock_frs_questionnaire_from_blaise
    case = mock_frs_allocated_case_from_cma_launcher
    totalmobile_unallocate_request = TotalMobileIncomingFRSUnallocationRequestModel(
        questionnaire_name=questionnaire["name"],
        case_id="100100",
        interviewer_name="User2",
    )
    mock_cma_blaise_service.questionnaire_exists.return_value = questionnaire
    mock_cma_blaise_service.case_exists.return_value = case

    # act
    with caplog.at_level(logging.INFO):
        allocate_service.unallocate_case(totalmobile_unallocate_request)

    # assert
    assert (
        "root",
        logging.INFO,
        f"Reset successful for Case: {totalmobile_unallocate_request.case_id} within Questionnaire {totalmobile_unallocate_request.questionnaire_name} in CMA_Launcher",
    ) in caplog.record_tuples


def test_unallocate_case_raises_questionnaire_doesnot_exist_exception_if_questionnaire_doesnot_exist(
    allocate_service, mock_cma_blaise_service, caplog
):
    # arrange
    totalmobile_unallocate_request = TotalMobileIncomingFRSUnallocationRequestModel(
        questionnaire_name="FRS2410A", case_id="100100", interviewer_name="User2"
    )
    mock_cma_blaise_service.questionnaire_exists.side_effect = ValueError(
        "Some error occured in blaise rest API while getting Questionnaire by name"
    )

    # act
    with caplog.at_level(logging.ERROR) and pytest.raises(
        QuestionnaireDoesNotExistError
    ):
        allocate_service.unallocate_case(totalmobile_unallocate_request)

    # assert
    assert (
        "root",
        logging.ERROR,
        f"Could not find Questionnaire FRS2410A in Blaise",
    ) in caplog.record_tuples


def test_unallocate_case_fails_and_raise_exception_if_case_doesnot_exist(
    allocate_service,
    mock_cma_blaise_service,
    mock_frs_questionnaire_from_blaise,
    caplog,
):
    # arrange
    questionnaire = mock_frs_questionnaire_from_blaise
    totalmobile_unallocate_request = TotalMobileIncomingFRSUnallocationRequestModel(
        questionnaire_name=questionnaire["name"],
        case_id="100100",
        interviewer_name="User2",
    )
    mock_cma_blaise_service.questionnaire_exists.return_value = questionnaire
    mock_cma_blaise_service.case_exists.return_value = False
    caplog.set_level(logging.INFO)

    # act
    with pytest.raises(CaseNotFoundException):
        allocate_service.unallocate_case(totalmobile_unallocate_request)

    # assert
    assert (
        "root",
        logging.INFO,
        f"Case {totalmobile_unallocate_request.case_id} within Questionnaire "
        f"{totalmobile_unallocate_request.questionnaire_name} does not exist in CMA_Launcher. "
        f"Unallocation failed.",
    ) in caplog.record_tuples


def test_unallocate_case_raises_reset_fail_exception_if_case_reset_fails(
    allocate_service,
    mock_cma_blaise_service,
    mock_frs_questionnaire_from_blaise,
    mock_frs_allocated_case_from_cma_launcher,
    caplog,
):
    # arrange
    questionnaire = mock_frs_questionnaire_from_blaise
    case = mock_frs_allocated_case_from_cma_launcher
    totalmobile_unallocate_request = TotalMobileIncomingFRSUnallocationRequestModel(
        questionnaire_name=questionnaire["name"],
        case_id="100100",
        interviewer_name="User2",
    )
    mock_cma_blaise_service.questionnaire_exists.return_value = questionnaire
    mock_cma_blaise_service.case_exists.return_value = case
    mock_cma_blaise_service.update_frs_case.side_effect = ValueError(
        "Some error occured in blaise rest API while updating multikey case!"
    )

    # act
    with caplog.at_level(logging.ERROR) and pytest.raises(CaseResetFailedException):
        allocate_service.unallocate_case(totalmobile_unallocate_request)

    # assert
    assert (
        "root",
        logging.ERROR,
        f"Reset failed. Failed in resetting Case: {totalmobile_unallocate_request.case_id} within Questionnaire {totalmobile_unallocate_request.questionnaire_name} in CMA_Launcher",
    ) in caplog.record_tuples
