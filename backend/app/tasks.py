import csv
from datetime import datetime, timedelta

from celery import shared_task
from extensions import db, mail  # Import mail instance
from flask_mail import Message  # Import Message class
from models.score import Score
from models.user import User
from sqlalchemy import func


# Task:1 - Download CSV for Admin
@shared_task(ignore_results=False, name="download_csv_report")
def csv_report():
    # ... (existing code is fine)
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
        filepath = f"app/static/{filename}"

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
    """
    Generates and sends a monthly activity report to all users.
    """
    try:
        users = User.query.filter_by(active=True).all()

        for user in users:
            today = datetime.utcnow()
            last_day_of_prev_month = today.replace(day=1) - timedelta(days=1)
            first_day_of_prev_month = last_day_of_prev_month.replace(day=1)

            scores = Score.query.filter(
                Score.user_id == user.id,
                Score.timestamp.between(
                    first_day_of_prev_month, last_day_of_prev_month
                ),
            ).all()

            if not scores:
                continue

            report_content = f"Hi {user.full_name},\n\nHere is your activity report for the last month:\n\n"
            total_score = 0
            for score in scores:
                report_content += (
                    f"- Quiz: {score.quiz.title}, Score: {score.total_score}\n"
                )
                total_score += score.total_score

            avg_score = total_score / len(scores)
            report_content += f"\nAverage Score: {avg_score:.2f}\n\n"
            report_content += (
                "Keep up the great work!\n\nRegards,\nThe Quiz Master Team"
            )

            # --- Send email using Flask-Mail and MailHog ---
            msg = Message("Your Monthly Quiz Master Report", recipients=[user.email])
            msg.body = report_content
            mail.send(msg)
            # -----------------------------------------------

        return {
            "status": "completed",
            "message": "Monthly reports sent to all active users.",
        }

    except Exception as e:
        return {"status": "failed", "error": str(e)}


# Task:3 - Daily Reminders
@shared_task(ignore_results=False, name="send_daily_reminders")
def send_daily_reminders():
    """
    Sends reminders to inactive users.
    """
    try:
        inactive_threshold = datetime.utcnow() - timedelta(days=7)

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
