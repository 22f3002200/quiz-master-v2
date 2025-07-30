from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from redis import StrictRedis

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
redis_client = StrictRedis.from_url("redis://localhost:6379/0", decode_responses=True)
