from flask import Blueprint

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")

from app.api.admin import (
    analytics,
    # async_jobs,
    chapters,
    questions,
    quizzes,
    subjects,
    users,
)
