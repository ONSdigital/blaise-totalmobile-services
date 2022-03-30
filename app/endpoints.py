from flask import request

from app import app
from app.handlers.total_mobile_handler import (
    update_visit_status_request_handler, submit_form_result_request_handler, complete_visit_request_handler)


@app.route("/ons/totalmobile-incoming/UpdateVisitStatusRequest", methods=["POST"])
def update_visit_status_request():
    update_visit_status_request_handler(request)


@app.route("/ons/totalmobile-incoming/SubmitFormResultRequest", methods=["POST"])
def submit_form_result_request():
    submit_form_result_request_handler(request)


@app.route("/ons/totalmobile-incoming/CompleteVisitRequest", methods=["POST"])
def complete_visit_request():
    complete_visit_request_handler(request)
