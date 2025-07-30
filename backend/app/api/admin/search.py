from flask import g, jsonify, request

from app.api.admin import admin_bp
from app.auth.decorators import user_required
from app.models.chapter import Chapter
from app.models.quiz import Quiz
from app.models.subject import Subject
from app.models.user import User


@admin_bp.route("/search", methods=["GET"])
@user_required
def search(current_user_id):
    term = request.args.get("term", "")
    area = request.args.get("area", "chapter,subject,quizzes")

    search_areas = [a.strip() for a in area.split(",")]
    results = {}

    if not term or not search_areas:
        return jsonify(results)

    if "chapter" in search_areas:
        chapters = Chapter.query.filter(Chapter.name.ilike(f"%{term}%")).all()
        results["chapters"] = [
            {"id": c.id, "name": c.name, "type": "chapter", "subject_id": c.subject_id}
            for c in chapters
        ]

    if "subject" in search_areas:
        subjects = Subject.query.filter(Subject.name.ilike(f"%{term}%")).all()
        results["subjects"] = [
            {"id": s.id, "name": s.name, "type": "subject"} for s in subjects
        ]

    if "quizzes" in search_areas:
        quizzes = Quiz.query.filter(Quiz.title.ilike(f"%{term}%")).all()
        results["quizzes"] = [
            {
                "id": q.id,
                "title": q.title,
                "type": "quiz",
                "subject_id": q.subject_id,
                "chapter_id": q.chapter_id,
            }
            for q in quizzes
        ]

    return jsonify(results)
