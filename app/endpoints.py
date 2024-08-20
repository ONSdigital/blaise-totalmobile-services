import logging

from flask import Blueprint, current_app, jsonify, request

from app.auth import auth
from app.exceptions.custom_exceptions import (
    BadReferenceError,
    InvalidTotalmobileUpdateRequestException,
    MissingReferenceError,
    QuestionnaireCaseDoesNotExistError,
    QuestionnaireCaseError,
    QuestionnaireDoesNotExistError,
)
from app.handlers.totalmobile_incoming_handler import (
    complete_visit_request_handler,
    submit_form_result_request_handler,
    update_visit_status_request_handler,
)
from services.update.mappers.blaise_update_case_mapper_service import (
    BlaiseUpdateCaseMapperService,
)
from services.update.update_case_service import UpdateCaseService

incoming = Blueprint("incoming", __name__, url_prefix="/bts")


@incoming.after_request
def add_header(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=86400"
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Frame-Options"] = "DENY"
    return response


@incoming.route("/submitformresultrequest", methods=["POST"])
@auth.login_required
def submit_form_result_request():
    logging.info(f"Incoming request via the 'submitformresultrequest' endpoint")
    try:
        update_case_service = UpdateCaseService(
            blaise_service=current_app.blaise_service,
            mapper_service=BlaiseUpdateCaseMapperService(),
        )
        submit_form_result_request_handler(request, update_case_service)
        return "ok"
    except (MissingReferenceError, BadReferenceError):
        return "Missing/invalid reference in request", 400
    except InvalidTotalmobileUpdateRequestException:
        return "Request appears to be malformed", 400
    except QuestionnaireDoesNotExistError:
        return "Questionnaire does not exist in Blaise", 404
    except QuestionnaireCaseDoesNotExistError:
        return "Case does not exist in Blaise", 404
    except QuestionnaireCaseError:
        return "Error trying to get case in Blaise", 500


@incoming.route("/completevisitrequest", methods=["POST"])
@auth.login_required
def complete_visit_request():
    logging.info(f"Incoming request via the 'completevisitrequest' endpoint")
    complete_visit_request_handler(request)
    return "ok"


@incoming.route("/updatevisitstatusrequest", methods=["POST"])
@auth.login_required
def update_visit_status_request():
    logging.info(f"Incoming request via the 'updatevisitstatusrequest' endpoint")
    update_visit_status_request_handler(request)
    return "ok"


@incoming.route("/<version>/health", methods=["GET"])
def health_check(version):
    return jsonify({"healthy": True})
