from flask import Blueprint, jsonify, request

from app.auth import auth
from app.handlers.total_mobile_handler import (
    complete_visit_request_handler,
    submit_form_result_request_handler,
    update_visit_status_request_handler,
)

incoming = Blueprint("incoming", __name__, url_prefix="/ons/totalmobile-incoming")


@incoming.route("/UpdateVisitStatusRequest", methods=["POST"])
@auth.login_required
def update_visit_status_request():
    return jsonify(update_visit_status_request_handler(request))


@incoming.route("/SubmitFormResultRequest", methods=["POST"])
@auth.login_required
def submit_form_result_request():
    return jsonify(submit_form_result_request_handler(request))


@incoming.route("/CompleteVisitRequest", methods=["POST"])
@auth.login_required
def complete_visit_request():
    return jsonify(complete_visit_request_handler(request))
