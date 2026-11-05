from flask import Blueprint, jsonify, request

from serializers import loan_to_dict
from services import loans as service

bp = Blueprint("loans", __name__)


@bp.get("/loans")
def list_loans():
    only_overdue = request.args.get("overdue") == "true"
    return jsonify([loan_to_dict(loan, include_current_fine=True) for loan in service.list_loans(only_overdue)])


@bp.get("/loans/<int:loan_id>")
def get_loan(loan_id):
    return jsonify(loan_to_dict(service.get_loan(loan_id), include_current_fine=True))


@bp.post("/loans")
def create_loan():
    data = request.get_json(silent=True) or {}
    return jsonify(loan_to_dict(service.check_out(data))), 201


@bp.post("/loans/<int:loan_id>/return")
def return_book(loan_id):
    return jsonify(loan_to_dict(service.return_book(loan_id)))


@bp.post("/loans/<int:loan_id>/renew")
def renew_loan(loan_id):
    return jsonify(loan_to_dict(service.renew(loan_id)))


@bp.post("/loans/<int:loan_id>/pay-fine")
def pay_fine(loan_id):
    return jsonify(loan_to_dict(service.pay_fine(loan_id)))
