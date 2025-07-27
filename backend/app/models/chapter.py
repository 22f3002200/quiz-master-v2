from datetime import datetime
import pytz

from app.extensions import db

now = datetime.now()
# IST = pytz.timezone("Asia/Kolkata")


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(
        db.Integer, db.ForeignKey("subject.id", ondelete="CASCADE"), nullable=False
    )  # ForeignKey Relationship
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: datetime.utcnow())

    # Relationship
    quizzes = db.relationship(
        "Quiz", backref="chapter", lazy=True, cascade="all, delete-orphan"
    )
