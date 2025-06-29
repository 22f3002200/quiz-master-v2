from flask import jsonify
from sqlalchemy import func

from app.api.admin import admin_bp
from app.models.chapter import Chapter
from app.models.question import Question
from app.models.quiz import Quiz
from app.models.score import Score
from app.models.subject import Subject
from app.models.user import User


@admin_bp.route("/dashboard/summary", methods=["GET"])
def get_dashboard_summary():
    try:
        # counts
        total_users = User.query.count()
        total_subjects = Subject.query.count()
        total_chapters = Chapter.query.count()
        total_quizzes = Quiz.query.count()
        total_questions = Question.query.count()
        total_attempts = Score.query.count()

        # Recent activity
        recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
        recent_quizzes = Quiz.query.order_by(Quiz.created_at.desc()).limit(5).all()

        # Summary
        summary = {
            "totals": {
                "users": total_users,
                "subjects": total_subjects,
                "chapters": total_chapters,
                "quizzes": total_quizzes,
                "questions": total_questions,
                "quiz_attempt": total_attempts,
            },
            "recent_users": [
                {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "created_at": user.created_at.isoformat(),
                }
                for user in recent_users
            ],
            "recent_quizzes": [
                {
                    "id": quiz.id,
                    "title": quiz.title,
                    "subject_name": quiz.subject_name if quiz.subject else None,
                    "chapter_name": quiz.chapter_name if quiz.chapter else None,
                    "created_at": quiz.created_at.isoformat(),
                }
                for quiz in recent_quizzes
            ],
        }
        return jsonify(summary), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route("/analytics/quiz-performance", methods=["GET"])
def get_quiz_performance():
    try:
        quiz_stat = (
            Quiz.query.outerjoin(Score)
            .with_entities(
                Quiz.id,
                Quiz.title,
                Quiz.subject_id,
                func.count(Score.id).label("total_attempts"),
                func.avg(Score.total_score).label("avg_score"),
                func.max(Score.total_score).label("max_score"),
                func.min(Score.total_score).label("min_score"),
            )
            .group_by(Quiz.id)
            .all()
        )

        performance_data = []
        for stat in quiz_stat:
            performance_data.append(
                {
                    "quiz_id": stat.id,
                    "quiz_title": stat.title,
                    "subject_id": stat.subject_id,
                    "total_attempts": stat.total_attempts or 0,
                    "average_score": float(stat.avg_score) if stat.avg_score else 0,
                    "max-score": stat.max_score or 0,
                    "min_score": stat.min_score or 0,
                }
            )

        return jsonify(performance_data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


@admin_bp.route("/analytics/user-performance", methods=["GET"])
def get_user_performance():
    try:
        user_stats = (
            User.query.outerjoin(Score)
            .with_entities(
                User.id,
                User.full_name,
                User.email,
                func.count(Score.id).label("total_attempts"),
                func.avg(Score.total_score).label("avg_score"),
                func.max(Score.total_score).label("max_score"),
            )
            .group_by(User.id)
            .order_by(func.avg(Score.total_score).desc())
            .all()
        )

        performance_data = []
        for stat in user_stats:
            performance_data.append(
                {
                    "user_id": stat.id,
                    "full_name": stat.full_name,
                    "email": stat.email,
                    "total_attemps": stat.total_attempts,
                    "average_score": float(stat.avg_score) if stat.avg_score else 0,
                    "max_score": stat.max_score or 0,
                }
            )

        return jsonify(performance_data), 200

    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# @admin_bp.route("/analytics/monthly-stats", methods=["GET"])
# def get_monthly_stats():
#     try:
#         from datetime import datetime, timedelta

#         # Get current month stats
#         current_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)

#         # Quiz attempts this month
#         monthly_attempts = Score.query.filter(
#             Score.timestamp >= current_month
#         ).count()
