"""Library rules: loan length, fines, loan limits and renewals.

No Flask and no database here, so every rule can be tested on its own.
A loan is a dict with the keys due_date, returned, fine and fine_paid.
"""
from datetime import date, timedelta

LOAN_DAYS = 14
MAX_RENEWALS = 1
FINE_PER_DAY = 0.50
LOAN_LIMITS = {"student": 3, "staff": 5}
MEMBER_TYPES = tuple(LOAN_LIMITS)


def money(amount):
    """Round an amount to cents."""
    return round(float(amount), 2)


# ---------- dates ----------


def days_late(due_date, today=None):
    """Days past the due date (negative if it isn't due yet). due_date is 'YYYY-MM-DD'."""
    today = today or date.today()
    return (today - date.fromisoformat(due_date)).days


def is_overdue(due_date, today=None):
    return days_late(due_date, today) > 0


def default_due_date(today=None):
    today = today or date.today()
    return (today + timedelta(days=LOAN_DAYS)).isoformat()


def renewed_due_date(due_date):
    return (date.fromisoformat(due_date) + timedelta(days=LOAN_DAYS)).isoformat()


# ---------- fines ----------


def fine_for(due_date, today=None):
    """Fine for a book returned (or still out) on `today`."""
    return max(0, days_late(due_date, today)) * FINE_PER_DAY


def current_fine(loan, today=None):
    """The stored fine once returned, otherwise what it would be if returned today."""
    if loan["returned"]:
        return loan["fine"]
    return fine_for(loan["due_date"], today)


def amount_owed(loans, today=None):
    """Fines building up on open loans, plus unpaid fines on returned loans."""
    owed = 0
    for loan in loans:
        if not loan["returned"]:
            owed += fine_for(loan["due_date"], today)
        elif not loan["fine_paid"]:
            owed += loan["fine"]
    return owed


# ---------- limits ----------


def loan_limit(member_type):
    return LOAN_LIMITS.get(member_type, LOAN_LIMITS["student"])


def open_loan_count(loans):
    return sum(1 for loan in loans if not loan["returned"])


def loans_remaining(member_type, loans):
    return loan_limit(member_type) - open_loan_count(loans)
