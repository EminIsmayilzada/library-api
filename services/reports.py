import repository as repo
import rules
from db import connection


def overdue_report():
    with connection() as conn:
        open_loans = repo.open_loans_with_details(conn)
    items = []
    total = 0
    for loan in open_loans:
        days_late = rules.days_late(loan["due_date"])
        if days_late > 0:
            fine = rules.fine_for(loan["due_date"])
            total += fine
            items.append(
                {
                    "loan_id": loan["loan_id"],
                    "title": loan["title"],
                    "member": loan["member"],
                    "days_late": days_late,
                    "fine": rules.money(fine),
                }
            )
    return {"items": items, "total_fines": rules.money(total)}


def summary_report():
    with connection() as conn:
        total_books = repo.count_books(conn)
        loans = repo.list_loans(conn)
    return {
        "total_books": total_books,
        "on_loan": rules.open_loan_count(loans),
        "fines_outstanding": rules.money(rules.amount_owed(loans)),
    }
