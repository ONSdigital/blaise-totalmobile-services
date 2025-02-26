import logging

from app.exceptions.custom_exceptions import (
    BadReferenceError,
    MissingReferenceError,
    SurveyDoesNotExistError,
)
from factories.service_instance_factory import ServiceInstanceFactory
from models.create.cma.totalmobile_incoming_frs_request_model import (
    TotalMobileIncomingFRSRequestModel,
)
from models.update.cma.totalmobile_incoming_frs_unallocation_request_model import (
    TotalMobileIncomingFRSUnallocationRequestModel,
)
from models.update.totalmobile_incoming_update_request_model import (
    TotalMobileIncomingUpdateRequestModel,
)
from services.cma_blaise_service import CMABlaiseService
from services.delete.delete_cma_case_service import DeleteCMACaseService
from services.create.cma.frs_case_allocation_service import FRSCaseAllocationService


def submit_form_result_request_handler(request, current_app):
    data = request.get_json()
    totalmobile_case = TotalMobileIncomingUpdateRequestModel.import_request(data)

    survey_type = get_survey_type(data)
    verify_survey_type(survey_type)

    ServiceInstanceFactory().create_update_case_service(
        survey_type, current_app.blaise_service
    ).update_case(totalmobile_case)

    if survey_type == "FRS":
        remove_case_from_cma(current_app, totalmobile_case)


def remove_case_from_cma(current_app, totalmobile_case):
    cma_blaise_service = CMABlaiseService(current_app.app_config)
    frs_case_allocation_service = FRSCaseAllocationService(cma_blaise_service)
    cma_service_facade = DeleteCMACaseService(
        cma_blaise_service, frs_case_allocation_service
    )
    cma_service_facade.remove_case_from_cma(totalmobile_case)


def create_visit_request_handler(request, current_app):
    data = request.get_json()
    totalmobile_frs_case = TotalMobileIncomingFRSRequestModel.import_request(data)

    frs_case_allocation_service = FRSCaseAllocationService(
        cma_blaise_service=current_app.cma_blaise_service
    )
    frs_case_allocation_service.create_case(totalmobile_frs_case)


def force_recall_visit_request_handler(request, current_app):
    data = request.get_json()
    totalmobile_unallocation_frs_case = (
        TotalMobileIncomingFRSUnallocationRequestModel.import_request(data)
    )
    frs_case_allocation_service = FRSCaseAllocationService(
        cma_blaise_service=current_app.cma_blaise_service
    )
    frs_case_allocation_service.unallocate_case(totalmobile_unallocation_frs_case)
    return


def get_survey_type(data):
    try:
        return data["result"]["association"]["reference"][:3]
    except KeyError:
        return None


def verify_survey_type(survey_type):
    if survey_type is None:
        raise MissingReferenceError("Reference field is missing in association block")
    if not isinstance(survey_type, str) or len(survey_type) < 3:
        raise BadReferenceError("Reference field in association block is invalid")
    if survey_type not in ("LMS", "FRS"):
        logging.error(f"survey_type of '{survey_type}' is invalid")
        raise SurveyDoesNotExistError
