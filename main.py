import flask
import os

from cloud_functions.create_job import create_totalmobile_job
from dotenv import load_dotenv

if os.path.isfile("./.env"):
    print("Loading environment variables from dotenv file")
    load_dotenv()


def TestTMCreateJob(request: flask.Request) -> str:
    return create_totalmobile_job(request)
