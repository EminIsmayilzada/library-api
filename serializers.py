"""The JSON shape of each kind of record. Each shape is defined once, here."""
from rules import current_fine, money


def book_to_dict(book):
    return {
        "id": book["id"],
        "title": book["title"],
        "author": book["author"],
        "isbn": book["isbn"],
        "available": bool(book["available"]),
    }


def member_to_dict(member):
    return {"id": member["id"], "name": member["name"], "email": member["email"], "type": member["type"]}


def loan_to_dict(loan, include_current_fine=False):
    result = {
        "id": loan["id"],
        "book_id": loan["book_id"],
        "member_id": loan["member_id"],
        "due_date": loan["due_date"],
        "returned": bool(loan["returned"]),
        "fine": money(loan["fine"]),
        "fine_paid": bool(loan["fine_paid"]),
        "renewals": loan["renewals"],
        "checked_out": loan["checked_out"],
    }
    if include_current_fine:
        result["current_fine"] = money(current_fine(loan))
    return result


def member_loan_to_dict(loan):
    """The shorter loan shape used in /members/<id>/loans."""
    return {
        "id": loan["id"],
        "book_id": loan["book_id"],
        "due_date": loan["due_date"],
        "returned": bool(loan["returned"]),
        "fine": money(loan["fine"]),
        "fine_paid": bool(loan["fine_paid"]),
    }
