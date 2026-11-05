from flask import Blueprint, jsonify, request

from rules import money
from serializers import member_loan_to_dict, member_to_dict
from services import members as service

bp = Blueprint("members", __name__)


@bp.get("/members")
def list_members():
    return jsonify([member_to_dict(member) for member in service.list_members()])


@bp.get("/members/<int:member_id>")
def get_member(member_id):
    return jsonify(member_to_dict(service.get_member(member_id)))


@bp.post("/members")
def create_member():
    data = request.get_json(silent=True) or {}
    return jsonify(member_to_dict(service.add_member(data))), 201


@bp.get("/members/<int:member_id>/loans")
def member_loans(member_id):
    account = service.member_account(member_id)
    return jsonify(
        {
            "loans": [member_loan_to_dict(loan) for loan in account["loans"]],
            "total_owed": money(account["owed"]),
            "loans_remaining": account["remaining"],
        }
    )
