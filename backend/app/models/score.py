from datetime import datetime

from app.extensions import db

now = datetime.utcnow()


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(
        db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    correct_count = db.Column(db.Integer, nullable=False)
    wrong_count = db.Column(db.Integer, nullable=False)
    unattempted_count = db.Column(db.Integer, nullable=False)
    total_score = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=now)
    status = db.Column(db.String(20))

    #relationhip
    quiz = db.relationship("Quiz", back_populates="scores")
