from datetime import datetime

from app.extensions import db

# Association tables for many-to-many relationships for users and roles
user_roles = db.Table(
    "user_roles",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id"), primary_key=True),
)

# Association tables for many-to-many relationships for users and saved quizzes
saved_quizzes = db.Table(
    "saved_quizzes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("quiz_id", db.Integer, db.ForeignKey("quiz.id"), primary_key=True),
)

# Association tables for many-to-many relationships for users and subjects
enrolled_subjects = db.Table(
    "enrolled_subjects",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("subject_id", db.Integer, db.ForeignKey("subject.id"), primary_key=True),
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    # fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=True)

    full_name = db.Column(db.String(120), nullable=False)
    qualification = db.Column(db.String(50))
    dob = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    roles = db.relationship("Role", secondary=user_roles, back_populates="users")
    scores = db.relationship(
        "Score", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    user_answers = db.relationship(
        "UserAnswer", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    saved_quizzes_rel = db.relationship(
        "Quiz", secondary=saved_quizzes, back_populates="saved_by_users"
    )
    enrolled_subjects_rel = db.relationship(
        "Subject", secondary=enrolled_subjects, back_populates="enrolled_users"
    )
