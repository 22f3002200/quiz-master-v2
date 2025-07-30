import json
from datetime import timedelta

from flask import jsonify, request
from pydantic import ValidationError

from app.api.admin import admin_bp
from app.auth.decorators import admin_required, user_required
from app.extensions import db, redis_client
from app.models.subject import Subject
from app.schema.subject_schema import (
    SubjectCreateSchema,
    SubjectResponseSchema,
    SubjectUpdateSchema,
)


# Create subjects (Checked)
@admin_bp.route("/subjects", methods=["POST"])
@admin_required
def create_subject():
    try:
        json_data = request.get_json()
        subject_data = SubjectCreateSchema(**json_data)
        subject = Subject()
        subject.name = subject_data.name
        subject.description = subject_data.description
        db.session.add(subject)
        db.session.commit()

        response_date = SubjectResponseSchema.model_validate(subject)
        return jsonify(response_date.model_dump()), 201

    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# List of all subjects (Checked)
@admin_bp.route("/subjects", methods=["GET"])
@user_required
def list_subjects(**kwargs):
    try:
        # cached_subjects = redis_client.get("all_subjects")

        # if cached_subjects:
        #     return jsonify(json.loads(cached_subjects)), 200

        subjects = Subject.query.all()
        subjects_data = [
            SubjectResponseSchema.model_validate(subject).model_dump()
            for subject in subjects
        ]

        # redis_client.setex(
        #     "all_subjects", timedelta(hours=1), json.dumps(subjects_data, default=str)
        # )

        return jsonify(subjects_data), 200

    except Exception as e:
        return jsonify({"error": "Internal Error", "details": str(e)}), 500


# Update Subjects (Checked)
@admin_bp.route("/subjects/<int:subject_id>", methods=["PUT"])
@admin_required
def update_subject(subject_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        json_data = request.get_json()
        update_data = SubjectUpdateSchema(**json_data)

        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(subject, field, value)

        db.session.commit()

        response_data = SubjectResponseSchema.model_validate(subject)
        return jsonify(response_data.model_dump()), 200

    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# Delete Subjects (Checked)
@admin_bp.route("/subjects/<int:subject_id>", methods=["DELETE"])
@admin_required
def delete_subject(subject_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        db.session.delete(subject)
        db.session.commit()

        return jsonify({"message": "Subject deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
