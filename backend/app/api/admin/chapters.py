from flask import jsonify, request
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.api.admin import admin_bp
from app.auth.decorators import admin_required, user_required
from app.extensions import db
from app.models.chapter import Chapter
from app.models.subject import Subject
from app.schema.chapter_schema import (
    ChapterCreateSchema,
    ChapterResponseSchema,
    ChapterUpdateSchema,
)


# Create Chapters (Checked)
@admin_bp.route("/subjects/<int:subject_id>/chapters", methods=["POST"])
@admin_required
def create_chapter(subject_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        print(subject)

        json_data = request.get_json()
        chapter_data = ChapterCreateSchema(**json_data)

        chapter = Chapter()
        chapter.subject_id = subject_id
        chapter.name = chapter_data.name
        chapter.description = chapter_data.description

        db.session.add(chapter)
        db.session.commit()

        response_data = ChapterResponseSchema.model_validate(chapter)
        return jsonify(response_data.model_dump()), 201

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# List of all Chapters in a Subject (Checked)
@admin_bp.route("/subjects/<int:subject_id>/chapters", methods=["GET"])
@user_required
def list_chapters(subject_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        print(subject)

        chapters = Chapter.query.filter_by(subject_id=subject_id).all()
        chapters_data = [
            ChapterResponseSchema.model_validate(chapter).model_dump()
            for chapter in chapters
        ]
        return jsonify(chapters_data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# List of all Chapters
@admin_bp.route("/chapters", methods=["GET"])
@user_required
def list_of_chapters():
    try:
        chapters = Chapter.query.all()
        chapters_data = [
            ChapterResponseSchema.model_validate(chapter).model_dump()
            for chapter in chapters
        ]
        return jsonify(chapters_data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# Update Chapters (Checked)
@admin_bp.route("/chapters/<int:chapter_id>", methods=["PUT"])
@admin_required
def update_chapter(chapter_id):
    try:
        chapter = Chapter.query.get_or_404(chapter_id)
        json_data = request.get_json()
        update_data = ChapterUpdateSchema(**json_data)

        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(chapter, field, value)

        db.session.commit()

        response_data = ChapterResponseSchema.model_validate(chapter)
        return jsonify(response_data.model_dump()), 200

    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# Delete Chapters
@admin_bp.route("/chapters/<int:chapter_id>", methods=["DELETE"])
@admin_required
def delete_chapter(chapter_id):
    try:
        chapter = Chapter.query.get_or_404(chapter_id)
        db.session.delete(chapter)
        db.session.commit()

        return jsonify({"message": "Chapter deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
