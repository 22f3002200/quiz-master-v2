from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.user import User


def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({"msg": "User not found"}), 404

        # check if user has admin role
        admin_role = next((role for role in user.roles if role.name == "admin"), None)
        if not admin_role:
            return jsonify({"msg": "Admin access required"}), 403

        return f(*args, kwargs)

    return decorated_function


def user_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({"msg": "User not found"}), 404

        return f(*args, current_user_id=current_user_id, **kwargs)

    return decorated_function


def role_required(role_name):
    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)

            if not user:
                return jsonify({"msg": "User not found"}), 404

            # chech if user has required role
            required_role = next(
                (role for role in user.roles if role.name == role_name), None
            )
            if not required_role:
                return jsonify({"msg": f"{role_name.title()} access required"}), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator
