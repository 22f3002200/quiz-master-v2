import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_SAMESITE = "Lax"

    # Flask-Security Configuration
    SECURITY_API_ENABLED_METHODS = ["session", "token"]
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    SECURITY_TOKEN_AUTHENTICATION_TOKEN = "auth_token"
    SECURITY_PASSWORD_SALT = os.environ.get("PASSWORD_SALT") or "super-secret-salt"
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CHANGEABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_UNAUTHORIZED_VIEW = None
    SECURITY_POST_LOGIN_REDIRECT_ENDPOINT = None
    SECURITY_POST_LOGOUT_REDIRECT_ENDPOINT = None

    # JWT configuration
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-string"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORIGHTM = "HS256"
    JWT_VERIFY_SUB = False

    # Celery Configuration
    CELERY_BROKER_URL = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/1"
    CELERY_TIMEZONE = "Asia/Kolkata"
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

    # MailHog configuration
    MAIL_SERVER = "localhost"
    MAIL_PORT = 1025  # Default MailHog SMTP port
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER = "noreply@quizmaster.com"
