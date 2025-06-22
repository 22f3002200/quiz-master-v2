from flask_security.core import RoleMixin

from app.extensions import db

from .user import user_roles


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text)

    # Relationship
    users = db.relationship("User", secondary=user_roles, back_populates="roles")
