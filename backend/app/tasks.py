import csv
from datetime import datetime

from celery import shared_task
from extensions import db
from models.score import Score
from models.user import User
from sqlalchemy import func


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
