from flask import Blueprint

auth_bp = Blueprint("api", __name__, url_prefix="/api/auth")

from app.auth import routes
