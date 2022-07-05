import os
import flask

from dotenv import load_dotenv

from app.app import app, load_config, setup_app

import cloud_functions.create_totalmobile_job
import cloud_functions.check_questionnaire_release_date
import cloud_functions.create_questionnaire_case_tasks


def check_questionnaire_release_date() -> str:
    return cloud_functions.check_questionnaire_release_date.check_questionnaire_release_date()


def create_totalmobile_job(request: flask.Request) -> str:
    return cloud_functions.create_totalmobile_job.create_totalmobile_job(request)


def create_questionnaire_case_tasks(request: flask.Request) -> str:
    return cloud_functions.create_questionnaire_case_tasks.create_questionnaire_case_tasks(request)


if os.path.isfile("./.env"):
    print("Loading environment variables from dotenv file")
    load_dotenv()

load_config(app)
setup_app(app)

if __name__ == "__main__":
    print("Running Flask application")
    app.run(host="0.0.0.0", port=5011)
