from datetime import date

import notifications
import repository as repo
import rules
from db import connection
from errors import Conflict, InvalidRequest, require
from validation import is_valid_date


def list_loans(only_overdue=False):
    with connection() as conn:
        loans = repo.list_loans(conn)
    if only_overdue:
        loans = [loan for loan in loans if not loan["returned"] and rules.is_overdue(loan["due_date"])]
    return loans


def get_loan(loan_id):
    with connection() as conn:
        return require(repo.find_loan(conn, loan_id), "loan not found")


def check_out(data):
    if not data.get("book_id") or not data.get("member_id"):
        raise InvalidRequest("book_id and member_id are required")
    if data.get("due_date") and not is_valid_date(data["due_date"]):
        raise InvalidRequest("invalid due_date")

    with connection() as conn:
        book = require(repo.find_book(conn, data["book_id"]), "book not found")
        member = require(repo.find_member(conn, data["member_id"]), "member not found")
        if not book["available"]:
            raise Conflict("book is not available")

        loans = repo.loans_for_member(conn, member["id"])
        if rules.amount_owed(loans) > 0:
            raise Conflict("member has unpaid fines")
        if rules.open_loan_count(loans) >= rules.loan_limit(member["type"]):
            raise Conflict("loan limit reached")

        today = date.today()
        due_date = data.get("due_date") or rules.default_due_date(today)
        loan_id = repo.insert_loan(conn, data["book_id"], data["member_id"], due_date, today.isoformat())
        repo.set_book_available(conn, data["book_id"], False)
        loan = repo.find_loan(conn, loan_id)

    notifications.checkout_notice(member, book)
    return loan


def return_book(loan_id):
    with connection() as conn:
        loan = require(repo.find_loan(conn, loan_id), "loan not found")
        if loan["returned"]:
            raise Conflict("loan already returned")

        fine = rules.fine_for(loan["due_date"])
        repo.mark_returned(conn, loan_id, fine)
        repo.set_book_available(conn, loan["book_id"], True)
        member = repo.find_member(conn, loan["member_id"])
        book = repo.find_book(conn, loan["book_id"])
        updated = repo.find_loan(conn, loan_id)

    notifications.return_notice(member, book, fine)
    return updated


def renew(loan_id):
    with connection() as conn:
        loan = require(repo.find_loan(conn, loan_id), "loan not found")
        if loan["returned"]:
            raise Conflict("loan already returned")
        if rules.is_overdue(loan["due_date"]):
            raise Conflict("overdue loans cannot be renewed")
        if loan["renewals"] >= rules.MAX_RENEWALS:
            raise Conflict("loan was already renewed")

        repo.extend_loan(conn, loan_id, rules.renewed_due_date(loan["due_date"]))
        member = repo.find_member(conn, loan["member_id"])
        book = repo.find_book(conn, loan["book_id"])
        updated = repo.find_loan(conn, loan_id)

    notifications.renewal_notice(member, book)
    return updated


def pay_fine(loan_id):
    with connection() as conn:
        loan = require(repo.find_loan(conn, loan_id), "loan not found")
        if not loan["returned"]:
            raise Conflict("return the book before paying")
        if loan["fine"] <= 0 or loan["fine_paid"]:
            raise Conflict("no fine to pay")

        repo.mark_fine_paid(conn, loan_id)
        member = repo.find_member(conn, loan["member_id"])
        updated = repo.find_loan(conn, loan_id)

    notifications.fine_paid_notice(member, loan["fine"])
    return updated
