from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import (
    DevelopmentConfig,
    TestingConfig,
    ProductionConfig
)

from sqlalchemy import MetaData

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()

configurations = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig
}


def create_app(config_name="development"):
    app = Flask(__name__)

    app.config.from_object(
        configurations.get(config_name, DevelopmentConfig)
    )

    import os
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from app.users import users_bp
    from app.products import products_bp
    from app.posts import posts_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(posts_bp)

    from app.posts import models
    from app.products import models as product_models
    from app import views

    app.add_url_rule(
        "/",
        endpoint="homepage",
        view_func=views.homepage
    )

    app.add_url_rule(
        "/resume",
        endpoint="resume",
        view_func=views.resume
    )

    app.add_url_rule(
        "/contacts",
        endpoint="contacts",
        view_func=views.contacts,
        methods=["GET", "POST"]
    )

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    return app