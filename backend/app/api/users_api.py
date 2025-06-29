from datetime import datetime, timedelta

from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from pydantic import ValidationError
from sqlalchemy import func

from app.api import bp
from app.auth.decorators import user_required
from app.extensions import db
from app.models.chapter import Chapter
from app.models.question import Question
from app.models.quiz import Quiz
from app.models.score import Score
from app.models.user_answer import UserAnswer


# List of quizzes by chapters
@bp.route("/chapters/<int:chapter_id>/quizzes", methods=["GET"])
@user_required
def list_quizzes(chapter_id, current_user_id):
    try:
        # current_user_id = get_jwt_identity()
        chapter = Chapter.query.get_or_404(chapter_id)

        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        quizzes_data = []

        for quiz in quizzes:

            # Check if user has attempted this quiz
            user_score = Score.query.filter_by(
                quiz_id=quiz.id, user_id=current_user_id
            ).first()

            quiz_data = {
                "id": quiz.id,
                "title": quiz.title,
                "date_of_quiz": quiz.date_of_quiz.isoformat(),
                "scheduled_at": quiz.scheduled_at.isoformat(),
                "duration": quiz.duration.total_seconds() / 60,
                "remarks": quiz.remarks,
                "total_questions": len(quiz.questions),
                "attempted": user_score is not None,
                "last_score": user_score.total_score if user_score else None,
                "last_attempted": (
                    user_score.timestamp.isoformat() if user_score else None
                ),
            }
            quizzes_data.append(quiz_data)

        return (
            jsonify(
                {
                    "chapter": {
                        "id": chapter.id,
                        "name": chapter.name,
                        "subject_name": chapter.subject.name,
                    },
                    "quizzes": quizzes_data,
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# Get quiz for attempt
@bp.route("/quizzes/<int:quiz_id>", methods=["GET"])
@user_required
def get_quiz(quiz_id):
    try:
        # current_user_id = get_jwt_identity()
        quiz = Quiz.query.get_or_404(quiz_id)

        # Check if quiz is scheduled and not exxpired
        now = datetime.now()
        if quiz.scheduled_at > now:
            return jsonify({"error": "Quiz is not yet available"}), 400

        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        questions_data = []

        for question in questions:
            question_data = {
                "id": question.id,
                "statement": question.statement,
                "option1": question.option1,
                "option2": question.option2,
                "option3": question.option3,
                "option4": question.option4,
            }
            questions_data.append(question_data)

        quiz_data = {
            "id": quiz.id,
            "title": quiz.title,
            "duration": quiz.duration.total_seconds() / 60,
            "remarks": quiz.remarks,
            "chapter_name": quiz.chapter_name,
            "subject_name": quiz.subject_name,
            "total_questions": len(questions_data),
            "questions": questions_data,
        }

        return jsonify(quiz_data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# Submit quiz and calculate score
@bp.route("/quizzes/<int:quiz_id>/submit", methods=["POST"])
@user_required
def submit_quiz(quiz_id, current_user_id):
    try:
        # current_user_id = get_jwt_identity()
        quiz = Quiz.query.get_or_404(quiz_id)
        # print(quiz)

        json_data = request.get_json()
        answers = json_data.get("answers", {})

        # Get all questions for this quiz
        questions = Question.query.filter_by(quiz_id=quiz_id).all()

        correct_count = 0
        wrong_count = 0
        unattempted_count = 0

        # Process each question
        for question in questions:
            selected_option = answers.get(str(question.id))

            # Save user answer
            user_answer = UserAnswer()
            user_answer.user_id = current_user_id
            user_answer.quiz_id = quiz_id
            user_answer.question_id = question.id
            user_answer.selected_option = selected_option

            db.session.add(user_answer)

            # Calculate score
            if selected_option is None:
                unattempted_count = unattempted_count + 1
            elif selected_option == question.correct_option:
                correct_count = correct_count + 1
            else:
                wrong_count = wrong_count + 1

        # Calculate total score
        total_score = correct_count * 4 - wrong_count * 1

        # Save Score
        score = Score()
        score.quiz_id = quiz_id
        score.user_id = current_user_id
        score.correct_count = correct_count
        score.wrong_count = wrong_count
        score.unattempted_count = unattempted_count
        score.total_score = total_score
        score.timestamp = datetime.now()
        score.status = "completed"

        db.session.add(score)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Quiz submitted successfully",
                    "score": {
                        "correct_count": correct_count,
                        "wrong_count": wrong_count,
                        "unattempted_count": unattempted_count,
                        "total_score": total_score,
                        "total_questions": len(questions),
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@bp.route("/my-scores", methods=["GET"])
@user_required
def get_scores(current_user_id):
    try:
        # current_user_id = get_jwt_identity()
        scores = (
            Score.query.filter_by(user_id=current_user_id)
            .order_by(Score.timestamp.desc())
            .all()
        )

        scores_data = []

        for score in scores:
            score_data = {
                "id": score.id,
                "quiz_id": score.quiz_id,
                "quiz_title": score.quiz.title,
                "chapter_name": score.quiz.chapter.name,
                "subject_name": score.quiz.subject.name,
                "correct_count": score.correct_count,
                "wrong_coung": score.wrong_count,
                "unattempted_count": score.unattempted_count,
                "total_score": score.total_score,
                "timestamp": score.timestamp.isoformat(),
                "status": score.status,
            }
            scores_data.append(score_data)

        return jsonify(scores_data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@bp.route("/dashboard/stats", methods=["GET"])
@user_required
def get_user_dashboard(current_user_id):
    try:

        # Get user's statistics
        total_quizzes_attempted = Score.query.filter_by(user_id=current_user_id).count()

        if total_quizzes_attempted > 0:
            avg_score = (
                db.session.query(func.avg(Score.total_score))
                .filter_by(user_id=current_user_id)
                .scalar()
            )

            best_score = (
                db.session.query(func.max(Score.total_score))
                .filter_by(user_id=current_user_id)
                .scalar()
            )

            recent_attempts = (
                Score.query.filter_by(user_id=current_user_id)
                .order_by(Score.timestamp.desc())
                .limit(5)
                .all()
            )

            recent_attempts_data = []
            for attempt in recent_attempts:
                recent_attempt_data = {
                    "quiz_title": attempt.quiz.title,
                    "subject_name": attempt.quiz.subject.name,
                    "total_score": attempt.total_score,
                    "timestamp": attempt.timestamp.isoformat(),
                }
                recent_attempts_data.append(recent_attempt_data)
        else:
            avg_score = 0
            best_score = 0
            recent_attempts_data = []

        # Available quizzes count
        total_available_quizzes = Quiz.query.count()

        stats = {
            "total_quizzes_attempted": total_quizzes_attempted,
            "total_available_quizzes": total_available_quizzes,
            "average_score": float(avg_score) if avg_score else 0,
            "best_score": best_score or 0,
            "recent_attempts": recent_attempts_data,
        }

        return jsonify(stats), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
