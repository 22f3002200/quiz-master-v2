from datetime import datetime, timedelta

from sqlalchemy import func

from . import create_app, db
from .celery_app import create_celery_app
from .models.score import Score
from .models.user import User

app = create_app()
celery = create_celery_app(app)


@celery.task
def send_daily_reminders():
    with app.app_context():
        seven_days_ago = datetime.utcnow() - timedelta(days=7)

        # Users who have scores, but their last score is older than 7 days
        users_to_remind = (
            db.session.query(User.id, User.email, User.full_name)
            .outerjoin(Score)
            .group_by(User.id)
            .having(func.max(Score.timestamp) < seven_days_ago)
            .all()
        )

        for user in users_to_remind:
            send_reminder_email(user.email, user.full_name)


def send_reminder_email(email, name):
    print(f"Sending reminder email to {name} at {email}")
