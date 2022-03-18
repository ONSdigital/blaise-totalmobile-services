from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/ons/totalmobile-incoming/UpdateVisitStatusRequest", methods=["POST"])
def update_visit_status_request():
    return "<p>Hello, World!</p>"


@app.route("/ons/totalmobile-incoming/SubmitFormResultRequest", methods=["POST"])
def submit_form_result_request():
    return "<p>Hello, World!</p>"


@app.route("/ons/totalmobile-incoming/CompleteVisitRequest", methods=["POST"])
def complete_visit_request():
    return "<p>Hello, World!</p>"
