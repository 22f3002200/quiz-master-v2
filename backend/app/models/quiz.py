from datetime import datetime

from app.extensions import db

from .user import saved_quizzes


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(
        db.Integer, db.ForeignKey("chapter.id", ondelete="CASCADE"), nullable=False
    )  # ForeignKey
    subject_id = db.Column(
        db.Integer, db.ForeignKey("subject.id", ondelete="CASCADE"), nullable=False
    )  # ForeignKey
    title = db.Column(db.String(120), nullable=False)
    date_of_quiz = db.Column(db.Date, nullable=False)
    scheduled_at = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.Text, default="Easy Peasy")
    created_at = db.Column(db.DateTime, default=datetime.utcnow())

    # Relationships
    questions = db.relationship(
        "Question", backref="quiz", lazy=True, cascade="all, delete-orphan"
    )
    user_answers = db.relationship(
        "UserAnswer", backref="quiz", lazy=True, cascade="all, delete-orphan"
    )
    scores = db.relationship(
        "Score", backref="quiz", lazy=True, cascade="all, delete-orphan"
    )
    saved_by_users = db.relationship(
        "User", secondary=saved_quizzes, back_populates="saved_quizzes_rel"
    )
    
