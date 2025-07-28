from config import Config
from flask import Flask
from flask_cors import CORS
from flask_security.core import Security
from flask_security.datastore import SQLAlchemyUserDatastore

from app.auth.jwt_manager import jwt
from app.celery_app import create_celery_app
from app.extensions import db, login_manager
from app.models.role import Role
from app.models.user import User


def create_admin_user():
    admin_role = Role.query.filter_by(name="admin").first()
    if not admin_role:
        admin_role = Role()
        admin_role.name = "admin"
        admin_role.description = "Administrator role"

        db.session.add(admin_role)
        db.session.commit()

    # Create admin if it doesn't exist
    admin_user = User.query.filter_by(email="admin@quizmaster.com").first()
    if not admin_user:
        admin_user = User()
        admin_user.email = "admin@quizmaster.com"
        admin_user.full_name = "Quiz Master Admin"
        admin_user.password = "Admin@123"
        admin_user.active = True
        admin_user.qualification = "Administrator"

        admin_user.roles.append(admin_role)
        db.session.add(admin_user)
        db.session.commit()

        print("Admin user created successfully")
        print(f"Email: {admin_user.email}")
        print("Password: Admin@123")
    else:
        if admin_role not in admin_user.roles:
            admin_user.roles.append(admin_role)
            # db.session.add(admin_user)
            db.session.commit()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Intialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Initialize jwt
    jwt.init_app(app)

    CORS(app)

    # from app import models
    from app.api import bp as api_blueprint
    from app.api.admin import admin_bp
    from app.auth import auth_bp

    app.register_blueprint(api_blueprint)
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        create_admin_user()
    return app
