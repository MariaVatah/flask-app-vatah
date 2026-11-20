import os
from flask import Flask

app = Flask(__name__)

app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "lab4-development-secret-key"
)

from . import views

from app.users import users_bp
app.register_blueprint(users_bp)

from app.products import products_bp
app.register_blueprint(products_bp)