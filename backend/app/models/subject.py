from datetime import datetime

from app.extensions import db

from .user import enrolled_subjects

now = datetime.now()


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=now)

    # Relationships
    chapters = db.relationship(
        "Chapter", backref="subject", lazy=True, cascade="all, delete-orphan"
    )
    quizzes = db.relationship(
        "Quiz", backref="subject", lazy=True, cascade="all, delete-orphan"
    )
    enrolled_users = db.relationship(
        "User", secondary=enrolled_subjects, back_populates="enrolled_subjects_rel"
    )
