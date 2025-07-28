import os
from datetime import timedelta

from celery.schedules import crontab

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
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_ALGORIGHTM = "HS256"
    JWT_VERIFY_SUB = False

    # Celery Configuration
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://localhost:6379/0"
    )
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_ACCEPT_CONTENT = ["json"]
    CELERY_TIMEZONE = "UTC"
    CELERY_ENABLE_UTC = True
    CELECRY_BEAT_SCHEDULE = {
        "send-daily-reminder": {
            "task": "app.tasks.send_daily_reminders",
            "schedule": crontab(minute="*/1"),
        }
    }

    # Redis Configuration
    REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
