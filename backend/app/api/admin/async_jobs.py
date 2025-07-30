from flask import jsonify

from app.api.admin import admin_bp
from app.auth.decorators import admin_required
from app.tasks import csv_report


@admin_bp.route("/export-csv", methods=["POST"])
@admin_required
def export_csv():
    task = csv_report.apply_async()
    result = task.get()
    if result.get("status") == "completed":
        return jsonify(result)
    else:
        return jsonify({"error": result.get("error", "An unknown error occurred")}), 500
