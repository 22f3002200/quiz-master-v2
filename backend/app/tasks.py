import csv
import os  # Import the os module
from datetime import datetime, timedelta

from celery import shared_task
from flask_mail import Message
from sqlalchemy import func

from .extensions import db, mail
from .models.score import Score
from .models.user import User


# Task:1 - Download CSV for Admin
@shared_task(ignore_results=False, name="download_csv_report")
def csv_report():
    try:
        users_stat = (
            db.session.query(
                User.id,
                User.full_name,
                User.email,
                func.count(Score.id),
                func.avg(Score.total_score),
                func.max(Score.total_score),
            )
            .outerjoin(Score)
            .group_by(User.id)
            .all()
        )

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"user_performance_{timestamp}.csv"
        filepath = f"app/static/exports/{filename}"

        # Ensure the directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "USER ID",
                    "FULL NAME",
                    "EMAIL",
                    "TOTAL ATTEMPTS",
                    "AVG SCORE",
                    "MAX SCORE",
                ]
            )

            for row in users_stat:
                writer.writerow(
                    [
                        row.id,
                        row.full_name,
                        row.email,
                        row[3],
                        float(row[4]) if row[4] else 0,
                        row[5] or 0,
                    ]
                )

        return {"status": "completed", "url": f"/static/exports/{filename}"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}


# Task:2 - Monthly Report sent via email
@shared_task(ignore_results=False, name="send_monthly_activity_report")
def send_monthly_activity_report():
    try:
        users = User.query.all()

        today = datetime.now()
        last_day_of_prev_month = today.replace(day=1) - timedelta(days=1)
        first_day_of_prev_month = last_day_of_prev_month.replace(day=1)

        reports_sent = 0
        import logging

        logger = logging.getLogger(__name__)
        logger.info(f"Users: {users}")
        for user in users:
            scores = Score.query.filter(
                Score.user_id == user.id,
                Score.timestamp.between(
                    first_day_of_prev_month, last_day_of_prev_month
                ),
            ).all()

            if not scores:
                continue

            total_score = sum(score.total_score for score in scores)
            avg_score = total_score / len(scores)

            report_content = f"""Hi {user.full_name},

Here is your activity report for the last month:

"""
            for score in scores:
                report_content += f"- Quiz: {score.quiz.title if score.quiz else 'Unknown'}, Score: {score.total_score}\n"

            report_content += f"\nAverage Score: {avg_score:.2f}\n\nKeep up the great work!\n\nRegards,\nThe Quiz Master Team"

            try:
                msg = Message(
                    "Your Monthly Quiz Master Report", recipients=[user.email]
                )
                msg.body = report_content
                mail.send(msg)
                reports_sent += 1
            except Exception:
                pass

        return {
            "status": "completed",
            "message": f"Monthly reports sent to {reports_sent} users.",
        }

    except Exception as e:
        return {"status": "failed", "error": str(e)}


# Task:3 - Daily Reminders
@shared_task(ignore_results=False, name="send_daily_reminders")
def send_daily_reminders():
    try:
        inactive_threshold = datetime.now() - timedelta(days=7)

        active_users_in_last_7_days = (
            db.session.query(Score.user_id)
            .filter(Score.timestamp > inactive_threshold)
            .distinct()
        )

        inactive_users = User.query.filter(
            User.id.notin_(active_users_in_last_7_days)
        ).all()

        for user in inactive_users:
            reminder_message = f"Hi {user.full_name},\n\nWe miss you at Quiz Master! Come back and test your knowledge with our new quizzes.\n\nRegards,\nThe Quiz Master Team"

            # --- Send email using Flask-Mail and MailHog ---
            msg = Message("We miss you at Quiz Master!", recipients=[user.email])
            msg.body = reminder_message
            mail.send(msg)
            # -----------------------------------------------

        return {
            "status": "completed",
            "message": f"Reminders sent to {len(inactive_users)} inactive users.",
        }

    except Exception as e:
        return {"status": "failed", "error": str(e)}
