from flask import Blueprint, jsonify

from services import reports as service

bp = Blueprint("reports", __name__)


@bp.get("/reports/overdue")
def report_overdue():
    return jsonify(service.overdue_report())


@bp.get("/reports/summary")
def report_summary():
    return jsonify(service.summary_report())
