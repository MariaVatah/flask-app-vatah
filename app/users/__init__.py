from flask import Blueprint
import os

users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users",
    template_folder=os.path.join(
        os.path.dirname(__file__), "templates"
    )
)

from app.users import views
