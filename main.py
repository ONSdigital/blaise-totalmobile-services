import os

import flask
from dotenv import load_dotenv

from cloud_functions.create_instrument_case_tasks import (
    create_case_tasks_for_instrument,
)
from cloud_functions.create_job import create_totalmobile_job

if os.path.isfile("./.env"):
    print("Loading environment variables from dotenv file")
    load_dotenv()


def create_totalmobile_job(request: flask.Request) -> str:
    return create_totalmobile_job(request)


def create_instrument_case_tasks(request: flask.Request) -> str:
    return create_case_tasks_for_instrument(request)
