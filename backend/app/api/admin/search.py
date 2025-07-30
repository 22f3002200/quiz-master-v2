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

    # Check the user's role from the g object provided by @user_required
    # current_user_role = g.current_user.get("role") if g.current_user else None

    # # Prevent non-admins from even attempting to search users
    # if "users" in area and current_user_role != "admin":
    #     return jsonify({"error": "You are not authorized to search for users."}), 403

    search_areas = [a.strip() for a in area.split(",")]
    results = {}

    if not term or not search_areas:
        return jsonify(results)

    # --- Publicly searchable items ---
    if "chapter" in search_areas:
        chapters = Chapter.query.filter(Chapter.name.ilike(f"%{term}%")).all()
        # Add a 'type' field to help the frontend with routing
        results["chapters"] = [
            {"id": c.id, "name": c.name, "type": "chapter"} for c in chapters
        ]

    if "subject" in search_areas:
        subjects = Subject.query.filter(Subject.name.ilike(f"%{term}%")).all()
        results["subjects"] = [
            {"id": s.id, "name": s.name, "type": "subject"} for s in subjects
        ]

    if "quizzes" in search_areas:
        quizzes = Quiz.query.filter(Quiz.title.ilike(f"%{term}%")).all()
        results["quizzes"] = [
            {"id": q.id, "title": q.title, "type": "quiz"} for q in quizzes
        ]

    # --- Admin-only search ---
    # Double-check for admin role before searching users
    # if "users" in search_areas and current_user_role == "admin":
    #     users = User.query.filter(User.full_name.ilike(f"%{term}%")).all()
    #     results["users"] = [
    #         {"id": u.id, "full_name": u.full_name, "type": "user"} for u in users
    #     ]

    return jsonify(results)
