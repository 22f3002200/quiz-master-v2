from app.extensions import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(
        db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False
    )
    statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.Text, nullable=False)
    option2 = db.Column(db.Text, nullable=False)
    option3 = db.Column(db.Text, nullable=False)
    option4 = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)

    # Relationship
    user_answers = db.relationship(
        "UserAnswer", backref="question", lazy=True, cascade="all, delete-orphan"
    )
