import repository as repo
import rules
from db import connection
from errors import Conflict, InvalidRequest, require
from validation import is_valid_email, is_valid_member_type


def list_members():
    with connection() as conn:
        return repo.list_members(conn)


def get_member(member_id):
    with connection() as conn:
        return require(repo.find_member(conn, member_id), "member not found")


def add_member(data):
    if not data.get("name"):
        raise InvalidRequest("name is required")
    if not is_valid_email(data.get("email")):
        raise InvalidRequest("invalid email")
    member_type = data.get("type", "student")
    if not is_valid_member_type(member_type):
        raise InvalidRequest("type must be " + " or ".join(rules.MEMBER_TYPES))
    with connection() as conn:
        if repo.find_member_by_email(conn, data["email"]) is not None:
            raise Conflict("email already registered")
        member_id = repo.insert_member(conn, data["name"], data["email"], member_type)
        return repo.find_member(conn, member_id)


def member_account(member_id):
    """A member's loans, what they owe, and how many more books they may borrow."""
    with connection() as conn:
        member = require(repo.find_member(conn, member_id), "member not found")
        loans = repo.loans_for_member(conn, member_id)
    return {
        "loans": loans,
        "owed": rules.amount_owed(loans),
        "remaining": rules.loans_remaining(member["type"], loans),
    }
