from flask import Flask

from app.auth import auth
from app.endpoints import incoming

from .config import Config

app = Flask(__name__)
config = Config.from_env()
app.config["user"] = config.user
app.config["password_hash"] = config.password_hash

app.auth = auth

app.register_blueprint(incoming)
