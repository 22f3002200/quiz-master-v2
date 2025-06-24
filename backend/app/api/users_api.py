from datetime import datetime

from flask import jsonify, request
from pydantic import ValidationError

from app.api import bp
from app.extensions import db
from app.models.user import User
from app.schema.user_schema import (
    UserCreateSchema,
    UserListResponseSchema,
    UserResponseSchema,
    UserUpdateSchema,
)

now = datetime.now()


@bp.route("/", methods=["GET"])
def root():
    return {"message": "Hello World"}


@bp.route("/users", methods=["POST"])
def create_user():
    try:
        json_data = request.get_json()
        user_data = UserCreateSchema(**json_data)

        user = User()
        user.email = user_data.email
        user.password = user_data.password_hash
        user.full_name = user_data.full_name
        user.qualification = user_data.qualification
        user.dob = user_data.dob
        user.active = user_data.active
        user.created_at = now
        # db.session.add(user)
        # db.session.commit()

        return jsonify({"email": user.email, "full_name": user.full_name})
    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400
