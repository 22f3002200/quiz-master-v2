from datetime import datetime, timedelta

from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from pydantic import ValidationError
from werkzeug.security import check_password_hash

from app.auth import auth_bp
from app.extensions import db
from app.models.user import User
from app.schema.auth_schema import ChangePasswordSchema, LoginSchema, RegisterSchema


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        json_data = request.get_json()
        register_data = RegisterSchema(**json_data)

        # Check if User exists or not
        existing_user = User.query.filter_by(email=register_data.email).first()
        if existing_user:
            return jsonify({"msg": "User with this email already exists"}), 409

        # Create new user
        user = User()
        user.email = register_data.email
        user.full_name = register_data.full_name
        user.qualification = register_data.qualification
        user.dob = register_data.dob
        user.active = True
        user.password = register_data.password

        db.session.add(user)
        db.session.commit()

        # Create tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return (
            jsonify(
                {
                    "msg": "User registered successfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "full_name": user.full_name,
                        "active": user.active,
                    },
                }
            ),
            201,
        )

    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Registration failed", "error": str(e)}), 500
