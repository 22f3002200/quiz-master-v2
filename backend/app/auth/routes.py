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
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash

from app.auth import auth_bp
from app.extensions import db
from app.models.user import User
from app.schema.auth_schema import ChangePasswordSchema, LoginSchema, RegisterSchema
from app.schema.user_schema import UserResponseSchema, UserUpdateSchema


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


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        json_data = request.get_json()
        login_data = LoginSchema(**json_data)

        # Find user
        user = User.query.filter_by(email=login_data.email).first()

        if not user or not user.check_password(login_data.password):
            return jsonify({"msg": "Invalid email or password"}), 401

        # Create Token
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return (
            jsonify(
                {
                    "msg": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "full_name": user.full_name,
                    },
                }
            ),
            200,
        )

    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Login failed", "error": str(e)}), 500


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({"msg": "User not found"}), 404

        new_access_token = create_access_token(identity=current_user_id)

        return jsonify({"access_token": new_access_token}), 200

    except Exception as e:
        return ({"msg": "Token refresh failed", "error": str(e)}), 500


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:  # have to remove token from client side using javascript
        return jsonify({"msg": "Successfully logged out"})

    except Exception as e:
        return jsonify({"msg": "Internal server error", "error": str(e)}), 500


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({"msg": "User not found"}), 404

        return (
            jsonify(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "full_name": user.full_name,
                        "qualification": user.qualification,
                        "dob": user.dob.isoformat() if user.dob else None,
                        "created_at": user.created_at.isoformat(),
                    }
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"msg": "Internal server error", "error": str(e)}), 500


@auth_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_profile():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        json_data = request.get_json()
        update_data = UserUpdateSchema(**json_data)

        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        db.session.commit()

        response_data = UserResponseSchema.model_validate(user)
        print(response_data)
        return jsonify(response_data.model_dump()), 200

    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email already exists"}), 409
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@auth_bp.route("/password", methods=["POST"])
@jwt_required()
def change_password():
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({"error": "User not found"}), 404

        json_data = request.get_json()
        change_data = ChangePasswordSchema(**json_data)

        if not user.check_password(change_data.current_password):
            return jsonify({"error": "Old password is incorrect"}), 400
        user.password = change_data.new_password
        db.session.commit()

        return jsonify({"msg": "Password changed successfully"}), 400
    except ValidationError as e:
        return jsonify({"msg": "Validation error", "errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"msg": "Login failed", "error": str(e)}), 500
