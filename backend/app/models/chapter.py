from datetime import datetime

from app.extensions import db

now = datetime.now()


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(
        db.Integer, db.ForeignKey("subject.id", ondelete="CASCADE"), nullable=False
    )  # ForeignKey Relationship
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=now)

    # Relationship
    quizzes = db.relationship(
        "Quiz", backref="chapter", lazy=True, cascade="all, delete-orphan"
    )
