from flask import jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.api.admin import admin_bp
from app.extensions import db
from app.models.user import User
from app.schema.user_schema import (
    UserCreateSchema,
    UserListResponseSchema,
    UserResponseSchema,
    UserUpdateSchema,
)


# checked
@admin_bp.route("/users", methods=["POST"])
def create_user():
    try:
        json_data = request.get_json()
        print("🚀 Incoming data:", json_data)
        user_data = UserCreateSchema(**json_data)

        # Check for existing user
        existing_user = User.query.filter_by(email=user_data.email).first()
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 409

        user = User()
        user.email = user_data.email
        user.password_hash = user_data.password_hash
        user.full_name = user_data.full_name
        user.qualification = user_data.qualification
        user.dob = user_data.dob
        user.active = user_data.active

        db.session.add(user)
        db.session.commit()

        response_data = UserResponseSchema.model_validate(user)
        return jsonify(response_data.model_dump()), 201

    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "User with this email already exists"}), 409

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# checked
@admin_bp.route("/users", methods=["GET"])
def list_users():
    try:
        users = User.query.all()
        users_data = [
            UserListResponseSchema.model_validate(user).model_dump() for user in users
        ]
        # print(users_data)
        return (users_data), 200

    except Exception as e:
        return jsonify({"error": "Internal Error", "details": str(e)}), 500


# checked
@admin_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)

        response_data = UserResponseSchema.model_validate(user)
        return jsonify(response_data.model_dump()), 200

    except Exception as e:
        return jsonify({"error": "Internal Error", "details": str(e)}), 500


# checked
@admin_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        print(user)

        json_data = request.get_json()
        print(json_data)
        update_data = UserUpdateSchema(**json_data)
        print(update_data)

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


# checked
@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)

        # user.active = False
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"}), 204

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route("/users/<int:user_id>/scores", methods=["GET"])
def get_user_scores(user_id):
    try:
        user = User.query.get_or_404(user_id)
        scores = user.scores

        scores_data = []
        for score in scores:
            score_data = {
                "id": score.id,
                "quiz_id": score.quiz_id,
                "quiz_title": score.quiz.title if score.quiz else None,
                "correct_count": score.correct_count,
                "wrong_count": score.wrong_count,
                "unattempted_count": score.unattempted_count,
                "total_score": score.total_score,
                "timestamp": score.timestamp,
                "status": score.status,
            }
            scores_data.append(score_data)
        return (
            jsonify(
                {"user_id": user_id, "user_name": user.full_name, "scores": score_data}
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
