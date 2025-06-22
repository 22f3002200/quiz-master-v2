from flask import jsonify, request
from pydantic import ValidationError

from app.api.admin import admin_bp
from app.extensions import db
from app.models.question import Question
from app.models.quiz import Quiz
from app.schema.question_schema import (
    QuestionCreateSchema,
    QuestionResponseSchema,
    QuestionUpdateSchema,
)


@admin_bp.route("/quizzes/<int:quiz_id>/questions", methods=["POST"])
def create_question(quiz_id):
    try:
        quiz = Quiz.query.get_or_404(quiz_id)

        json_data = request.get_json()
        question_data = QuestionCreateSchema(**json_data)

        question = Question()
        question.quiz_id = quiz_id
        question.statement = question_data.statement
        question.option1 = question_data.option1
        question.option2 = question_data.option2
        question.option3 = question_data.option3
        question.option4 = question_data.option4
        question.correct_option = question_data.correct_option

        db.session.add(question)
        db.session.commit()

        response_data = QuestionResponseSchema.model_validate(question)
        return jsonify(response_data.model_dump()), 200

    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route("/quizzes/<int:quiz_id>/questions", methods=["GET"])
def list_question_by_quiz(quiz_id):
    try:
        quiz = Quiz.query.get_or_404(quiz_id)

        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        question_data = [
            QuestionResponseSchema.model_validate(question).model_dump()
            for question in questions
        ]

        return jsonify(question_data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route("/questions/<int:question_id>", methods=["GET"])
def get_question(question_id):
    try:
        question = Question.query.get_or_404(question_id)
        response_data = QuestionResponseSchema.model_validate(question)
        return jsonify(response_data.model_dump()), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route("/questions/<int:question_id>", methods=["PUT"])
def update_question(question_id):
    try:
        question = Question.query.get_or_404(question_id)

        json_data = request.get_json()
        update_data = QuestionUpdateSchema(**json_data)

        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(question, field, value)

        db.session.commit()

        response_data = QuestionResponseSchema.model_validate(question)
        return jsonify(response_data.model_dump()), 200

    except ValidationError as e:
        return jsonify({"error": "Validation error", "details": e.errors()}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question(question_id):
    try:
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()

        return jsonify({"message": "Question deleted successfully"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
