from flask import Blueprint, current_app, jsonify, request

from app.auth import auth
from app.exceptions.custom_exceptions import (
    BadReferenceError,
    MissingReferenceError,
    QuestionnaireCaseDoesNotExistError,
    QuestionnaireDoesNotExistError, InvalidTotalmobileUpdateRequestException,
)
from app.handlers.total_mobile_handler import (
    complete_visit_request_handler,
    submit_form_result_request_handler,
    update_visit_status_request_handler,
)

incoming = Blueprint("incoming", __name__, url_prefix="/bts")


@incoming.route("/updatevisitstatusrequest", methods=["POST"])
@auth.login_required
def update_visit_status_request():
    update_visit_status_request_handler(request)


@incoming.route("/submitformresultrequest", methods=["POST"])
@auth.login_required
def submit_form_result_request():
    try:
        submit_form_result_request_handler(request, current_app.questionnaire_service)
        return "ok"
    except (MissingReferenceError, BadReferenceError, InvalidTotalmobileUpdateRequestException):
        return "Missing/invalid reference in request", 400
    except QuestionnaireDoesNotExistError:
        return "Questionnaire does not exist in Blaise", 404
    except QuestionnaireCaseDoesNotExistError:
        return "Case does not exist in Blaise", 404


@incoming.route("/completevisitrequest", methods=["POST"])
@auth.login_required
def complete_visit_request():
    complete_visit_request_handler(request)


@incoming.route("/<version>/health", methods=["GET"])
def health_check(version):
    return jsonify({"healthy": True})
