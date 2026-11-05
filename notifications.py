"""Emails to members. outbox.txt stands in for a real mail server.

To use a real mail server, only send_email needs to change.
"""
from rules import money

OUTBOX_PATH = "outbox.txt"  # relative on purpose: created in the folder the API runs from


def send_email(to, subject, body):
    with open(OUTBOX_PATH, "a") as f:
        f.write(f"TO: {to} | SUBJECT: {subject} | BODY: {body}\n")


def checkout_notice(member, book):
    send_email(member["email"], "Book checked out", f"You checked out {book['title']}")


def renewal_notice(member, book):
    send_email(member["email"], "Loan renewed", f"You renewed {book['title']}")


def return_notice(member, book, fine):
    send_email(member["email"], "Book returned", f"You returned {book['title']}. Fine: ${money(fine)}")


def fine_paid_notice(member, amount):
    send_email(member["email"], "Fine paid", f"We received ${money(amount)}")
