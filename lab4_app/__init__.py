
from flask import Flask
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "lab4-development-secret-key"

app.template_folder = os.path.join(
    os.path.dirname(__file__),
    "templates"
)

app.static_folder = os.path.join(
    os.path.dirname(__file__),
    "static"
)

from lab4_app import routes
