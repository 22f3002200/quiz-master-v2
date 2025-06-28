from datetime import datetime, timedelta
from flask import jsonify, request
from flask_jwt_extended import get_jwt_identity
from app.auth.decorators import user_required
from pydantic import ValidationError
from sqlalchemy import func

from app.api import bp
from app.extensions import db
from app.models.chapter import Chapter
from app.models.quiz import Quiz
from app.models.score import Score

# List of quizzes by chapters
@bp.route("/chapters/<int:chapter_id>/quizzes", methods=["GET"])
@user_required
def list_quizzes(chapter_id):
    try:
        current_user_id = get_jwt_identity()
        chapter = Chapter.query.get_or_404(chapter_id)

        quizzes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        quizzes_data = []

        for quiz in quizzes:
            # Check if user has attempted this quiz
            user_score = Score.query.filter_by(quiz_id=quiz.id, user_id=current_user_id).first()

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
                "last_attempted": user_score.timestamp.isoformat() if user_score else None
            }
            quizzes_data.append(quiz_data)
        
        return jsonify({
            "chapter": {
                "id": chapter.id,
                "name": chapter.name
                "subject_name": chapter.subject.name
            },
            "quizzes": quizzes_data
        }), 200
    
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500