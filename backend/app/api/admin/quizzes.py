import json
from datetime import timedelta

from flask import current_app, jsonify, request
from pydantic import ValidationError

from app.api.admin import admin_bp
from app.auth.decorators import admin_required, user_required
from app.extensions import db, redis_client
from app.models.chapter import Chapter
from app.models.question import Question
from app.models.quiz import Quiz
from app.models.subject import Subject
from app.schema.quiz_schema import (
    QuizCreateSchema,
    QuizResponseSchema,
    QuizUpdateSchema,
)


@admin_bp.route(
    "/subjects/<int:subject_id>/chapters/<int:chapter_id>/quizzes", methods=["POST"]
)
@admin_required
def create_quiz(subject_id, chapter_id):
    try:
        chapter = Chapter.query.get_or_404(chapter_id)

        json_data = request.get_json()
        quiz_data = QuizCreateSchema(**json_data)

        quiz = Quiz()
        quiz.chapter_id = chapter_id
        quiz.subject_id = subject_id
        quiz.title = quiz_data.title
        quiz.date_of_quiz = quiz_data.date_of_quiz
        quiz.scheduled_at = quiz_data.scheduled_at
        quiz.duration = quiz_data.duration
        quiz.remarks = quiz_data.remarks

        db.session.add(quiz)
        db.session.commit()

        response_data = QuizResponseSchema.model_validate(quiz)

        return jsonify(response_data.model_dump()), 201

    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route(
    "/subjects/<int:subject_id>/chapters/<int:chapter_id>/quizzes", methods=["GET"]
)
@user_required
def list_quizzes_by_chapter(subject_id, chapter_id, current_user_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        chapter = Chapter.query.get_or_404(chapter_id)

        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        quizzes_data = [
            QuizResponseSchema.model_validate(quiz).model_dump() for quiz in quizzes
        ]
        return jsonify(quizzes_data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route("/subjects/<int:subject_id>/quizzes", methods=["GET"])
@user_required
def list_quizzes_by_subject(subject_id, current_user_id):
    try:
        subject = Subject.query.get_or_404(subject_id)

        quizzes = Quiz.query.filter_by(subject_id=subject_id).all()
        quizzes_data = [
            QuizResponseSchema.model_validate(quiz).model_dump() for quiz in quizzes
        ]
        return jsonify(quizzes_data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route("/quizzes", methods=["GET"])
@user_required
def list_all_quizzes(current_user_id):
    try:
        cached_quizzes = redis_client.get("all_quizzes")

        if cached_quizzes:
            return jsonify(json.loads(cached_quizzes)), 200

        quizzes = Quiz.query.all()
        quizzes_data = [
            QuizResponseSchema.model_validate(quiz).model_dump() for quiz in quizzes
        ]

        redis_client.setex(
            "all_quizzes", timedelta(hours=1), json.dumps(quizzes_data, default=str)
        )

        print(quizzes_data)
        return jsonify(quizzes_data), 200
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route("/quizzes/<int:quiz_id>", methods=["PUT"])
@admin_required
def update_quiz(quiz_id):
    try:
        quiz = Quiz.query.get_or_404(quiz_id)

        json_data = request.get_json()
        update_data = QuizUpdateSchema(**json_data)

        for field, value in update_data.model_dump(exclude_unset=True).items():
            if field == "duration" and value is not None:
                setattr(quiz, field, timedelta(minutes=value))
            else:
                setattr(quiz, field, value)
        db.session.commit()

        response_data = QuizResponseSchema.model_validate(quiz)
        return jsonify(response_data.model_dump()), 200

    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route("/quizzes/<int:quiz_id>", methods=["DELETE"])
@admin_required
def delete_quiz(quiz_id):
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        db.session.delete(quiz)
        db.session.commit()

        return jsonify({"message": "Quiz deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
