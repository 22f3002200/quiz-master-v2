from config import Config
from flask import Flask
from flask_security.core import Security
from flask_security.datastore import SQLAlchemyUserDatastore

from app.celery_app import make_celery
from app.extensions import db, login_manager
from app.models.role import Role
from app.models.user import User


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Intialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Intialize Celery
    celery = make_celery(app)
    app.celery = celery

    # setup flask-security
    # user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    # # security = Security(app, user_datastore)

    # from app import models
    from app.api import bp as api_blueprint
    from app.api.admin import admin_bp

    # from app.api.auth import auth_bp

    app.register_blueprint(api_blueprint)
    app.register_blueprint(admin_bp)
    # app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
    return app
