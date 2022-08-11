import os
from appconfig import Config
import flask

from dotenv import load_dotenv
from app.app import load_config, setup_app

import cloud_functions.create_totalmobile_job
import cloud_functions.create_questionnaire_case_tasks
import cloud_functions.check_questionnaire_release_date


def create_totalmobile_job(request: flask.Request) -> str:
    return cloud_functions.create_totalmobile_job.create_totalmobile_job(request)


def create_questionnaire_case_tasks(request: flask.Request) -> str:
    config = Config.from_env()
    return cloud_functions.create_questionnaire_case_tasks.create_questionnaire_case_tasks(request, config)


def check_questionnaire_release_date(_event, _context) -> str:
    return cloud_functions.check_questionnaire_release_date.check_questionnaire_release_date()


if os.path.isfile("./.env"):
    print("Loading environment variables from dotenv file")
    load_dotenv()

app = setup_app()
load_config(app)


if __name__ == "__main__":
    print("Running Flask application")
    app.run(host="0.0.0.0", port=5011)
