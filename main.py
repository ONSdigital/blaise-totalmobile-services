import os
import flask


from app.app import app, load_config, setup_app
from dotenv import load_dotenv

from cloud_functions.create_instrument_case_tasks import (
    create_case_tasks_for_instrument,
)

from cloud_functions.create_job import (
    create_totalmobile_job as create_totalmobile_job_exectutor,
)


def create_totalmobile_job(request: flask.Request) -> str:
    return create_totalmobile_job_exectutor(request)


def create_instrument_case_tasks(request: flask.Request) -> str:
    return create_case_tasks_for_instrument(request)


if os.path.isfile("./.env"):
    print("Loading environment variables from dotenv file")
    load_dotenv()

load_config(app)
setup_app(app)

if __name__ == "__main__":
    print("Running Flask application")
    app.run(host="0.0.0.0", port=5011)
